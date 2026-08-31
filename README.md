# HealthConnect: Intelligent Appointment Management

> An ongoing healthcare data-science project exploring how appointment data can support responsible no-show prediction and more effective clinic operations.

**Programme:** AnalystLab Africa Data Science Internship — Experience Lab  
**Current phase:** Problem definition and initial data assessment  
**Author:** [Wilson Moses](https://github.com/WilsonMoses-Data)

## Project overview

Missed appointments can leave clinical capacity underused, disrupt schedules, and limit timely patient support. HealthConnect currently has limited data-driven capability to identify scheduled appointments that may be at risk of becoming no-shows.

This project applies the IBM Data Science Methodology to investigate whether historical appointment data can support a responsible and operationally useful attendance-intervention workflow.

> **Core question:** Can information available before a scheduled appointment help identify appointments at risk of becoming no-shows and support more effective attendance interventions?

## Objectives

1. Translate the clinic problem into a clear analytical task.
2. Assess whether the supplied data is relevant, reliable, and available at the intended prediction point.
3. Explore the factors associated with attendance and no-shows.
4. Prepare a reproducible and leakage-safe modelling dataset.
5. Establish an interpretable baseline and compare suitable classification models.
6. Evaluate predictive performance, operational usefulness, and fairness.
7. Demonstrate how risk estimates could support clinic workflows.
8. Define a feedback process for monitoring outcomes and model performance.

## Current analytical approach

The proposed machine-learning task is supervised binary classification at appointment level.

| Element | Definition |
|---|---|
| Positive class | `No-Show` |
| Negative class | `Attended` |
| Unit of analysis | One scheduled appointment |
| Proposed output | Probability that an appointment results in a no-show |
| Provisional prediction point | After booking and before the appointment occurs |

`Cancelled` appointments are retained in the source data but excluded from the first binary experiment. They are not automatically treated as attended appointments or no-shows.

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

One row represents an appointment, not a unique patient. Patient identifiers may therefore appear more than once.

## Methodology

| IBM Data Science stage | Application to HealthConnect |
|---|---|
| Business Understanding | Define the operational problem, stakeholders, intended intervention, and success criteria |
| Analytical Approach | Translate the business need into descriptive, diagnostic, and predictive questions |
| Data Requirements | Determine the required information and when it must be available |
| Data Collection | Review supplied resources, provenance, and information gaps |
| Data Understanding | Examine structure, distributions, relationships, and quality concerns |
| Data Preparation | Define the modelling cohort and build leakage-safe preprocessing |
| Modelling | Establish a baseline and compare suitable classifiers |
| Evaluation | Assess errors, operational value, interpretability, and subgroup performance |
| Deployment | Demonstrate how clinic staff could access and act on predictions |
| Feedback | Monitor performance, outcomes, drift, and staff feedback |

## Initial data assessment

### Positive findings

- No exact duplicate rows or duplicate appointment identifiers were detected.
- Derived weekday, age-group, and booking-lead-time fields agree with their source variables.
- Previous no-show counts do not exceed previous appointment counts.
- The provisional binary target is approximately balanced.

### Issues requiring investigation

- `distance_to_clinic_km` is missing in 90 records.
- `estimated_waiting_time_min` is missing in 60 records.
- The literal value `None` in `reminder_channel` represents no reminder channel, not an unknown value.
- The CSV date format differs from the ISO format stated in the data dictionary.
- The data contains 737 Sunday appointments despite a stated Sunday closure.
- Repeated patient identifiers contain age histories that may not support reliable longitudinal interpretation.
- The creation time of the waiting-time estimate is unspecified, making prediction-time availability uncertain.
- Reminder and cancellation timestamps are unavailable, limiting reconstruction of what staff knew at a given decision point.

These issues are documented rather than silently corrected. Each will be resolved, excluded, or retained with an explicit limitation.

## Candidate feature groups

| Group | Examples |
|---|---|
| Demographic | Age, age group, gender |
| Appointment | Appointment type, weekday, time period |
| Booking | Booking lead days |
| Patient history | Previous appointments, previous no-shows |
| Engagement | Reminder status, reminder channel |
| Accessibility | Distance to clinic |
| Operational | Estimated waiting time |

Identifiers will not be used as ordinary predictors. Variables created or updated after the prediction point will be excluded to prevent leakage.

## Planned modelling and evaluation

1. Define the eligible modelling cohort.
2. Separate training and test data appropriately.
3. Fit preprocessing operations using training data only.
4. Establish a simple benchmark.
5. Train an interpretable logistic-regression model.
6. Compare selected tree-based alternatives where justified.
7. Evaluate precision, recall, F1-score, ROC-AUC, and confusion matrices.
8. Select thresholds using clinic priorities rather than accuracy alone.
9. Review interpretability and subgroup performance.
10. Assess whether predictions support a realistic staff intervention.

Final metrics and model choices will be published only after the modelling and evaluation stages are completed.

## Project status

| Phase | Status |
|---|---|
| Business understanding and problem definition | Completed |
| Initial data-quality and suitability assessment | Completed |
| Structured exploratory analysis | Planned |
| Data preparation and feature engineering | Planned |
| Modelling | Planned |
| Predictive, operational, and fairness evaluation | Planned |
| Deployment demonstration | Planned |
| Feedback and monitoring framework | Planned |

## Repository contents

```text
HealthConnect-Healthcare-Data-Science-AI-Project/
├── README.md
├── LICENSE
├── HealthConnect_Appointment_Data.csv
├── HealthConnect_Data_Dictionary - Data Dictionary.csv
├── HealthConnect_Week4_ML_Problem_Definition.ipynb
├── HealthConnect_Week4_ML_Problem_Definition_Report.pdf
└── HealthConnect_Week4_Project_Summary.pdf
```

### Key files

- [`HealthConnect_Week4_ML_Problem_Definition.ipynb`](HealthConnect_Week4_ML_Problem_Definition.ipynb) — executed notebook covering the problem definition and initial assessment.
- [`HealthConnect_Week4_ML_Problem_Definition_Report.pdf`](HealthConnect_Week4_ML_Problem_Definition_Report.pdf) — formal project report.
- [`HealthConnect_Week4_Project_Summary.pdf`](HealthConnect_Week4_Project_Summary.pdf) — concise Week 4 summary.

## Tools used

- Python
- pandas
- NumPy
- Jupyter Notebook

Later phases will document additional tools only when they are actually used.

## Responsible use

This is an educational project based on a fictional clinic scenario. It is not a clinical decision system and must not be used to diagnose patients, rank access to care, or deny services.

The project considers privacy, responsible use of demographic variables, unequal error rates, prediction versus causation, uncertainty, human review, and continued monitoring. Any intervention should be supportive rather than punitive.

## Reproducing the current analysis

1. Clone the repository.
2. Create a Python environment.
3. Install Jupyter, pandas, and NumPy.
4. Open `HealthConnect_Week4_ML_Problem_Definition.ipynb`.
5. Run the notebook from top to bottom with the CSV files retained at repository root.

The repository should add a pinned dependency file as the project expands.

## Learning outcomes

- Translating a business problem into a data-science problem.
- Applying the IBM Data Science Methodology.
- Assessing data suitability before modelling.
- Distinguishing predictions from interventions and business outcomes.
- Identifying data leakage and prediction-time constraints.
- Communicating assumptions, risks, and limitations.

## Licence and acknowledgement

Original code and documentation are released under the repository’s [MIT Licence](LICENSE). The HealthConnect scenario and supplied resources were provided for educational use through the AnalystLab Africa Experience Lab; their inclusion does not transfer ownership of the underlying material.

## Contact

**Wilson Moses** — Data Scientist × AI Engineer in development  
[LinkedIn](https://www.linkedin.com/in/wilson-moses-9207b22bb) · [GitHub](https://github.com/WilsonMoses-Data) · [Moses Learns Data](https://www.tiktok.com/@moses.learnsdata)
