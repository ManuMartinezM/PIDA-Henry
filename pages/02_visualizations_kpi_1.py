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

st.title("Crew Fatality Rate Reduction by 10% in the Last Decade")

# Create a slider for selecting the year range
year_range = st.slider("Select Year Range", min_value=air_accidents['Date'].dt.year.min(), max_value=air_accidents['Date'].dt.year.max(), value=(2002, 2021))

# Filter the DataFrame based on the selected year range
filtered_df = air_accidents[(air_accidents['Date'].dt.year >= year_range[0]) & (air_accidents['Date'].dt.year <= year_range[1])]

# Calculate Crew Fatalities per year
crew_fatalities_per_year = filtered_df.groupby(filtered_df['Date'].dt.year)['CrewFatalities'].sum()

# Calculate Crew Fatality Rate per year
crew_fatality_rate_per_year = round(crew_fatalities_per_year / len(filtered_df), 2)

# Calculate Crew Fatalities for the decades 2002-2011 and 2012-2021
crew_fatalities_decade_1 = filtered_df[filtered_df['2002-2011']]['CrewFatalities'].sum()
crew_fatalities_decade_2 = filtered_df[filtered_df['2012-2021']]['CrewFatalities'].sum()

# Calculate Crew Fatality Rate for the decades 2002-2011 and 2012-2021
crew_fatality_rate_decade_1 = crew_fatalities_decade_1 / len(filtered_df[filtered_df['2002-2011']])
crew_fatality_rate_decade_2 = crew_fatalities_decade_2 / len(filtered_df[filtered_df['2012-2021']])

# Calculate the KPI result for the decades
kpi_result = ((crew_fatality_rate_decade_2 - crew_fatality_rate_decade_1) / crew_fatality_rate_decade_1) * 100

# Display a banner or a text box with the KPI result
if kpi_result <= -10:
    st.success("KPI Achieved: Crew Fatality Rate Reduced by {}%".format(abs(round(kpi_result, 2))))
else:
    st.error("KPI Not Achieved: Crew Fatality Rate Increased by {}%".format(round(kpi_result, 2)))

# Create Crew Fatalities per year plot
fig1 = go.Figure(data=[
    go.Bar(x=crew_fatalities_per_year.index, y=crew_fatalities_per_year.values, text=crew_fatalities_per_year.values, textposition='auto')
])
fig1.update_layout(title='Crew Fatalities per Year', xaxis_title='Year', yaxis_title='Crew Fatalities')
st.plotly_chart(fig1)

# Create Crew Fatality Rate per year plot
fig2 = go.Figure(data=[
    go.Bar(x=crew_fatality_rate_per_year.index, y=crew_fatality_rate_per_year.values, text=crew_fatality_rate_per_year.values, textposition='auto')
])
fig2.update_layout(title='Crew Fatality Rate per Year', xaxis_title='Year', yaxis_title='Crew Fatality Rate (%)')
st.plotly_chart(fig2)

# Create Crew Fatality Rate per decade plot
fig3 = go.Figure(data=[
    go.Bar(x=['2002-2011', '2012-2021'], y=[crew_fatality_rate_decade_1, crew_fatality_rate_decade_2], text=[round(crew_fatality_rate_decade_1, 2), round(crew_fatality_rate_decade_2, 2)], textposition='auto')
])
fig3.update_layout(title='Crew Fatality Rate per Decade', xaxis_title='Decade', yaxis_title='Crew Fatality Rate (%)')
st.plotly_chart(fig3)

# Create a line chart to show the change in crew fatality rate
fig4 = go.Figure(data=[
    go.Scatter(x=crew_fatality_rate_per_year.index, y=crew_fatality_rate_per_year.values, mode='lines+markers', line=dict(width=2)),
])

fig4.update_layout(title='Change in Crew Fatality Rate Over Time', xaxis_title='Year', yaxis_title='Crew Fatality Rate (%)')

# Highlight the KPI period (2002-2011 vs. 2012-2021) with a shaded area
fig4.add_shape(
    go.layout.Shape(
        type='rect',
        x0=2002,
        x1=2011,
        y0=crew_fatality_rate_per_year.min(),
        y1=crew_fatality_rate_per_year.max(),
        fillcolor='rgba(0, 0, 255, 0.2)',  # Blue shading
        opacity=0.3,
        layer='below',
        line=dict(width=0),
    )
)
fig4.add_shape(
    go.layout.Shape(
        type='rect',
        x0=2012,
        x1=2021,
        y0=crew_fatality_rate_per_year.min(),
        y1=crew_fatality_rate_per_year.max(),
        fillcolor='rgba(255, 0, 0, 0.2)',  # Red shading
        opacity=0.3,
        layer='below',
        line=dict(width=0),
    )
)

st.plotly_chart(fig4)