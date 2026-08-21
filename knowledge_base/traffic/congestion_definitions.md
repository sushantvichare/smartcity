# Congestion Definitions

## Project Congestion Scale

The Smart City project uses a 0-100 congestion scale for model outputs.

  Range    Category   Interpretation
  -------- ---------- ------------------------------------------------
  0-20     Very Low   Traffic is generally flowing freely
  21-40    Low        Minor traffic interaction
  41-60    Moderate   Noticeable traffic but generally manageable
  61-80    High       Significant slowdown and increased travel time
  81-100   Severe     Strong congestion and substantial slowdown

These categories are project-defined interpretation thresholds.

## Congestion and Speed

Congestion generally corresponds to reduced vehicle speed relative to
normal or free-flow conditions.

However, speed alone should not be used to determine congestion. The
assistant should consider the model's congestion output and other
available variables.

## Congestion and Vehicle Count

Higher vehicle counts can contribute to congestion when traffic demand
approaches or exceeds effective road capacity.

The relationship is not necessarily linear. A road with a high vehicle
count can sometimes maintain good traffic flow, while a lower count can
still produce delays because of incidents, signals, road restrictions,
or bottlenecks.

## Congestion and Travel Time

When congestion increases, travel time generally increases.

The Travel Time Index can help communicate this effect:

-   Around 1.0: close to free-flow travel time.
-   Above 1.0: additional travel time compared with free flow.
-   Higher values: greater delay.

## Example

If a model predicts:

-   Congestion level: 85
-   Average speed: 22 km/h
-   TTI: 2.1

The assistant can describe this as severe project-level congestion,
reduced speed, and substantially longer travel time than free-flow
conditions.

It should not state that these values represent an official government
classification.
