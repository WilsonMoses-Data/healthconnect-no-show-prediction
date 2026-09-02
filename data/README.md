# HealthConnect dataset documentation

## Files

- `raw/healthconnect_appointment_data.csv` — original appointment-level dataset supplied for the Experience Lab scenario.
- `healthconnect_data_dictionary.csv` — definitions and notes for all 18 variables.

## Source and scope

The dataset was supplied through the AnalystLab Africa Experience Lab for the fictional HealthConnect Clinic scenario. It contains synthetic and anonymised educational data, not real patient records.

One row represents one scheduled appointment. The same anonymised patient identifier may occur across several appointments.

## Structure

- 5,000 appointment records
- 18 variables
- 1,696 anonymised patient identifiers
- Target source field: `appointment_outcome`
- Outcomes: `Attended`, `No-Show` and `Cancelled`

## Raw-data protection

The file in `raw/` is preserved unchanged. Quality issues are documented rather than corrected in place. Future transformations should be written to a separate processed-data location with a transformation log.

## Known quality and interpretation issues

- 90 missing values in `distance_to_clinic_km`.
- 60 missing values in `waiting_time_minutes`.
- `None` in `reminder_channel` is a meaningful “no reminder” category.
- The observed date format is month/day/year, while the dictionary examples use ISO dates.
- 737 appointments occur on Sundays despite the scenario’s stated Sunday closure.
- Repeated patient identifiers contain inconsistent age histories.
- Reminder, cancellation and waiting-time creation timestamps are unavailable.

## Licence and attribution

The repository’s MIT Licence applies to Wilson Moses’s original code and documentation. It does not transfer ownership of the supplied scenario, dataset or data dictionary. Reuse should follow the terms of the educational source.
