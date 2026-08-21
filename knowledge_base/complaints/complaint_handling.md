# Complaint Handling

## Purpose

This document provides a general framework for explaining citizen
complaint data in the Smart City chatbot.

## Complaint Lifecycle

A typical complaint workflow can include:

1.  Complaint submitted.
2.  Complaint categorized.
3.  Complaint assigned to the relevant department.
4.  Complaint investigated.
5.  Action taken.
6.  Complaint resolved or closed.
7.  Citizen feedback recorded when available.

The actual workflow may differ depending on the municipal system
represented by the dataset.

## Useful Metrics

The chatbot can summarize:

-   Total complaints
-   Complaints by category
-   Complaints by area
-   Open complaints
-   Closed complaints
-   Average resolution time
-   Complaint volume over time
-   Satisfaction score when available

## Citizen Satisfaction

If the project contains a citizen satisfaction model, its output should
be presented as a prediction.

Example:

> The model predicts a satisfaction score of 72.

The chatbot should not state that the citizen actually gave a score of
72 unless that value exists in the source data.

## Prioritization

Complaint prioritization can consider:

-   Number of complaints
-   Severity
-   Location
-   Recency
-   Resolution time
-   Public safety implications
-   Repeated complaints

The chatbot should explain which factors were actually used by the
project's model or analysis.

## Avoiding Unsupported Claims

The assistant should never invent:

-   Complaint counts
-   Resolution times
-   Department actions
-   Citizen identities
-   Complaint outcomes

If information is unavailable, say that it is not present in the
available data.
