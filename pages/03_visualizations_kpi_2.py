import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

air_accidents = pd.read_csv('Air_Accidents.csv')
air_accidents["Date"] = pd.to_datetime(air_accidents["Date"], format="%Y-%m-%d")

st.title('KPI: Hijacking incidents reduction by 10%')
st.markdown('***')

# Count the total number of aviation accidents involving hijacked planes
air_accidents['Hijack'] = air_accidents['Summary'].str.contains('hijack', case=False)
total_accidents_involving_hijack = air_accidents['Hijack'].sum()

# Extract the year and create a new 'Year' column
air_accidents['Year'] = air_accidents['Date'].dt.year

# Filter the dataset to include only hijack incidents
hijack_incidents = air_accidents[air_accidents['Hijack']]

# Group by year and count the number of hijack incidents
hijack_incidents_by_year = hijack_incidents.groupby('Year')['Hijack'].count()

air_accidents['Year'] = air_accidents['Date'].dt.year
air_accidents['Decade'] = (air_accidents['Date'].dt.year // 10) * 10

# Count the total number of incidents for each decade
hijack_incidents_by_decade = hijack_incidents.groupby(air_accidents['Decade']).size()

# Hijack incidents by operator
hijacking_operators = hijack_incidents['Operator'].value_counts()

total_accidents_by_decade = air_accidents.groupby(air_accidents['Decade']).size()

# Calculate the Hijacking Incident Rate for each decade
hijacking_incident_rate_by_decade = (hijack_incidents_by_decade / total_accidents_by_decade) * 100

if st.checkbox('Total number of hijacking incidents'):
    st.write(total_accidents_involving_hijack)

if st.checkbox('Hijack incidents Per Year'):
    graph_1 = plt.figure(figsize=(12, 6))
    hijack_incidents_by_year.plot(kind='bar', color='skyblue')
    plt.title('Number of Hijack Incidents by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Incidents')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(graph_1)

if st.checkbox('Hijack incidents Per Decade'):
    graph_2 = plt.figure(figsize=(12, 6))
    hijack_incidents_by_decade.plot(kind='bar', color='skyblue')
    plt.title('Number of Hijack Incidents by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Number of Incidents')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(graph_2)
    
if st.checkbox('Hijack incidents per operator'):
    pivot_table = hijack_incidents.pivot_table(index='Year', columns='Operator', aggfunc='size', fill_value=0)
    
    graph_3 = plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5, cbar=True)
    plt.title('Hijacking Incidents by Year and Operator')
    plt.xlabel('Operator')
    plt.ylabel('Year')
    plt.tight_layout()
    st.pyplot(graph_3)

if st.checkbox('Hijack incident rate by decade'):
    graph_4 = plt.figure(figsize=(12, 6))
    plt.plot(hijacking_incident_rate_by_decade.index, hijacking_incident_rate_by_decade.values, marker='o', linestyle='-', color='red')
    plt.title('Hijacking Incident Rate by Decade (1970s to Present)')
    plt.xlabel('Decade')
    plt.ylabel('Hijacking Incident Rate (%)')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(graph_4)

