"""Dated, reproducible consolidation checks; no training or threshold tuning."""
from pathlib import Path
from datetime import datetime, timezone
from html.parser import HTMLParser
import hashlib,json,sys,time,subprocess,re
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score,average_precision_score,brier_score_loss,confusion_matrix,precision_score,recall_score,f1_score
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from healthconnect import features,score,CAT
OUT=ROOT/'outputs/validation';OUT.mkdir(parents=True,exist_ok=True)
raw=pd.read_csv(ROOT/'data/raw/healthconnect_appointment_data.csv',keep_default_na=False)
artifact=ROOT/'models/candidate_pipeline.joblib';obj=joblib.load(artifact)
x=features(raw);eligible=raw.appointment_outcome.isin(['Attended','No-Show'])
x=x.loc[eligible];truth=raw.loc[eligible,'appointment_outcome'].eq('No-Show').astype(int)
a=x.appointment_date.lt('2026-03-01');b=x.booking_date.ge('2026-03-01')
modelmetrics=ROOT/'outputs/model/metrics'
summary=json.loads((modelmetrics/'run_summary.json').read_text())
rows=[]
def check(name,expected,fn,evidence):
 try:
  result=fn();rows.append(dict(test=name,expected_result=expected,actual_result=str(result or 'As expected'),status='PASS',issue='',action='Validated current implementation',retest_result='PASS',evidence=evidence))
 except Exception as exc:
  rows.append(dict(test=name,expected_result=expected,actual_result=f'{type(exc).__name__}: {exc}',status='FAIL',issue=str(exc),action='Investigate failure',retest_result='FAIL',evidence=evidence))
def require(cond,message):
 if not cond:raise AssertionError(message)
def source():
 digest=hashlib.sha256((ROOT/'data/raw/healthconnect_appointment_data.csv').read_bytes()).hexdigest()
 require(digest=='1f2c40ae14833b46fe6e1a353446a0e038f19ae06434b37d98545b3e28697137','Source hash changed')
 require(raw.shape==(5000,18),'Source dimensions changed');return digest
check('Original source integrity','Original SHA-256 and 5,000 x 18 retained',source,'data/raw/healthconnect_appointment_data.csv')
def split():
 require((int(a.sum()),int(b.sum()),int((~(a|b)).sum()))==(3682,799,256),'Partition mismatch')
 require(x.loc[a,'appointment_date'].max()<x.loc[b,'booking_date'].min(),'Temporal outcome leakage')
 require(set(raw.loc[x.loc[a].index,'appointment_id']).isdisjoint(raw.loc[x.loc[b].index,'appointment_id']),'Appointment overlap')
 return '3,682 train; 799 reused comparison; 256 purged'
check('Target and temporal split','Cancelled excluded, target No-Show=1, non-overlapping appointments and dates',split,'outputs/model/metrics/fold_definitions.csv')
def folds():
 for f in summary['folds']:
  aa=x.loc[a,'appointment_date'].lt(f['cutoff']);bb=x.loc[a,'booking_date'].ge(f['cutoff']) & x.loc[a,'booking_date'].lt(f['booking_end'])
  require((aa.sum(),bb.sum())==(f['train'],f['validation']),'Fold sizes differ')
  require(x.loc[a].loc[aa,'appointment_date'].max()<x.loc[a].loc[bb,'booking_date'].min(),'Fold leakage')
 return 'All three folds separate available outcomes from later bookings'
check('Internal fold chronology','All training outcomes precede validation bookings',folds,'outputs/model/metrics/fold_definitions.csv')
def selection():
 rank=pd.read_csv(modelmetrics/'validation_ranking.csv');require(rank.iloc[0]['model']==obj['candidate'],'Candidate mismatch')
 oof=pd.read_csv(modelmetrics/'out_of_time_predictions.csv');oo=oof[oof.model.eq(obj['candidate'])]
 choices=[]
 for t in np.linspace(0,1,201):
  pred=oo.probability.ge(t)
  if pred.mean()<=.30:choices.append((recall_score(oo.truth,pred,zero_division=0),precision_score(oo.truth,pred,zero_division=0),-t,t))
 chosen=max(choices)[-1];require(abs(chosen-obj['threshold'])<1e-12,'Threshold mismatch')
 return f'{obj["candidate"]}; threshold {chosen:.3f}; internal predictions only'
check('Candidate and threshold provenance','Existing internal ranking and workload rule reproduce',selection,'outputs/model/metrics/threshold_scenarios.csv')
def preprocessing():
 prep=obj['pipeline'].named_steps['prep'];cols=prep.transformers_[0][2]
 require(set(cols)=={'age','distance_to_clinic_km','is_weekend','log_lead_days'},'Unexpected model feature')
 np.testing.assert_allclose(prep.named_transformers_['numeric'].named_steps['impute'].statistics_,x.loc[a,cols].median().to_numpy(),rtol=0,atol=1e-12)
 for col,categories in zip(CAT,prep.named_transformers_['category'].categories_):require(set(categories)==set(x.loc[a,col]),'Categories differ from training')
 require(obj['pipeline'].classes_.tolist()==[0,1],'Target class order differs')
 return 'Training medians/categories match; identifiers/outcomes/history/reminders/waiting time excluded'
check('Preprocessing and feature eligibility','Fit statistics match training only and class order is [0,1]',preprocessing,'models/candidate_pipeline.joblib')
def parity():
 p=obj['pipeline'].predict_proba(features(raw.loc[x.loc[b].index],require_history=False))[:,1]
 stored=pd.read_csv(modelmetrics/'reused_test_predictions.csv')
 require(stored.appointment_id.tolist()==raw.loc[x.loc[b].index,'appointment_id'].tolist(),'IDs differ')
 np.testing.assert_allclose(p,stored[obj['candidate']],rtol=0,atol=1e-12)
 baseline=pd.read_csv(ROOT/'data/reference/week5_test_predictions.csv')
 np.testing.assert_allclose(stored['Week 5 logistic'],baseline['Logistic regression_probability'],rtol=0,atol=1e-12)
 require(stored.truth.tolist()==truth.loc[b].tolist(),'Target mismatch')
 return 'All 799 candidate and baseline probabilities agree within 1e-12'
check('Frozen prediction and baseline parity','Same appointments, targets and saved probabilities',parity,'outputs/model/metrics/reused_test_predictions.csv')
def metrics_check():
 p=pd.read_csv(modelmetrics/'reused_test_predictions.csv');table=pd.read_csv(modelmetrics/'reused_test_comparison.csv')
 for row in table.itertuples():
  name=obj['candidate'] if row.model.endswith(' capacity scenario') else row.model
  prob=p[name];pred=prob.ge(row.threshold)
  tn,fp,fn,tp=confusion_matrix(p.truth,pred,labels=[0,1]).ravel()
  np.testing.assert_allclose([row.roc_auc,row.average_precision,row.brier,row.recall,row.precision,row.f1],[roc_auc_score(p.truth,prob),average_precision_score(p.truth,prob),brier_score_loss(p.truth,prob),recall_score(p.truth,pred),precision_score(p.truth,pred),f1_score(p.truth,pred)],rtol=0,atol=1e-12)
  require((tn,fp,fn,tp)==(row.tn,row.fp,row.fn,row.tp),'Confusion mismatch')
 return f'{len(table)} result rows independently recalculated'
check('Classification metric reconciliation','Metrics and confusion matrices match saved predictions',metrics_check,'outputs/model/metrics/reused_test_comparison.csv')
# Run the maintained original 17 checks as a separate process.
subprocess.run([sys.executable,str(ROOT/'tests/test_interface.py')],check=True,capture_output=True,text=True)
for row in pd.read_csv(OUT/'interface_results.csv').itertuples():
 rows.append(dict(test=row.test,expected_result='Documented interface behaviour',actual_result=row.status,status=row.status,issue='',action='Reran original interface check',retest_result=row.status,evidence='tests/test_interface.py'))
sample=pd.read_csv(ROOT/'examples/sample_input.csv',keep_default_na=False)
def rejects(d):
 try:score(d,artifact)
 except ValueError as e:return str(e)
 raise AssertionError('Expected a clear ValueError')
def changed(field,value):
 d=sample.copy();d[field]=d[field].astype(object);d.loc[d.index[0],field]=value;return d
check('Duplicate columns rejected','Clear ValueError instead of pandas TypeError',lambda:rejects(pd.concat([sample,sample[['age']]],axis=1)),'src/healthconnect.py')
check('Wrong input container rejected','Clear ValueError',lambda:rejects(sample.to_dict('records')),'src/healthconnect.py')
check('Nonnumeric distance rejected','Clear ValueError',lambda:rejects(changed('distance_to_clinic_km','far')),'src/healthconnect.py')
check('Blank appointment ID rejected','Clear ValueError',lambda:rejects(changed('appointment_id','  ')),'src/healthconnect.py')
check('Invalid calendar date rejected','Clear ValueError',lambda:rejects(changed('booking_date','02/30/2026')),'src/healthconnect.py')
def columns():
 np.testing.assert_array_equal(score(sample,artifact).no_show_probability,score(sample[sample.columns[::-1]],artifact).no_show_probability)
 return 'Input column order does not change scores'
check('Column-order invariance','Probabilities unchanged',columns,'src/healthconnect.py')
def sunday():
 d=sample.copy();d['booking_date']='03/01/2026';d['appointment_date']='03/08/2026'
 require(score(d,artifact).warnings.str.contains('sunday_schedule_conflict').all(),'Missing Sunday warning')
 return 'Sunday conflicts flagged'
check('Sunday warning','All Sunday inputs flagged',sunday,'src/healthconnect.py')
def fullbatch():
 start=time.perf_counter();output=score(raw,artifact);elapsed=time.perf_counter()-start
 require(output.appointment_id.tolist()==raw.appointment_id.tolist(),'Order/ID mismatch')
 require(output.no_show_probability.between(0,1).all(),'Invalid probabilities')
 chunks=pd.concat([score(raw.iloc[i:i+137],artifact) for i in range(0,len(raw),137)],ignore_index=True)
 np.testing.assert_allclose(output.no_show_probability,chunks.no_show_probability,rtol=0,atol=1e-12)
 expected=(output.no_show_probability>=obj['threshold']).astype(int)
 np.testing.assert_array_equal(output.support_flag,expected)
 return f'5,000 synthetic records, chunk parity <=1e-12; batch {elapsed:.3f}s (observation, no SLA). Includes cancelled records for schema stress only, not model-validity evidence.'
check('Full-source batch and chunk reliability','5,000 records preserve order, threshold rule and batch/chunk parity',fullbatch,'src/healthconnect.py')
def kpis():
 counts=raw.appointment_outcome.value_counts();n=len(raw);den=int(eligible.sum())
 expected={'Appointment records':n,'Distinct patients':raw.patient_id.nunique(),'Eligible appointments':den,'Attendance rate':counts['Attended']/den,'No-show rate':counts['No-Show']/den,'Cancellation rate':counts['Cancelled']/n,'Reminder coverage':raw.reminder_sent.eq('Yes').mean()}
 table=pd.read_csv(ROOT/'outputs/analytics/kpi_summary.csv').set_index('metric')
 for name,value in expected.items():np.testing.assert_allclose(table.loc[name,'value'],value,rtol=0,atol=1e-12)
 return 'All seven KPIs agree with independent source calculation'
check('Analytics-to-model cohort and KPI parity','Same 4,737 eligible rows and correct denominators',kpis,'outputs/analytics/kpi_summary.csv')
def segments():
 d=raw.loc[eligible].copy();d['target']=d.appointment_outcome.eq('No-Show')
 d['lead_band']=pd.cut(pd.to_numeric(d.booking_lead_days),[-1,3,7,14,30,np.inf],labels=['0-3 days','4-7 days','8-14 days','15-30 days','31+ days'])
 for field,file in [('lead_band','lead_time_findings'),('reminder_sent','reminder_findings'),('appointment_type','appointment_type_findings')]:
  exp=d.groupby(field,observed=False).target.agg(['sum','count','mean']);actual=pd.read_csv(ROOT/f'outputs/analytics/{file}.csv').set_index(field)
  for key,row in exp.iterrows():np.testing.assert_allclose(actual.loc[str(key),['no_show_count','eligible_appointments','no_show_rate']].astype(float),row.to_numpy(float),rtol=0,atol=1e-12)
  require(int(actual.eligible_appointments.sum())==int(eligible.sum()),'Segment total mismatch')
 return 'Lead-time, reminder and appointment-type tables reconcile to source and totals'
check('Segment analytics reconciliation','Group counts, rates and totals agree',segments,'outputs/analytics/')
def dashboard():
 html=(ROOT/'dashboard/index.html').read_text();data=json.loads(re.search(r'id="dashboard-evidence">(.*?)</script>',html,re.S).group(1))
 require(data['source_sha256']==source(),'Dashboard source mismatch')
 table=pd.read_csv(ROOT/'outputs/analytics/kpi_summary.csv')
 require(data['kpis']==table.to_dict('records'),'Dashboard payload mismatch')
 for row in table.itertuples():
  value=f'{row.value:.1%}' if row.unit=='rate' else f'{row.value:,.0f}'
  require(f'<strong>{value}</strong><span>{row.metric}</span>' in html,'Visible KPI mismatch')
 for target in re.findall(r'<img[^>]*src="([^"]+)"',html):require((ROOT/'dashboard'/target).is_file(),f'Broken dashboard image {target}')
 require('<select' not in html,'Unexpected untested filter')
 return 'Visible cards, evidence payload and chart paths reconcile; static dashboard has no filters'
check('Dashboard data and image consistency','Visible values match exports; chart paths exist',dashboard,'dashboard/index.html')
# Additional descriptive evidence; never used to select/refit candidate.
prob_train=obj['pipeline'].predict_proba(x.loc[a])[:,1]
prob_test=obj['pipeline'].predict_proba(x.loc[b])[:,1]
oof=pd.read_csv(modelmetrics/'out_of_time_predictions.csv');oo=oof[oof.model.eq(obj['candidate'])]
def metricrow(label,y,p):
 return dict(population=label,n=len(y),roc_auc=roc_auc_score(y,p) if len(set(y))>1 else None,average_precision=average_precision_score(y,p),brier=brier_score_loss(y,p))
gaps=pd.DataFrame([metricrow('training (optimistic)',truth[a],prob_train),metricrow('internal OOF (selection exposed)',oo.truth,oo.probability),metricrow('reused comparison',truth[b],prob_test)])
gaps.to_csv(OUT/'generalisation_diagnostics.csv',index=False)
train_ids=set(raw.loc[x.loc[a].index,'patient_id']);evaluation=raw.loc[x.loc[b].index].copy();evaluation['truth']=truth[b];evaluation['probability']=prob_test
evaluation['patient_seen_in_training']=evaluation.patient_id.isin(train_ids)
segment_rows=[]
for field in ['gender','age_group','appointment_type','patient_seen_in_training']:
 for group,part in evaluation.groupby(field):
  for threshold in [.5,obj['threshold']]:
   tn,fp,fn,tp=confusion_matrix(part.truth,part.probability.ge(threshold),labels=[0,1]).ravel()
   segment_rows.append(dict(field=field,group=group,threshold=threshold,n=len(part),positives=int(part.truth.sum()),negatives=int((1-part.truth).sum()),tn=tn,fp=fp,fn=fn,tp=tp,recall=tp/(tp+fn) if tp+fn else np.nan,false_positive_rate=fp/(fp+tn) if fp+tn else np.nan))
pd.DataFrame(segment_rows).to_csv(OUT/'segment_diagnostics.csv',index=False)
cal=evaluation.copy();cal['bin']=pd.qcut(cal.probability,5,duplicates='drop')
cal.groupby('bin',observed=True).agg(n=('truth','size'),mean_probability=('probability','mean'),observed_no_show_rate=('truth','mean')).to_csv(OUT/'calibration_bins.csv')
for name,expected in [('Fresh temporal evaluation','New later labelled appointments, not the reused 799 records'),('Verified human HC-POD collaboration','Actual participant exchange or programme acceptance'),('Operational readiness','Confirmed cancellation workflow, scheduling, identity, fairness and capacity criteria')]:
 rows.append(dict(test=name,expected_result=expected,actual_result='Evidence not supplied',status='BLOCKED',issue='External evidence unavailable',action='Document limitation; do not invent evidence',retest_result='NOT RUN',evidence='docs/validation.md'))
rows.append(dict(test='Dashboard filters',expected_result='Interactive filter behaviour if implemented',actual_result='Static report has no filter controls',status='NOT APPLICABLE',issue='',action='No new filtering feature required',retest_result='NOT APPLICABLE',evidence='dashboard/index.html'))
pd.DataFrame(rows).to_csv(OUT/'validation_results.csv',index=False)
metadata={'executed_at':datetime.now(timezone.utc).isoformat(),'source_sha256':source(),'candidate':obj['candidate'],'threshold':obj['threshold'],'train_test_shared_patient_ids':len(train_ids & set(evaluation.patient_id)),'reused_set_returning_rows':int(evaluation.patient_seen_in_training.sum()),'reused_set_unseen_id_rows':int((~evaluation.patient_seen_in_training).sum()),'counts':pd.Series([r['status'] for r in rows]).value_counts().to_dict(),'fresh_holdout':False,'human_collaboration_verified':False}
(OUT/'run_summary.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(json.dumps(metadata,indent=2));print(gaps.to_string(index=False))
failed=[r for r in rows if r['status']=='FAIL']
if failed:print(json.dumps(failed,indent=2));sys.exit(1)
