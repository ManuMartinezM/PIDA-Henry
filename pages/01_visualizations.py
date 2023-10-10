import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

air_accidents = pd.read_csv('Air_Accidents.csv')
air_accidents["Date"] = pd.to_datetime(air_accidents["Date"], format="%Y-%m-%d")

# Extract the year from the 'Date' column and create a new 'Year' column
air_accidents['Year'] = air_accidents['Date'].dt.year

st.title("Air Accidents")

# Create a slider for selecting the year range
year_range_air_accidents = st.slider("Select Year Range", air_accidents['Year'].min(), air_accidents['Year'].max(), (air_accidents['Year'].min(), air_accidents['Year'].max()), key='year_range_air_accidents')

# Filter data based on the selected year range
filtered_data = air_accidents[(air_accidents['Year'] >= year_range_air_accidents[0]) & (air_accidents['Year'] <= year_range_air_accidents[1])]

# Calculate total accidents, total non-military accidents, and total military accidents
total_accidents = len(filtered_data)
total_non_military = len(filtered_data[filtered_data['IsMilitary'] == False])
total_military = len(filtered_data[filtered_data['IsMilitary'] == True])

# Create an expander for the card visualizations
with st.expander("Accident Statistics"):
    # Subheader and values for total accidents
    st.subheader("Total Accidents")
    st.write(total_accidents)

    # Subheader and values for total non-military accidents
    st.subheader("Total Non-Military Accidents")
    st.write(total_non_military)

    # Subheader and values for total military accidents
    st.subheader("Total Military Accidents")
    st.write(total_military)


# Military vs. Non-Military flights pie chart

st.title('Military vs. Non-Military flights')

year_range_vs = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='year_range_vs')
filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= year_range_vs[0]) & (air_accidents['Date'].dt.year <= year_range_vs[1])]
filtered_accidents['IsMilitary'] = filtered_accidents['IsMilitary'].map({True: 'Military', False: 'Non-Military'})

military_counts = filtered_accidents['IsMilitary'].value_counts()
st.plotly_chart(px.pie(names=military_counts.index, values=military_counts, title='Military vs. Non-Military Flights'))

#Accidents Per Year

st.title('Accidents per Year')

# User input for year range
accidents_year_range = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='accidents_year_range')

# User input for accident type
accident_type = st.selectbox('Select Accident Type', ['Total', 'Non-Military', 'Military'], key='accident_type')

# Filter data based on the selected year range and accident type
if accident_type == 'Total':
    filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= accidents_year_range[0]) & (air_accidents['Date'].dt.year <= accidents_year_range[1])]
    title = 'Accidents per Year (Total)'
elif accident_type == 'Non-Military':
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['Date'].dt.year >= accidents_year_range[0]) & (air_accidents['Date'].dt.year <= accidents_year_range[1])]
    title = 'Accidents per Year (Non-Military)'
else:
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['Date'].dt.year >= accidents_year_range[0]) & (air_accidents['Date'].dt.year <= accidents_year_range[1])]
    title = 'Accidents per Year (Military)'

# Group data for accidents per year
accidents_per_year = filtered_accidents.groupby(filtered_accidents['Date'].dt.year).size()

# Create a line chart using Plotly Express
fig = px.line(x=accidents_per_year.index, y=accidents_per_year, labels={'x':'Year', 'y':'Accidents'}, title=title)

st.plotly_chart(fig)

# Fatalities per Year

st.title('Fatalities per Year')

# User input for year range
fatalities_year_range = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='fatalities_per_year')

# User input for fatalities type
fatalities_type = st.selectbox('Select Fatalities Type', ['Total', 'Non-Military', 'Military'], key='fatalities_type')

# Filter data based on the selected year range and fatalities type
if fatalities_type == 'Total':
    filtered_fatalities = air_accidents[(air_accidents['Date'].dt.year >= fatalities_year_range[0]) & (air_accidents['Date'].dt.year <= fatalities_year_range[1])]
    title = 'Fatalities per Year (Total)'
elif fatalities_type == 'Non-Military':
    filtered_fatalities = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['Date'].dt.year >= fatalities_year_range[0]) & (air_accidents['Date'].dt.year <= fatalities_year_range[1])]
    title = 'Fatalities per Year (Non-Military)'
else:
    filtered_fatalities = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['Date'].dt.year >= fatalities_year_range[0]) & (air_accidents['Date'].dt.year <= fatalities_year_range[1])]
    title = 'Fatalities per Year (Military)'

# Group data for fatalities per year
fatalities_per_year = filtered_fatalities.groupby(filtered_fatalities['Date'].dt.year)['TotalFatalities'].sum()

# Create a line chart using Plotly Express
fig = px.line(x=fatalities_per_year.index, y=fatalities_per_year, labels={'x':'Year', 'y':'Fatalities'}, title=title)

st.plotly_chart(fig)

# By Operator

st.title('Accidents by Operator')

# User input for year range
operator_year_range = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='accidents_by_operator')

# User input for accident type
accident_type = st.selectbox('Select Accident Type', ['Total', 'Non-Military', 'Military'], key='accident_type_operator')

# Default operators for the "Total" option
default_total_operators = air_accidents['Operator'].value_counts().head(10).index.tolist()

# Define an empty list to hold the selected operators
selected_operators = []

# If the selected accident type is "Total," allow the user to select operators
if accident_type == 'Total':
    selected_operators = st.multiselect("Select Operators", air_accidents['Operator'].unique(), default=default_total_operators)

# Filter data based on the selected year range, accident type, and selected operators
if accident_type == 'Total':
    filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= operator_year_range[0]) & (air_accidents['Date'].dt.year <= operator_year_range[1]) & (air_accidents['Operator'].isin(selected_operators))]
    title = 'Accidents by Operator (Total)'
elif accident_type == 'Non-Military':
    default_non_military_operators = air_accidents[air_accidents['IsMilitary'] == False]['Operator'].value_counts().head(10).index.tolist()
    selected_non_military_operators = st.multiselect("Select Non-Military Operators", air_accidents[air_accidents['IsMilitary'] == False]['Operator'].unique(), default=default_non_military_operators)
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['Date'].dt.year >= operator_year_range[0]) & (air_accidents['Date'].dt.year <= operator_year_range[1])]
    filtered_accidents = filtered_accidents[filtered_accidents['Operator'].isin(selected_non_military_operators)]
    title = 'Accidents by Operator (Non-Military)'
else:
    default_military_operators = air_accidents[air_accidents['IsMilitary'] == True]['Operator'].value_counts().head(10).index.tolist()
    selected_military_operators = st.multiselect("Select Military Operators", air_accidents[air_accidents['IsMilitary'] == True]['Operator'].unique(), default=default_military_operators)
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['Date'].dt.year >= operator_year_range[0]) & (air_accidents['Date'].dt.year <= operator_year_range[1])]
    filtered_accidents = filtered_accidents[filtered_accidents['Operator'].isin(selected_military_operators)]
    title = 'Accidents by Operator (Military)'

# Group data for accidents by operator
operator_counts = filtered_accidents['Operator'].value_counts().head(10).reset_index()
operator_counts.columns = ['Operator', 'Accidents']

# Create a bar chart using Plotly Express
fig = px.bar(operator_counts, x='Operator', y='Accidents', labels={'x':'Operator', 'y':'Accidents'}, title=title)

st.plotly_chart(fig)

# By Country

st.title('Accidents by Country')

# User input for year range
country_year_range = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='accidents_by_country')

# User input for accident type
accident_type = st.selectbox('Select Accident Type', ['Total', 'Non-Military', 'Military'], key='accident_type_country')

# Default countries for the "Total" option
default_total_countries = air_accidents['LocationCountry'].value_counts().head(10).index.tolist()

# Define an empty list to hold the selected countries
selected_countries = []

# If the selected accident type is "Total," allow the user to select countries
if accident_type == 'Total':
    selected_countries = st.multiselect("Select Countries", air_accidents['LocationCountry'].unique(), default=default_total_countries)

# Filter data based on the selected year range, accident type, and selected countries
if accident_type == 'Total':
    filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= country_year_range[0]) & (air_accidents['Date'].dt.year <= country_year_range[1]) & (air_accidents['LocationCountry'].isin(selected_countries))]
    title = 'Accidents by Country (Total)'
elif accident_type == 'Non-Military':
    default_non_military_countries = air_accidents[air_accidents['IsMilitary'] == False]['LocationCountry'].value_counts().head(10).index.tolist()
    selected_non_military_countries = st.multiselect("Select Non-Military Countries", air_accidents[air_accidents['IsMilitary'] == False]['LocationCountry'].unique(), default=default_non_military_countries)
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['LocationCountry'].isin(selected_non_military_countries))]
    filtered_accidents = filtered_accidents[(filtered_accidents['Date'].dt.year >= country_year_range[0]) & (filtered_accidents['Date'].dt.year <= country_year_range[1])]
    title = 'Accidents by Country (Non-Military)'
else:
    default_military_countries = air_accidents[air_accidents['IsMilitary'] == True]['LocationCountry'].value_counts().head(10).index.tolist()
    selected_military_countries = st.multiselect("Select Military Countries", air_accidents[air_accidents['IsMilitary'] == True]['LocationCountry'].unique(), default=default_military_countries)
    filtered_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['LocationCountry'].isin(selected_military_countries))]
    filtered_accidents = filtered_accidents[(filtered_accidents['Date'].dt.year >= country_year_range[0]) & (filtered_accidents['Date'].dt.year <= country_year_range[1])]
    title = 'Accidents by Country (Military)'

# Group data for accidents by country
country_counts = filtered_accidents['LocationCountry'].value_counts().head(10).reset_index()
country_counts.columns = ['Country', 'Accidents']

# Create a bar chart using Plotly Express
fig = px.bar(country_counts, x='Country', y='Accidents', labels={'x':'Country', 'y':'Accidents'}, title=title)

st.plotly_chart(fig)

# Fatalities vs. Survivors

st.title('Fatalities vs. Survivors')

# User input for year range
year_range_fatalities_vs_survivors = st.slider('Select a year range', air_accidents['Date'].dt.year.min(), air_accidents['Date'].dt.year.max(), (2002, 2021), key='fatalities_vs_survivors')

# User input for comparison type
comparison_type = st.selectbox('Select comparison type', ['Total', 'Passenger', 'Crew'], key='comparison_type')

# User input for flight type
flight_type = st.selectbox('Select flight type', ['Total', 'Military', 'Non-Military'], key='flight_type')

# Filter data based on the selected year range, comparison type, and flight type
if comparison_type == 'Total':
    filtered_data = air_accidents[(air_accidents['Date'].dt.year >= year_range_fatalities_vs_survivors[0]) & (air_accidents['Date'].dt.year <= year_range_fatalities_vs_survivors[1])]
    title = 'Total Fatalities vs. Total Survivors'
elif comparison_type == 'Passenger':
    filtered_data = air_accidents[(air_accidents['Date'].dt.year >= year_range_fatalities_vs_survivors[0]) & (air_accidents['Date'].dt.year <= year_range_fatalities_vs_survivors[1]) & (air_accidents['IsMilitary'] == False)]
    title = 'Non-Military Fatalities vs. Survivors'
elif comparison_type == 'Crew':
    filtered_data = air_accidents[(air_accidents['Date'].dt.year >= year_range_fatalities_vs_survivors[0]) & (air_accidents['Date'].dt.year <= year_range_fatalities_vs_survivors[1]) & (air_accidents['IsMilitary'] == True)]
    title = 'Military Fatalities vs. Survivors'

# User input for operator (if applicable)
if 'Operator' in filtered_data.columns:
    selected_operators = st.multiselect('Select Operator(s)', filtered_data['Operator'].unique(), key='selected_operators')
    if selected_operators:
        filtered_data = filtered_data[filtered_data['Operator'].isin(selected_operators)]
        title += f' for Operator(s): {", ".join(selected_operators)}'

# User input for country (if applicable)
if 'LocationCountry' in filtered_data.columns:
    selected_countries = st.multiselect('Select Country(s)', filtered_data['LocationCountry'].unique(), key='selected_countries')
    if selected_countries:
        filtered_data = filtered_data[filtered_data['LocationCountry'].isin(selected_countries)]
        title += f' for Country(s): {", ".join(selected_countries)}'

# Filter data by flight type
if flight_type == 'Military':
    filtered_data = filtered_data[filtered_data['IsMilitary'] == True]
    title += ' (Military)'
elif flight_type == 'Non-Military':
    filtered_data = filtered_data[filtered_data['IsMilitary'] == False]
    title += ' (Non-Military)'

# Define default values for passengers' fatalities and calculate survivors
passenger_fatalities_column = 'PassengerFatalities'
passenger_survivors_column = 'PassengerSurvivors'

if passenger_fatalities_column not in filtered_data.columns:
    st.error("Passenger fatalities column not found in the dataset.")
else:
    if passenger_survivors_column not in filtered_data.columns:
        # Calculate passenger survivors as the difference between PassengersAboard and PassengerFatalities
        filtered_data['PassengerSurvivors'] = filtered_data['PassengersAboard'] - filtered_data[passenger_fatalities_column]

# Group data for total fatalities and survivors based on comparison type
fatalities_column = 'TotalFatalities'
survivors_column = 'Survived'

total_fatalities = filtered_data[fatalities_column].sum()
total_survivors = filtered_data[survivors_column].sum()

# Create a DataFrame for the donut chart
data = {
    'Group': ['Fatalities', 'Survivors'],
    'Value': [total_fatalities, total_survivors]
}
donut_df = pd.DataFrame(data)

# Create a donut chart using Plotly Express
fig = px.pie(
    donut_df,
    names='Group',
    values='Value',
    hole=0.4,  # Set the size of the hole to create a donut chart
    title=title,
    labels={'Value': 'Count'}
)

# Display the chart in the Streamlit app
st.plotly_chart(fig)

