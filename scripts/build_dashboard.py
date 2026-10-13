"""Build the existing descriptive dashboard from exported analytics evidence."""
from pathlib import Path
from html import escape
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/analytics'
kpis = pd.read_csv(OUT / 'kpi_summary.csv')
lead = pd.read_csv(OUT / 'lead_time_findings.csv')
values = kpis.set_index('metric').value
source_hash = hashlib.sha256((ROOT / 'data/raw/healthconnect_appointment_data.csv').read_bytes()).hexdigest()
def fmt(value, unit):
    return f'{value:.1%}' if unit == 'rate' else f'{value:,.0f}'
cards = ''.join(f'<article class="kpi"><strong>{fmt(row.value, row.unit)}</strong><span>{escape(row.metric)}</span></article>' for row in kpis.itertuples())
rows = ''.join(f'<tr><td>{escape(row.metric)}</td><td>{escape(row.definition)}</td><td>{fmt(row.value, row.unit)}</td></tr>' for row in kpis.itertuples())
charts = ''.join(f'<section><h2>{title}</h2><img src="../outputs/analytics/figures/{name}.png" alt="{title}"><p>{note}</p></section>' for name,title,note in [
 ('outcome_mix','Appointment outcomes','Eligible appointments = Attended + No-Show. A no-show is not a completed visit. Cancellations are reported separately.'),
 ('lead_time_no_show','Booking lead time','Descriptive association in fictional records; longer lead time is not established as a cause.'),
 ('reminder_association','Recorded reminders','Reminder timing, assignment and delivery are uncontrolled. This comparison does not measure effectiveness.'),
 ('appointment_type_no_show','Appointment type','Segment counts describe service mix; differences do not justify punitive treatment.')])
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>HealthConnect | Appointment analytics</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#f5f2eb;color:#20242a;font:16px/1.6 Arial,sans-serif}}header{{background:#17191d;color:white;padding:44px max(6vw,24px);border-bottom:4px solid #b18a45}}header p{{color:#ddd6c6}}h1{{font-size:36px;line-height:1.15;margin:10px 0}}.eyebrow{{font-size:12px;letter-spacing:2px;text-transform:uppercase}}main{{max-width:1080px;margin:28px auto;padding:0 22px}}h2{{font-size:23px;margin:0 0 12px}}.kpis{{display:flex;flex-wrap:wrap;gap:14px;margin:24px 0}}.kpi,section{{background:white;padding:22px}}.kpi{{flex:1 1 190px;border-top:3px solid #b18a45}}.kpi strong{{display:block;font-size:30px}}.kpi span{{font-size:13px;color:#555}}section{{margin:18px 0}}img{{width:100%;height:auto;display:block;max-width:860px;margin:auto}}table{{width:100%;border-collapse:collapse;font-size:14px}}th{{text-align:left;background:#25282e;color:white}}td,th{{padding:12px;border-bottom:1px solid #ddd}}.table-wrap{{overflow-x:auto}}footer{{font-size:12px;color:#666;overflow-wrap:anywhere;padding:20px 0}}a{{color:#72551f}}@media(max-width:520px){{h1{{font-size:28px}}main{{padding:0 12px}}section{{padding:16px}}}}
</style></head><body><header><div class="eyebrow">Wilson Moses / AnalystLab Africa</div><h1>HealthConnect appointment analytics</h1><p>Descriptive decision support • Fictional clinic • Portfolio prototype</p></header><main>
<section><h2>What the data shows</h2><p>Among {values['Eligible appointments']:,.0f} eligible appointments, {values['No-show rate']:.1%} were no-shows. Observed no-show rates range from {lead.iloc[0].no_show_rate:.1%} for bookings 0–3 days ahead to {lead.iloc[-1].no_show_rate:.1%} for 31+ days.</p><p>These patterns motivate a prospective test of supportive confirmation timing. They do not establish attendance improvement.</p></section>
<div class="kpis">{cards}</div>{charts}<section><h2>KPI definitions</h2><div class="table-wrap"><table><thead><tr><th>Metric</th><th>Definition</th><th>Value</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section><h2>How this connects to the model</h2><p>The model uses booking-known scheduling and demographic inputs. Reminder activity and waiting time remain descriptive fields, excluded from prediction because their timing is unverified. The analytics and model share the same source and target definition; this dashboard does not run live inference.</p><p>See <a href="../docs/validation.md">validation evidence</a> and <a href="../README.md">the complete project</a>. No human partner approval, deployment or intervention benefit is claimed.</p></section>
<footer>Static report: no filters, live feed or patient outreach. Rebuild with scripts/analyze_healthconnect.py. Consolidated 11 October 2026. Source SHA-256: {source_hash}</footer>
<script type="application/json" id="dashboard-evidence">{json.dumps({'source_sha256':source_hash,'kpis':kpis.to_dict('records')})}</script>
</main></body></html>'''
(ROOT / 'dashboard').mkdir(exist_ok=True)
(ROOT / 'dashboard/index.html').write_text(html)
print('Generated dashboard/index.html from analytics outputs')
