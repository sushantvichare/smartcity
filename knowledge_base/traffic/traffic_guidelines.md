# Traffic Guidelines

## Purpose

This document provides general traffic concepts for the Smart City RAG
assistant. It is intended to help the assistant explain traffic
predictions, congestion, vehicle flow, speed, and travel-time
indicators.

## Key Traffic Indicators

### Average Speed

Average speed is the mean speed of vehicles observed on a road segment
during a specified period.

-   Higher average speed generally indicates smoother traffic flow.
-   Lower average speed generally indicates slower or congested traffic.
-   Average speed should be interpreted together with vehicle count and
    road characteristics.

### Vehicle Count

Vehicle count represents the number of vehicles observed during a
defined time interval.

A high vehicle count does not automatically mean severe congestion. Road
capacity, traffic signals, incidents, weather, road works, and other
factors also influence congestion.

### Congestion Level

For this project, congestion level is represented on a 0-100 scale:

-   0-20: Very Low
-   21-40: Low
-   41-60: Moderate
-   61-80: High
-   81-100: Severe

These thresholds are project-level interpretation rules and should not
be presented as an official government traffic classification.

### Travel Time Index

Travel Time Index (TTI) compares the observed or predicted travel time
with a reference free-flow travel time.

TTI = Travel Time Under Current Conditions / Free-Flow Travel Time

A TTI of 1.0 means travel time is approximately equal to free-flow
travel time. Higher values indicate additional travel time.

## Peak Periods

Traffic conditions commonly vary by time of day. Morning and evening
commuting periods can have higher traffic demand than off-peak periods.

The chatbot should use the project's historical data when making
location-specific claims.

## Traffic Incidents

Accidents, road works, flooding, public events, vehicle breakdowns, and
temporary road closures can affect traffic conditions.

If incident information is unavailable, the chatbot should not claim
that a particular incident caused congestion.

## How the AI Assistant Should Explain Traffic Predictions

When reporting a traffic prediction, include:

1.  Predicted congestion level.
2.  Average predicted speed when available.
3.  Travel Time Index when available.
4.  Location and prediction time.
5.  Important model inputs.
6.  A clear explanation of the project-level congestion category.

The assistant should distinguish between model predictions and factual
observations.
