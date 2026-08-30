# HealthConnect Clinic Experience Lab - Week 4

## Project overview

This repository documents the Week 4 foundation stage of the AnalystLab Africa Data Science Internship Experience Lab. It investigates whether historical appointment information can support prediction of no-shows and prioritisation of patient attendance support.

## IBM methodology applied

1. Business Understanding
2. Analytical Approach
3. Data Requirements
4. Data Collection
5. Initial Data Understanding

Week 4 defines and assesses the proposed solution; it does not train or deploy the final model.

## Proposed machine-learning problem

The initial task is supervised binary classification at appointment level. No-Show is the positive class and Attended is the negative class. Cancelled appointments are preserved but temporarily excluded from the first binary experiment.

## Initial data snapshot

- 5,000 appointment records and 18 variables
- 1,696 anonymised patient identifiers
- 2,423 no-shows, 2,314 attended appointments and 263 cancellations
- 4,737 records in the provisional binary cohort
- 51.15% no-show rate within the binary cohort

## Key observations

- No exact duplicate rows or duplicate appointment identifiers were found.
- Distance is missing in 90 records and waiting time in 60.
- Reminder channel None means that no reminder was sent.
- The CSV date format differs from the dictionary's stated ISO format.
- The dataset includes 737 Sunday appointments despite the stated Sunday closure.
- Repeated patient identifiers contain inconsistent histories and require caution.

## Repository structure

HealthConnect_Week4/
- data/raw/
- notebooks/
- reports/
- supporting/
- README.md

## Proposed Week 5 focus

Conduct structured exploratory analysis, investigate identified quality concerns, confirm the prediction point and create a documented modelling cohort with leakage-safe preprocessing and evaluation.

## Author

Wilson Moses
AnalystLab Africa - Data Science Internship Programme, Batch D
