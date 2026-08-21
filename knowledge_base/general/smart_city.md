# Smart City Intelligence Platform

## Purpose

The Smart City AI Assistant combines machine-learning predictions,
historical datasets, and a retrieval-augmented knowledge base.

The system can support questions about:

-   Traffic
-   Air quality
-   Citizen complaints
-   Citizen satisfaction
-   Other models added by the project

## System Components

### Machine Learning Models

ML models generate predictions from structured data.

Examples in the project include:

-   Traffic congestion prediction
-   AQI prediction
-   Citizen satisfaction prediction

A model prediction should always be identified as a prediction.

### Retrieval-Augmented Generation

RAG retrieves relevant information from the project's knowledge base
before generating an answer.

The retrieved content provides context and definitions but does not
replace the ML model.

### AI Agent

The agent determines which resources are needed for a question.

For example:

> What is the predicted traffic condition in Andheri?

The agent may call the traffic prediction tool.

For:

> What does severe congestion mean?

The agent can retrieve traffic documentation without running a
prediction model.

For:

> Compare traffic and AQI conditions.

The agent may use both traffic and AQI tools and then retrieve relevant
documentation.

## Answer Structure

For prediction questions, the assistant should preferably provide:

1.  Prediction.
2.  Relevant input or location.
3.  Category or interpretation.
4.  Supporting context from RAG.
5.  Important limitations.

## Source Priority

When information conflicts, prefer sources in this order:

1.  Direct model output for predictions.
2.  Project dataset for historical observations.
3.  Project knowledge-base documents.
4.  General language-model knowledge.

## Hallucination Prevention

The chatbot should not invent:

-   Model predictions
-   Dataset values
-   Dates
-   Locations
-   Complaint statistics
-   AQI measurements
-   Traffic measurements
-   Model confidence
-   Sources that were not retrieved

If the system does not have enough information, it should say so.

## Multi-Model Questions

For questions requiring multiple domains, the agent can call multiple
tools.

Example:

> Which area has both the highest predicted traffic congestion and
> highest predicted AQI?

The system can:

1.  Generate traffic predictions.
2.  Generate AQI predictions.
3.  Compare the outputs.
4.  Retrieve relevant definitions.
5.  Explain the result.

## Model Transparency

When practical, answers should identify the model or data source used.

Example:

> Source: Traffic Prediction Model

or

> Source: AQI Prediction Model + Air Quality Knowledge Base

## Important Limitation

The Smart City assistant is a decision-support system. Its predictions
should not be presented as guaranteed future outcomes or as official
municipal decisions.
