# AQI Categories

## Project AQI Categories

This project uses the following AQI category interpretation:

  AQI       Category
  --------- --------------
  0-50      Good
  51-100    Satisfactory
  101-200   Moderate
  201-300   Poor
  301-400   Very Poor
  401-500   Severe

These categories correspond to the commonly used Indian AQI
classification framework. The chatbot should still identify the AQI
standard associated with the dataset when that metadata is available.

## Interpretation

### Good: 0-50

Air quality is generally considered good.

### Satisfactory: 51-100

Air quality is generally acceptable, although some pollutants may be
elevated.

### Moderate: 101-200

Air quality is at a moderate level and may be less suitable for
sensitive individuals.

### Poor: 201-300

Air quality is poor and may be associated with increased health concern.

### Very Poor: 301-400

Air quality is very poor and prolonged exposure may be a concern.

### Severe: 401-500

Air quality is severe and represents a high level of air pollution.

## Important Rule

The chatbot must not provide medical diagnosis or personalized medical
advice based solely on AQI predictions.

For a predicted AQI, clearly distinguish between:

-   predicted AQI,
-   observed AQI,
-   AQI category,
-   and general interpretation.
