# HealthConnect: Intelligent Appointment Management

An end-to-end healthcare data science project exploring how appointment data can be transformed into practical intelligence for improving patient attendance and clinic operations.

The project follows the complete data science lifecycle—from business understanding and data assessment to modelling, evaluation, deployment and feedback. Its initial use case is the prediction of appointment no-shows so that clinic staff can identify appointments that may benefit from timely attendance support.

> **Current phase:** Problem definition and initial data assessment  
> **Programme:** AnalystLab Africa Data Science Internship — Experience Lab  
> **Author:** Wilson Moses

## Project purpose

Missed appointments can leave clinical capacity underused, disrupt schedules and affect the delivery of timely patient services. HealthConnect currently has limited data-driven capability to identify which scheduled appointments may be at risk of becoming no-shows.

This project investigates whether historical appointment data can support a responsible and operationally useful solution that helps the clinic:

- understand patterns in appointment attendance;
- estimate the likelihood of a future no-show;
- prioritise appropriate reminder or follow-up support;
- use scheduled appointment capacity more effectively; and
- make informed decisions using interpretable evidence.

A model creates value only when its results support a suitable clinic action and that action leads to measurable operational improvement.

## Core project question

> Can HealthConnect use information available before a scheduled appointment to identify appointments at risk of becoming no-shows and support more effective attendance interventions?

## Project objectives

1. Define the clinic problem and translate it into a clear analytical task.
2. Assess the quality, relevance and suitability of the available appointment data.
3. Explore the factors associated with attendance and no-shows.
4. Prepare a reproducible and leakage-safe modelling dataset.
5. Develop and compare interpretable classification models.
6. Evaluate predictive performance, operational usefulness and fairness.
7. Demonstrate how risk estimates could support clinic workflows.
8. Establish a feedback process for monitoring outcomes and model performance.

## Data science methodology

The project is structured around the IBM Data Science Methodology.

| Stage | Application to HealthConnect |
|---|---|
| Business Understanding | Define the operational problem, stakeholders, intended action and success criteria. |
| Analytical Approach | Translate the business need into descriptive, diagnostic and predictive questions. |
| Data Requirements | Determine which information is needed and when it must be available. |
| Data Collection | Review the supplied resources, provenance and information gaps. |
| Data Understanding | Examine structure, distributions, relationships and data-quality concerns. |
| Data Preparation | Build a documented modelling cohort and leakage-safe preprocessing workflow. |
| Modelling | Establish a baseline and compare suitable classification models. |
| Evaluation | Assess model errors, operational value, interpretability and subgroup performance. |
| Deployment | Demonstrate how clinic staff could access and act on predictions. |
| Feedback | Monitor performance, outcomes, data drift and staff feedback over time. |

## Proposed analytical approach

The initial machine-learning task is **supervised binary classification** at appointment level:

- **Positive class:** `No-Show`
- **Negative class:** `Attended`
- **Unit of analysis:** one scheduled appointment
- **Proposed output:** probability that an appointment will result in a no-show
- **Provisional prediction point:** after booking and before the appointment occurs

`Cancelled` appointments are retained in the source data but temporarily excluded from the first binary experiment. They are not automatically classified as either attended appointments or no-shows. This decision will be revisited once cancellation timing and the intended scoring workflow are better understood.

## Dataset overview

The supplied fictional dataset contains historical appointment records for the HealthConnect Clinic scenario.

| Measure | Value |
|---|---:|
| Appointment records | 5,000 |
| Variables | 18 |
| Anonymised patient identifiers | 1,696 |
| No-shows | 2,423 |
| Attended appointments | 2,314 |
| Cancelled appointments | 263 |
| Provisional binary cohort | 4,737 |
| No-show rate in binary cohort | 51.15% |

One record represents an appointment rather than a unique patient. A patient identifier may therefore appear in multiple records.

## Initial data assessment

The first assessment indicates that the data can support a learning prototype, subject to documented assumptions and further validation.

### Positive findings

- No exact duplicate records or duplicate appointment identifiers were detected.
- Derived weekday, age-group and booking-lead-time fields agree with their source variables.
- Previous no-show counts do not exceed previous appointment counts.
- The provisional binary target is approximately balanced.

### Issues requiring investigation

- `distance_to_clinic_km` is missing in 90 records.
- `estimated_waiting_time_min` is missing in 60 records.
- The literal value `None` in `reminder_channel` represents no reminder channel and must not be mistaken for an unknown value.
- The actual CSV date format differs from the ISO format stated in the data dictionary.
- The dataset includes 737 Sunday appointments despite the stated Sunday closure.
- Repeated patient identifiers contain age histories that may not represent reliable longitudinal patient records.
- The creation time of the waiting-time estimate is unspecified, so its availability at prediction time is uncertain.
- Reminder and cancellation timestamps are unavailable, limiting reconstruction of what staff knew at a particular decision point.

These issues will not be silently corrected. Each one will be investigated, documented and either resolved, excluded or retained with an explicit limitation.

## Potential feature groups

Candidate predictors will be evaluated for relevance, reliability, fairness and availability at the selected prediction point.

| Feature group | Examples |
|---|---|
| Demographic | Age, age group and gender |
| Appointment | Appointment type, weekday and time period |
| Booking | Booking lead days |
| Patient history | Previous appointments and previous no-shows |
| Engagement | Reminder status and reminder channel |
| Accessibility | Distance to the clinic |
| Operational | Estimated waiting time |

Record identifiers will not be treated as ordinary predictive features. Any variable created or updated after the prediction point will be excluded to prevent data leakage.

## Planned modelling and evaluation

The modelling stage will begin with a simple benchmark before introducing more sophisticated methods.

1. Define the eligible modelling cohort.
2. Separate training and test data appropriately.
3. Fit preprocessing operations using training data only.
4. Establish a simple baseline.
5. Train an interpretable logistic-regression model.
6. Compare selected tree-based alternatives where justified.
7. Evaluate precision, recall, F1-score, ROC-AUC and confusion matrices.
8. Select decision thresholds using clinic priorities rather than accuracy alone.
9. Review interpretability and performance across relevant patient groups.
10. Assess whether predictions can support a realistic staff intervention.

Final metrics and model choices will be added only after the relevant modelling and evaluation stages are completed.

## Responsible use

This is an educational project based on a fictional clinic scenario. It is not a clinical decision system and should not be used to diagnose, rank or deny care to patients.

The project will consider patient privacy, responsible use of demographic variables, unequal error rates across patient groups, the distinction between prediction and causation, transparent communication of uncertainty, human review and continued monitoring. Patients should receive supportive rather than punitive interventions based on predicted risk.

## Project roadmap

| Phase | Focus | Status |
|---|---|---|
| 1. Foundation | Resource review, business understanding and problem definition | Completed |
| 2. Data assessment | Initial quality and suitability analysis | Completed |
| 3. Exploration | Structured exploratory data analysis and hypothesis development | Planned |
| 4. Preparation | Cleaning, feature engineering and modelling-cohort creation | Planned |
| 5. Modelling | Baseline and candidate classification models | Planned |
| 6. Evaluation | Predictive, operational and fairness assessment | Planned |
| 7. Deployment | Demonstration of prediction delivery and staff use | Planned |
| 8. Feedback | Monitoring, learning and improvement framework | Planned |

The roadmap will be updated as new evidence changes the project assumptions or analytical direction.

## Current repository structure

```text
HealthConnect/
├── data/
│   └── raw/
│       ├── HealthConnect_Appointment_Data.csv
│       └── HealthConnect_Data_Dictionary.csv
├── notebooks/
│   └── HealthConnect_Week4_ML_Problem_Definition.ipynb
├── reports/
│   ├── HealthConnect_Week4_ML_Problem_Definition_Report.docx
│   ├── HealthConnect_Week4_ML_Problem_Definition_Report.pdf
│   ├── HealthConnect_Week4_Project_Summary.docx
│   └── HealthConnect_Week4_Project_Summary.pdf
├── supporting/
│   └── HealthConnect_Week4_Data_Quality_Decision_Log.md
└── README.md
```

The original data is preserved in `data/raw/`. Cleaned or transformed datasets created later should be stored separately so that all processing steps remain reproducible.

## Current deliverables

- Machine Learning Problem Definition Report
- Executed Problem Definition and Data Assessment Notebook
- Week 4 Project Summary
- Data Quality and Decision Log
- Project README

## Key learning outcomes

This project demonstrates the ability to:

- translate a business problem into a data science problem;
- apply the IBM Data Science Methodology;
- assess whether data is suitable before modelling;
- distinguish business objectives, predictions and interventions;
- identify data leakage and prediction-time constraints;
- document assumptions, risks and limitations; and
- communicate technical findings to non-technical stakeholders.

## Author

**Wilson Moses**  
Aspiring Data Scientist and AI Engineer  
AnalystLab Africa — Data Science Internship Programme, Batch D

## Acknowledgement

Developed as part of the AnalystLab Africa Experience Lab. The HealthConnect clinic scenario and supplied resources are used for educational and portfolio purposes.
