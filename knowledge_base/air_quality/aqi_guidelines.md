# Air Quality Guidelines

## Purpose

This document provides general information for explaining Air Quality
Index (AQI) predictions in the Smart City application.

## AQI

AQI is an index used to communicate air-quality conditions using a
numerical scale. The meaning of an AQI value depends on the AQI system
and standard used by the underlying data.

For this project, use the AQI category definitions documented in
`aqi_categories.md`.

## Common Pollutants

Air-quality datasets may contain measurements such as:

-   PM2.5
-   PM10
-   NO2
-   SO2
-   CO
-   O3

The exact pollutants available depend on the project's dataset.

## Interpreting Predictions

The assistant should report:

1.  Predicted AQI.
2.  AQI category.
3.  Date and location.
4.  Important model inputs when available.
5.  Relevant pollutant measurements or predictions when available.

The assistant should not claim a pollutant caused an AQI value unless
the data or model analysis supports that conclusion.

## AQI vs Pollutant Concentration

AQI is an index, while PM2.5, PM10, NO2, and other measurements
represent pollutant concentrations.

They should not be treated as interchangeable.

## Uncertainty

An ML prediction is an estimate rather than a guaranteed future
measurement.

If model uncertainty or confidence information is unavailable, the
chatbot should not invent a confidence percentage.

## Health Communication

AQI explanations should be clear and cautious. For health-related
decisions, users should consult authoritative public-health or
environmental guidance rather than relying solely on the project's
prediction model.
