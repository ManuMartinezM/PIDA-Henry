import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

air_accidents = pd.read_csv('Air_Accidents.csv')
air_accidents["Date"] = pd.to_datetime(air_accidents["Date"], format="%Y-%m-%d")

# Filter the dataset for the decade groups 2002-2011 and 2012-2021 using the new columns
data_2002_2011 = air_accidents[air_accidents['2002-2011']]
data_2012_2021 = air_accidents[air_accidents['2012-2021']]

# Calculate total crew fatalities and crew on board for each decade group
crew_fatalities_2002_2011 = data_2002_2011['CrewFatalities'].sum()
total_accidents_2002_2011 = len(data_2002_2011)
crew_fatalities_2012_2021 = data_2012_2021['CrewFatalities'].sum()
total_accidents_2012_2021 = len(data_2012_2021)

# Calculate the fatality rate (percentage) for each decade group
crew_fatality_rate_2002_2011 = round((crew_fatalities_2002_2011 / total_accidents_2002_2011), 2)
crew_fatality_rate_2012_2021 = round((crew_fatalities_2012_2021 / total_accidents_2012_2021), 2)

st.title('KPI: Crew Fatality Rate Reduction by 10%')
st.markdown('***')

if st.checkbox('Crew Fatalities Per Year'):

    year_limit_1 = st.slider('Year:', 2002, 2022, 2002, key='slider_key_1')

    # Group the data by year and calculate total crew fatalities for each year
    crew_fatalities_by_year = air_accidents.groupby(air_accidents['Date'].dt.year)['CrewFatalities'].sum()

    # Create a line chart to show crew fatalities over the years
    graph_1 = plt.figure(figsize=(12, 6))
    plt.plot(crew_fatalities_by_year.index, crew_fatalities_by_year.values, marker='o', linestyle='-', color='red')
    plt.title('Crew Fatalities Per Year')
    plt.xlabel('Year')
    plt.ylabel('Total Crew Fatalities')
    plt.grid(True)
    plt.tight_layout()

    filtered_data = crew_fatalities_by_year[crew_fatalities_by_year.index <= year_limit_1]
    st.pyplot(graph_1)

if st.checkbox('Crew Fatality Rate Per Year'):

    year_limit_2 = st.slider('Year:', 2002, 2022, 2002, key='slider_key_2')

    # Group the data by year and calculate total crew fatalities and crew on board for each year
    crew_data_by_year = air_accidents.groupby(air_accidents['Date'].dt.year)[['CrewFatalities', 'CrewAboard']].sum()

    # Calculate the fatality rate (percentage) for each year
    crew_data_by_year['FatalityRate'] = round((crew_data_by_year['CrewFatalities'] / len(crew_data_by_year)), 2)

    # Create a line chart to show the fatality rate over the years
    graph_2 = plt.figure(figsize=(12, 6))
    plt.plot(crew_data_by_year.index, crew_data_by_year['FatalityRate'], marker='o', linestyle='-', color='red')
    plt.title('Crew Fatality Rate Per Year')
    plt.xlabel('Year')
    plt.ylabel('Crew Fatality Rate (%)')
    plt.grid(True)
    plt.tight_layout()

    filtered_data = crew_data_by_year[crew_data_by_year.index <= year_limit_2]
    st.pyplot(graph_2)

st.write('### Comparison between 2012-2021 and 2002-2011')

if st.checkbox('Crew Fatality Rate by Decade'):
    if st.button('2002-2011'):
        st.write(f"{crew_fatality_rate_2002_2011}%")
    if st.button('2012-2021'):
        st.write(f"{crew_fatality_rate_2012_2021}%")
    if st.button('Line Chart'):
        decades = ['2002-2011', '2012-2021']
        fatality_rates = [crew_fatality_rate_2002_2011, crew_fatality_rate_2012_2021]

        graph_3 = plt.figure(figsize=(8, 6))
        plt.plot(decades, fatality_rates, marker='o', linestyle='-', color='blue')
        plt.title('Crew Fatality Rate by Decade (2002-2011 vs. 2012-2021)')
        plt.xlabel('Decade')
        plt.ylabel('Crew Fatality Rate (%)')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(graph_3)
    
if st.checkbox('KPI Evaluation'):
    
   # Calculate the Crew Fatality Rate reduction percentage
    percentage_reduction = round(((crew_fatality_rate_2002_2011 - crew_fatality_rate_2012_2021) / crew_fatality_rate_2002_2011) * 100, 2)

    # Define the target reduction (10% reduction)
    target_reduction = 10

    # Check if the reduction meets the target
    kpi_met = percentage_reduction >= target_reduction

    st.write(f"Crew Fatality Rate Reduction: {percentage_reduction:.2f}%")
    st.write(f"KPI Met (10% Reduction Target): {kpi_met}")     