---
title: "Conversion Decision Router"
description: "A decision-support prototype that turns a calibrated purchase probability into one of three routes and sends uncertain cases to a person."
meta: "PyTorch · LLM agent · n8n · FastAPI"
dates: "September–October 2026"
role: "Sole author"
status: "Open-source prototype, presented at the GenAI Bootcamp (September 2026)"
order: 2
featured: true
repo: https://github.com/elifbayindir/conversion-quality-router
thumbnail: /assets/img/projects/conversion-decision-router/thumb.jpg
---

## Question

A probability alone does not tell an analyst what to do. When a session arrives, which cases can automation handle, which need a person, and where does a hybrid set-up work best, for a small team with little reviewer time?

## Approach

A PyTorch MLP estimates a calibrated purchase probability per session (UCI Online Shoppers Purchasing Intention dataset, compared against a logistic-regression baseline, PR-AUC as the main metric, group-aware split, leakage audit). A constrained LLM agent maps the evidence to one of three routes in a fixed JSON schema: priority review, human review, or log automatically. A validator checks schema and policy; any invalid output, model or network failure falls back deterministically to human review. n8n handles the workflow and Slack notifications; reviewer feedback goes to an append-only audit store and never retrains the model. The model provider is swappable.

{% include figure.html src="/assets/img/projects/conversion-decision-router/ui_evaluate_session.jpg" width="1600" height="989" alt="The Evaluate Session view: recommended route Priority review, calibrated purchase probability 66.7%, decision threshold 12.0%, uncertainty Clear, and the supporting signals." caption="The result view puts the calibrated probability, the decision threshold, the uncertainty check and the recommended route on one screen." %}

## What I found

On the frozen test split (1,845 sessions, 286 conversions), the two review routes held 67.6% of sessions but captured 95.5% of conversions; a random queue of the same size would capture 67.6%. All 362 uncertain sessions went to human review. These numbers describe one test split, not causal impact or revenue.

{% include figure.html src="/assets/img/projects/conversion-decision-router/operational_route_shares.png" width="1200" height="540" alt="Bar chart of the share of test sessions and of conversions in each of the three routes." caption="Share of test sessions and of conversions per route. The two review routes cover 67.6% of sessions and 95.5% of conversions." %}

{% include figure.html src="/assets/img/projects/conversion-decision-router/calibration_curve.png" width="536" height="568" alt="Calibration curve comparing predicted and observed purchase rates on the test split." caption="Calibration on the test split. Isotonic calibration lowers the test Brier score from 0.2232 to 0.1177." %}

## Outputs

- [Code on GitHub]({{ page.repo }}) (MIT licence)
- [Case study]({{ page.repo }}/blob/main/docs/case-study.md)

## Limitations

- No temporal holdout: the dataset has no timestamps.
- The MLP improves PR-AUC over logistic regression by only 0.014.
- Calibration and the uncertainty band come from one validation split.
- The prototype runs as a single local instance.
