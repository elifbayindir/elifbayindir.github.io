---
title: "Forecasting and uncertainty in repeated cognitive assessments"
summary: "Comparing seven forecasting procedures, including the tabular foundation model TabPFN-2, on 23,994 assessment cycles from 3,283 users."
meta: "MSc thesis · Funded project · First-author paper under review"
dates: "2024–2026"
role: "MSc thesis and BAP-funded project (grant 20451), proposal author"
status: "First-author paper under review at IEEE JBHI"
supervisors: "Assoc. Prof. Ercan Atam, Prof. Şefik Şuayb Arslan (Control and Intelligent Systems Laboratory, Boğaziçi University)"
order: 1
featured: true
# repo: TODO(elif): public demo of the pipeline on synthetic data, once it exists
---

## Question

Can forecasting and anomaly detection on repeated digital cognitive assessments flag when a person's performance departs from their own trend, as a tool for early dementia prevention? And does point accuracy alone distinguish good models?

## Approach

23,994 assessment cycles from 3,283 users of a digital cognitive assessment platform. Seven forecasting procedures compared with rolling-origin (temporal) validation: statistical baselines, tree ensembles and the pretrained tabular foundation model TabPFN-2. Evaluation of both point error and the calibration of prediction intervals.

The seven procedures were persistence, simple exponential smoothing, random forest, XGBoost, LightGBM, and a Compact and an Extended configuration of TabPFN-2. Each forecast the platform's composite performance score 1, 3, 5, 15 and 30 assessment cycles ahead, roughly one week to six months. An expanding-window design meant that every forecast used only information available at its origin, and all procedures were scored on the same users and target observations. Point error was measured as mean absolute error, prediction intervals by empirical coverage and width, and the full predictive distribution by the continuous ranked probability score.

{% include figure.html src="/assets/img/projects/cognitive-forecasting/rolling-origin-protocol.png" width="1600" height="735" alt="Diagram of the expanding-window rolling-origin protocol: for horizons of 1, 3, 5, 15 and 30 cycles, a bar shows the history available at the forecast origin, a grey segment the forecast horizon, and a circle the held-out target." caption="Expanding-window rolling-origin protocol. Each row shows the first valid forecast for one horizon: the history available at the origin, the forecast horizon and the held-out target. From my MSc thesis (2026), Figure 2.3." %}

## What I found

The strongest models converged to almost the same point error, but their uncertainty estimates differed clearly. TabPFN-2 stayed close to the target coverage without any training or tuning on this data. Point accuracy alone could not distinguish good models; a pretrained foundation model competed with tuned models.

## Outputs

- Bayındır, E., Arslan, S. Ş., & Atam, E. Point Accuracy Saturation and Calibrated Uncertainty in Longitudinal Digital Cognitive Forecasting. *IEEE Journal of Biomedical and Health Informatics*. <span class="muted">Under review</span>
- MSc thesis: *Trend and Anomaly Detection in Repeated Cognitive Assessments for Early Dementia Prevention*, Boğaziçi University, 2026.
