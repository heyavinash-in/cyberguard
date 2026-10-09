# Account Takeover Implementation Guide

## What the Scenario Detects
The scenario detects if current authentication and session activity deviate significantly from a user's established historical behavioral baseline. It is meant to catch Account Takeover (ATO) through unusual environmental signals combined with threat patterns like brute-force or MFA manipulation.

## How it Works
1. **Frontend**: Collects telemetry (IP, Country, Device, Success/Fail, MFA change). Never asks for passwords.
2. **Backend**: Receives a strongly typed `AccountActivityRequest`.
3. **Baseline**: `AccountBaselineService` compares the new event against a stored synthetic baseline of "known good" behavior for that user.
4. **Features**: `AccountFeatureExtractor` maps differences into numerical/boolean values (`new_device=True`, `unusual_login_hour=True`).
5. **Rules**: `AccountRuleEngine` deterministically scores explicit anomalies and provides explainable evidence.
6. **ML**: An `IsolationForest` unsupervised model evaluates the feature vector and outputs an anomaly probability.
7. **Correlation**: `AccountRiskEngine` looks for severe combinations (e.g., Burst of Fails + New Device = 50 pt escalation).
8. **Risk Calculation**: Evidence is fused into a 0-100 risk score and capped.
9. **Explanation**: Generated dynamically based on the highest risk level.
10. **Timeline**: Chronological events are mapped for the security operator to review.
11. **Responses**: Generates actionable playbooks based on risk severity.

## Simulations
- **Normal Activity**: Sends known device, known IP, standard hour. Returns `SAFE`.
- **Takeover Attack**: Sends an unusual location, new device, VPN, MFA change, and multiple failed logins. Returns `CRITICAL`.

## Production Requirements
This hackathon prototype uses in-memory baselines. A production rollout requires integration with real IdP streams (Entra ID, Okta), historical user databases, and accurate geo/IP threat intel feeds.
