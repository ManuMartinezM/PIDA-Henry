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

st.title('KPI: Hijacking incidents reduction by 10%')
st.markdown('***')

# Filter the DataFrame for the two decades (2000-2009 and 2010-2019)
decade_1_start = 2000
decade_1_end = 2009
decade_2_start = 2010
decade_2_end = 2019

filtered_df_decade_1 = air_accidents[(air_accidents['Date'].dt.year >= decade_1_start) & (air_accidents['Date'].dt.year <= decade_1_end)]
filtered_df_decade_2 = air_accidents[(air_accidents['Date'].dt.year >= decade_2_start) & (air_accidents['Date'].dt.year <= decade_2_end)]

# Define keywords or phrases indicating hijacking incidents
hijacking_keywords = ["hijack", "hijacking"]

# Count hijacking incidents for each decade
hijacking_incidents_decade_1 = len(filtered_df_decade_1[filtered_df_decade_1['Summary'].str.contains('|'.join(hijacking_keywords), case=False, na=False)])
hijacking_incidents_decade_2 = len(filtered_df_decade_2[filtered_df_decade_2['Summary'].str.contains('|'.join(hijacking_keywords), case=False, na=False)])

# Calculate the KPI result for the decades
kpi_result = (hijacking_incidents_decade_1 - hijacking_incidents_decade_2) / hijacking_incidents_decade_1 * 100

# Display a banner or a text box with the KPI result
if kpi_result >= -10:
    st.success("KPI Achieved: Hijacking Incidents Reduced by {}%".format(abs(round(kpi_result, 2))))
else:
    st.error("KPI Not Achieved: Hijacking Incidents Increased by {}%".format(round(kpi_result, 2)))

# Create a bar chart to visualize hijacking incidents for each decade
fig = px.bar(
    x=[f"{decade_1_start}-{decade_1_end}", f"{decade_2_start}-{decade_2_end}"],
    y=[hijacking_incidents_decade_1, hijacking_incidents_decade_2],
    labels={'x': 'Decade', 'y': 'Hijacking Incidents'},
    title='Hijacking Incidents Comparison'
)

st.plotly_chart(fig)

st.write("The hijacking incident rate for the 2010-2019 decade is zero. This significant reduction can be attributed to improved security measures and global efforts to prevent hijacking incidents in the aviation industry during this period.")

# Filter the dataset to include only rows with hijacking incidents
hijacking_incidents_df = air_accidents[air_accidents['Summary'].str.contains('|'.join(hijacking_keywords), case=False, na=False)]

# Create a slider for selecting the range of years
min_year = hijacking_incidents_df['Date'].dt.year.min()
max_year = hijacking_incidents_df['Date'].dt.year.max()
selected_years = st.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# Filter the hijacking incidents DataFrame based on the selected year range
filtered_df = hijacking_incidents_df[(hijacking_incidents_df['Date'].dt.year >= selected_years[0]) & (hijacking_incidents_df['Date'].dt.year <= selected_years[1])]

# Group the data by year and count the number of hijacking incidents per year
hijacking_incidents_by_year = filtered_df.groupby(filtered_df['Date'].dt.year).size().reset_index(name='Incidents')

# Create a bar chart to visualize the total number of hijacking incidents by year
fig2 = px.bar(
    hijacking_incidents_by_year,
    x='Date',
    y='Incidents',
    labels={'Date': 'Year', 'Incidents': 'Hijacking Incidents'},
    title='Total Hijacking Incidents by Year'
)

st.plotly_chart(fig2)

# Group the data by country and count the number of hijacking incidents per country
hijacking_incidents_by_country = filtered_df.groupby(filtered_df['LocationCountry']).size().reset_index(name='Incidents')

# Create a bar chart to visualize the total number of hijacking incidents by country
fig3 = px.bar(
    hijacking_incidents_by_country,
    x='LocationCountry',
    y='Incidents',
    labels={'LocationCountry': 'Country', 'Incidents': 'Hijacking Incidents'},
    title='Total Hijacking Incidents by Country'
)

fig3.update_xaxes(categoryorder='total descending')  # Sort countries by the number of incidents

st.plotly_chart(fig3)