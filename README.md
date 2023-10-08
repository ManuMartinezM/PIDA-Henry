# AIR ACCIDENTS ANALYSIS PROJECT - PIDA
### MANUEL MARTINEZ MARGALEF

![Cover Image](cover_image.jpg)

## Overview
This project focuses on analyzing airplane accidents from 1908 to the present day. The primary objective is to gain insights into the trends, causes, and safety improvements in aviation over the years. The dataset used for this analysis, named 'air_accidents,' contains information about accidents, including date, location, operator, aircraft details, fatalities, and more.

## Dataset
The 'air_accidents' dataset contains 5008 rows and includes the following columns:

* Date: Date of the accident
* DeclaredTime: Time of the accident
* Location: Location of the accident
* Operator: Airline/Military Delegation of the aircraft
* FlightNumber:
* Route: Route taken by the airplane
* Aircraft: Plane model
* Registration: 
* CN_LN
* TotalOnBoard: Number of people on board
* PassengersAboard: Total passengers on board
* CrewAboard: Total Crew on board
* Fatalities: Number of lethal outcomes
* PassengerFatalities: Number of lethal outcomes (just passengers)
* CrewFatalities: Number of lethal outcomes (just crew)
* Ground: Total people killed due to crash on the ground (for example, those who were not on board, but died due to the crash)
* Summary: Brief summary of the case
* TotalFatalities: Sum of all the casualties
* Survived: Number of survivors
* SurvivalRate: Survival Rate
* IsMilitary: Military or non-military
* LocationCountry: Country extracted from Location

## Exploratory Data Analysis (EDA)
During the EDA phase, several visualizations and key performance indicators (KPIs) were developed:

1) Total Accidents per Year: Visualized the number of accidents over the years to identify any trends.

![accidents per year](Project%20Images/accidents_per_year.png)

2) Fatalities per Year: Analyzed the fatalities in accidents to understand changes in aviation safety.

![fatalities per year](Project%20Images/fatalities_per_year.png)

3) Distribution of Military vs. Non-Military Accidents: Examined the proportion of accidents involving military aircraft.

![military vs nonmilitary](Project%20Images/military_vs_nonmilitary_pie.png)

4) Operators with Most Accidents: Identified operators with the highest number of accidents.

![operators nonmilitary](Project%20Images/top20_accidents_by_operator.png)

![operators military](Project%20Images/top20_accidents_by_operator_military.png)

5) Countries with Most Accidents: Determined the countries where accidents were most frequent.

![countries nonmilitary](Project%20Images/top20_countries_most_accidents.png)
![countries nonmilitary](Project%20Images/top20_countries_most_accidents_military.png)

## Key Performance Indicators (KPIs)
### Crew Fatality Rate Reduction by 10% in the Last Decade

![crew fatality rate per year](Project%20Images/crew_fatality_rates_per_year.png)

The analysis revealed that the crew fatality rate reduced by 3.18% between the 2002-2011 and 2012-2021 decades.

![crew fatality rate per decade](Project%20Images/crew_fatality_rate_by_decade.png)

However, the rate increased by 3.75% between 2012 and 2021, resulting in a 17.92% increase over the last decade compared to the previous one. This indicates that the KPI was not met.
### Reduction of Hijacking Incidents in Aviation Accidents by 10% in the Last Decade

![hijack incidents per year](Project%20Images/hijack_incidents_per_year.png)

![hijack incidents per decade](Project%20Images/hijack_incidents_per_decade.png)

![hijack incidents per year](Project%20Images/hijack_incidents_per_year_per_operator.png)

The hijacking rate in the total airplane accidents for the 2000s decade was 1.18%, primarily due to the 9/11 terrorist attacks.
Encouragingly, the hijacking rate dropped to 0% during the 2010s decade, meeting the KPI of reducing hijacking incidents by 10%.

![hijack incident rate per decade](Project%20Images/hijacking_incident_rate_per_decade.png)


## Conclusion
This project provides valuable insights into the history of airplane accidents, with a focus on safety improvements and trends over the years. The analysis of KPIs demonstrates both successes and challenges in aviation safety, emphasizing the importance of continuous efforts to enhance crew safety and mitigate security threats.