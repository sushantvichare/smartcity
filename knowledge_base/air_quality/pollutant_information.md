# Pollutant Information

## PM2.5

PM2.5 refers to fine particulate matter with an aerodynamic diameter of
2.5 micrometers or smaller.

Possible sources include combustion processes, vehicle emissions,
industrial activity, construction activity, and other sources depending
on the location.

## PM10

PM10 refers to particulate matter with an aerodynamic diameter of 10
micrometers or smaller.

Sources can include road dust, construction activity, industrial
processes, and combustion.

## Nitrogen Dioxide (NO2)

NO2 is commonly associated with combustion processes, including vehicle
and industrial emissions.

Traffic-heavy areas can have elevated NO2 under suitable conditions, but
the chatbot should rely on measured data when making location-specific
statements.

## Sulfur Dioxide (SO2)

SO2 can be associated with combustion of sulfur-containing fuels and
certain industrial processes.

## Carbon Monoxide (CO)

CO is a pollutant produced by incomplete combustion. Road traffic can be
an important source in some environments.

## Ozone (O3)

Ground-level ozone can form through atmospheric chemical reactions
involving precursor pollutants and sunlight.

## Using Pollutant Data in the Chatbot

When a user asks why AQI is high, the assistant should:

1.  Check which pollutant fields exist in the dataset.
2.  Identify the pollutant values or model features that are actually
    available.
3.  Use the model or data analysis to support the explanation.
4.  Avoid claiming causation from correlation alone.

If a pollutant is not present in the dataset, the assistant should say
that the available data does not contain that pollutant rather than
inventing a value.
