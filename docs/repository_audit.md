# Consolidation audit

**11 October 2026 | Wilson Moses | HealthConnect**

## What the repository actually contains

The main branch stopped at Week 5 while the README described Week 4. Week 6 and Week 8 existed on separate remote branches. The recoverable project includes a Data Science workflow, saved classifier, raw-input batch scorer, technical interface tests, descriptive analytics, static dashboard, and historical reports. No API deployment, live app, GenAI assistant, actual patient outreach, or verified human cross-track exchange was found.

The principal modelling result is a no-history logistic candidate selected internally. Raw reminders are used descriptively, not predictively. The Week 8 package is an analytics contribution; it does not evidence a new final predictive model.

## Issues resolved

| Finding | Consequence | Resolution |
|---|---|---|
| Separate unmerged branch packages | Visitors cannot see whole project from main | Consolidated source on a local review branch |
| README labelled model work planned | Portfolio understated actual implemented work | Rewrite for complete scope and evidence |
| Three identical raw-data copies, two identical dictionaries | Ambiguous source and unnecessary files | Keep one canonical original of each; compare hashes first |
| Week 5 wrong-case source and missing export directory | Notebook fails from a clean checkout | Correct path and create generated-data directory |
| Root dependencies omit modelling packages | Incomplete setup | Core pinned requirements and optional notebook requirements |
| Current-directory-dependent training script | Launch failures | Resolve paths from script location |
| Duplicated model code in notebook and script | Future drift | Notebook delegates to maintained source script |
| Duplicate input columns cause internal TypeError | Unclear malformed-data response | Explicit schema ValueError and regression check |
| Hard-coded dashboard with embedded duplicate charts | Stale values and excessive file size | Generate HTML from evidence; reference chart assets |
| “Completed appointments” includes no-shows | Misleading terminology | Current outputs use “eligible appointments”; denominator unchanged |
| Missing dated Week 7 completion record | Final integration lacks consolidated test trace | Requirement matrix and subsequent validation; external gaps remain explicit |

## What stayed intentionally

Original raw data and dictionary, preserved baseline reference predictions, the small trusted local model artefact, sample input/output, interpretable current figures, branding, original notebooks, and unique historical reports. The existing licence was retained and no rights over third-party educational data were added.

The old social-preview image is retained for GitHub repository metadata rather than inserted redundantly into the README. Week 4 visual assets remain because the maintained source-assessment script regenerates them. Unique PDFs are archived instead of recreated or silently rewritten. Generated processed cohorts, baseline figures, caches, environments, and logs are ignored.

## Cleanup record

[cleanup.csv](cleanup.csv) records source path, action, reason, and final location for each move/removal. New validation and documentation files are visible in the review diff. Canonical raw SHA-256 remains `1f2c40ae14833b46fe6e1a353446a0e038f19ae06434b37d98545b3e28697137`.

## Limits of the audit

This review covers the three named branches and the supplied Week 7 assignment. It does not verify external form submissions, unpublished local files, actual human exchanges, or the full contents of a clinic knowledge base absent from this checkout. Sunday-closure statements originate in prior project reports; real clinic hours were not independently established. No secret values were required. Public-report author contact details were retained in historical documents.

See [validation.md](validation.md) for technical outcomes and unresolved evidence requirements, and [handoff.md](handoff.md) for presentation guidance and publication metadata.
