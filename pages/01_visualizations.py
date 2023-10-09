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

# Accidents per year

accidents_year_range = st.slider("Select Year Range for Accidents", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)))
filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= accidents_year_range[0]) & (air_accidents['Date'].dt.year <= accidents_year_range[1])]

accidents_per_year = filtered_accidents.groupby('Date').size().resample('Y').sum()
st.plotly_chart(px.line(x=accidents_per_year.index, y=accidents_per_year, labels={'x':'Year', 'y':'Accidents'}, title='Accidents per Year'))

# Fatalities per year

fatalities_year_range = st.slider("Select Year Range for Fatalities", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)))
filtered_fatalities = air_accidents[(air_accidents['Date'].dt.year >= fatalities_year_range[0]) & (air_accidents['Date'].dt.year <= fatalities_year_range[1])]

fatalities_per_year = filtered_fatalities.groupby('Date')['TotalFatalities'].sum().resample('Y').sum()
st.plotly_chart(px.line(x=fatalities_per_year.index, y=fatalities_per_year, labels={'x':'Year', 'y':'Fatalities'}, title='Fatalities per Year'))

# Military vs. Non-Military flights pie chart

year_range_vs = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)))
filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= year_range_vs[0]) & (air_accidents['Date'].dt.year <= year_range_vs[1])]
filtered_accidents['IsMilitary'] = filtered_accidents['IsMilitary'].map({True: 'Military', False: 'Non-Military'})

military_counts = filtered_accidents['IsMilitary'].value_counts()
st.plotly_chart(px.pie(names=military_counts.index, values=military_counts, title='Military vs. Non-Military Flights'))

# Accidents per year (Non-Military)

non_military_accidents_year_range = st.slider("Select Year Range for Non-Military Accidents", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)))
filtered_non_military_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['Date'].dt.year >= non_military_accidents_year_range[0]) & (air_accidents['Date'].dt.year <= non_military_accidents_year_range[1])]

non_military_accidents_per_year = filtered_non_military_accidents.groupby('Date').size().resample('Y').sum()
st.plotly_chart(px.line(x=non_military_accidents_per_year.index, y=non_military_accidents_per_year, labels={'x':'Year', 'y':'Non-Military Accidents'}, title='Accidents per Year (Non-Military)'))

# Accidents per year (Military)

military_accidents_year_range = st.slider("Select Year Range for Military Accidents", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)))
filtered_military_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['Date'].dt.year >= military_accidents_year_range[0]) & (air_accidents['Date'].dt.year <= military_accidents_year_range[1])]

military_accidents_per_year = filtered_military_accidents.groupby('Date').size().resample('Y').sum()
st.plotly_chart(px.line(x=military_accidents_per_year.index, y=military_accidents_per_year, labels={'x':'Year', 'y':'Military Accidents'}, title='Accidents per Year (Military)'))

# Survivors vs. Fatalities (Military and Non-Military)

year_range = st.slider("Select Year Range", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='survivors_vs_fatalities')
filtered_accidents = air_accidents[(air_accidents['Date'].dt.year >= year_range[0]) & (air_accidents['Date'].dt.year <= year_range[1])]
filtered_accidents['IsMilitaryLabel'] = filtered_accidents['IsMilitary'].replace({True: 'Military', False: 'Non-Military'})

survivors_vs_fatalities = filtered_accidents.groupby('IsMilitaryLabel')[['Survived', 'TotalFatalities']].sum().reset_index()
st.plotly_chart(px.bar(survivors_vs_fatalities, x='IsMilitaryLabel', y=['Survived', 'TotalFatalities'], labels={'IsMilitaryLabel':'Military vs. Non-Military', 'value':'Count'}, title='Survivors vs. Fatalities'))

# Accidents by Operator (Non-Military)

year_range_non_military = st.slider("Select Year Range (Non-Military)", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='accidents_by_operator')

default_non_military_operators = air_accidents[air_accidents['IsMilitary'] == False]['Operator'].value_counts().head(10).index.tolist()
selected_non_military_operators = st.multiselect("Select Non-Military Operators", air_accidents[air_accidents['IsMilitary'] == False]['Operator'].unique(), default=default_non_military_operators)
filtered_non_military_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['Date'].dt.year >= year_range_non_military[0]) & (air_accidents['Date'].dt.year <= year_range_non_military[1])]
filtered_non_military_accidents = filtered_non_military_accidents[filtered_non_military_accidents['Operator'].isin(selected_non_military_operators)]

non_military_operators = filtered_non_military_accidents['Operator'].value_counts().head(10).reset_index()
non_military_operators.columns = ['Operator', 'Accidents']

st.plotly_chart(px.bar(non_military_operators, x='Operator', y='Accidents', labels={'x':'Operator', 'y':'Accidents'}, title='Accidents by Operator (Non-Military)'))

# Accidents by Operator (Military)

year_range_military = st.slider("Select Year Range (Military)", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='accidents_by_operator_military')

default_military_operators = air_accidents[air_accidents['IsMilitary'] == True]['Operator'].value_counts().head(10).index.tolist()
selected_military_operators = st.multiselect("Select Military Operators", air_accidents[air_accidents['IsMilitary'] == True]['Operator'].unique(), default=default_military_operators)
filtered_military_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['Date'].dt.year >= year_range_military[0]) & (air_accidents['Date'].dt.year <= year_range_military[1])]
filtered_military_accidents = filtered_military_accidents[filtered_military_accidents['Operator'].isin(selected_military_operators)]

military_operators = filtered_military_accidents['Operator'].value_counts().head(10).reset_index()
military_operators.columns = ['Operator', 'Accidents']

st.plotly_chart(px.bar(military_operators, x='Operator', y='Accidents', labels={'x':'Operator', 'y':'Accidents'}, title='Accidents by Operator (Military)'))

# Accidents by Country (Non-Military)

year_range_non_military = st.slider("Select Year Range (Non-Military)", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='year_range_non_military')
default_non_military_countries = air_accidents[air_accidents['IsMilitary'] == False]['LocationCountry'].value_counts().head(10).index.tolist()
selected_non_military_countries = st.multiselect("Select Non-Military Countries", air_accidents[air_accidents['IsMilitary'] == False]['LocationCountry'].unique(), default=default_non_military_countries)
filtered_non_military_accidents = air_accidents[(air_accidents['IsMilitary'] == False) & (air_accidents['LocationCountry'].isin(selected_non_military_countries))]
filtered_non_military_accidents = filtered_non_military_accidents[(filtered_non_military_accidents['Date'].dt.year >= year_range_non_military[0]) & (filtered_non_military_accidents['Date'].dt.year <= year_range_non_military[1])]

non_military_countries = filtered_non_military_accidents['LocationCountry'].value_counts().head(10).reset_index()
non_military_countries.columns = ['Country', 'Accidents']

st.plotly_chart(px.bar(non_military_countries, x='Country', y='Accidents', labels={'x':'Country', 'y':'Accidents'}, title='Accidents by Country (Non-Military)'))

# Accidents by Country (Military)

year_range_military = st.slider("Select Year Range (Military)", min_value=int(air_accidents['Date'].min().year), max_value=int(air_accidents['Date'].max().year), value=(int(air_accidents['Date'].min().year), int(air_accidents['Date'].max().year)), key='year_range_military')
default_military_countries = air_accidents[air_accidents['IsMilitary'] == True]['LocationCountry'].value_counts().head(10).index.tolist()
selected_military_countries = st.multiselect("Select Military Countries", air_accidents[air_accidents['IsMilitary'] == True]['LocationCountry'].unique(), default=default_military_countries)
filtered_military_accidents = air_accidents[(air_accidents['IsMilitary'] == True) & (air_accidents['LocationCountry'].isin(selected_military_countries))]
filtered_military_accidents = filtered_military_accidents[(filtered_military_accidents['Date'].dt.year >= year_range_military[0]) & (filtered_military_accidents['Date'].dt.year <= year_range_military[1])]

military_countries = filtered_military_accidents['LocationCountry'].value_counts().head(10).reset_index()
military_countries.columns = ['Country', 'Accidents']

st.plotly_chart(px.bar(military_countries, x='Country', y='Accidents', labels={'x':'Country', 'y':'Accidents'}, title='Accidents by Country (Military)'))


