import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

air_accidents = pd.read_csv('Air_Accidents.csv')
air_accidents["Date"] = pd.to_datetime(air_accidents["Date"], format="%Y-%m-%d")

# Count military and non-military accidents
military_count = air_accidents['IsMilitary'].value_counts()

# Only non-military flights
non_military_accidents = air_accidents[air_accidents['IsMilitary'] == False]
non_military_accidents_by_year = non_military_accidents.groupby(non_military_accidents['Date'].dt.year).size()

# Convert the Series to a DataFrame
non_military_accidents_by_year_df = non_military_accidents_by_year.reset_index(name='Count')

# Only military flights
military_accidents = air_accidents[air_accidents['IsMilitary'] == True]
military_accidents_by_year = military_accidents.groupby(military_accidents['Date'].dt.year)['Date'].count()

# Convert the Series to a DataFrame
military_accidents_by_year_df = military_accidents_by_year.reset_index(name='Count')

# Top 20 operators with the most accidents (non-military flights)
top_20_operators_non_military = air_accidents[air_accidents['IsMilitary'] == False]['Operator'].value_counts().head(20).index
filtered_data_non_military = air_accidents[(air_accidents['Operator'].isin(top_20_operators_non_military)) & (air_accidents['IsMilitary'] == False)]

# Top 20 operators with the most accidents (military flights)
top_20_operators_military = air_accidents[air_accidents['IsMilitary'] == True]['Operator'].value_counts().head(20).index
filtered_data_military = air_accidents[(air_accidents['Operator'].isin(top_20_operators_military)) & (air_accidents['IsMilitary'] == True)]

# Filter the dataset into non-military flights
non_military_accidents = air_accidents[air_accidents['IsMilitary'] == False]

# Calculate the number of accidents for each country in non-military flights
top_countries_non_military = non_military_accidents['LocationCountry'].value_counts().head(20)

# Filter the dataset into military flights
military_accidents = air_accidents[air_accidents['IsMilitary'] == True]

# Calculate the number of accidents for each country in military flights
top_countries_military = military_accidents['LocationCountry'].value_counts().head(20)

st.write('## Visualizations')

st.write('#### General')

if st.checkbox('Fatalities Per Year'):
    if st.button('Scatterplot'):

        casualty_limit = st.slider('Casualty number:', 0, 600, 300, key='slider_key_0')

        graph_1 = plt.figure(figsize= (18, 8))
        years = air_accidents['Date'].dt.year
        plt.plot(air_accidents['Fatalities'], years, 'o')
        plt.xlabel('Fatalities')
        plt.ylabel('Years')

        filtered_data = air_accidents[air_accidents['Fatalities'] <= casualty_limit]
        plt.plot(filtered_data['Fatalities'], filtered_data['Date'].dt.year, 'o')
        st.pyplot(graph_1)

    if st.button('Line Chart'):

        year_limit = st.slider('Year:', 1908, 2022, 2002, key='slider_key_01')

        year_count = air_accidents.groupby(air_accidents.Date.dt.year)[['Date']].count()

        graph_2 = plt.figure(figsize= (18, 8))
        plt.plot(year_count.index, year_count['Date'], marker= '.')
        plt.xlabel('Years')
        plt.ylabel('Total Accidents')

        filtered_data = year_count[year_count.index <= year_limit]
        st.pyplot(graph_2)

st.write('#### Military vs. Non-Military')

if st.checkbox('Military vs. Non-Military Accidents'):
    graph_3 = plt.figure(figsize=(6, 6))
    plt.pie(military_count, labels=['Non-Military', 'Military'], autopct='%1.1f%%', startangle=90)
    plt.title('Proportion of Military vs. Non-Military Accidents')
    st.pyplot(graph_3)

if st.checkbox('Accidents Per Year (Non-Military)'):
    graph_4 = plt.figure(figsize=(12, 6))
    sns.lineplot(data=non_military_accidents_by_year_df, x='Date', y='Count', marker='o')
    plt.title('Number of Non-Military Accidents by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.grid(True)
    st.pyplot(graph_4)

if st.checkbox('Accidents Per Year (Military)'):
    graph_5 = plt.figure(figsize=(12, 6))
    sns.lineplot(data=military_accidents_by_year_df, x='Date', y='Count', marker='o')
    plt.title('Number of Military Accidents by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Accidents')
    plt.grid(True)
    st.pyplot(graph_5)

if st.checkbox('Correlation between Passengers on Board and Fatalities (Both)'):
    graph_6 = plt.figure(figsize=(10, 6))
    sns.scatterplot(data=air_accidents, x='PassengersAboard', y='Fatalities', hue='IsMilitary', palette='viridis')
    plt.title('Correlation Between Passengers on Board and Fatalities')
    plt.xlabel('Number of Passengers on Board')
    plt.ylabel('Total Fatalities')
    plt.legend(title='Military')
    st.pyplot(graph_6)

if st.checkbox('Survivors vs. Fatalities (Both)'):
    graph_7 = plt.figure(figsize=(10, 6))
    sns.barplot(data=air_accidents, x='IsMilitary', y='TotalFatalities', color='red', label='Fatalities')
    sns.barplot(data=air_accidents, x='IsMilitary', y='Survived', color='green', label='Survivors')
    plt.title('Fatalities vs. Survivors by Military vs. Non-Military Accidents')
    plt.xlabel('Is Military')
    plt.ylabel('Count')
    plt.xticks([0, 1], ['Non-Military', 'Military'])
    plt.legend()
    st.pyplot(graph_7)

st.write('###### By Operator')

if st.checkbox('Top 20 Most Accidents by Operator (Non-Military)'):
    graph_8 = plt.figure(figsize=(12, 6))
    sns.countplot(data=filtered_data_non_military, y='Operator', order=filtered_data_non_military['Operator'].value_counts().index)
    plt.title('Distribution of Accidents by Operator (Top 20, Non-Military)')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Operator')
    st.pyplot(graph_8)

if st.checkbox('Top 20 Most Accidents by Operator (Military)'):
    graph_9 = plt.figure(figsize=(12, 6))
    sns.countplot(data=filtered_data_military, y='Operator', order=filtered_data_military['Operator'].value_counts().index)
    plt.title('Distribution of Accidents by Operator (Top 20, Military)')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Operator')
    st.pyplot(graph_9)

st.write('###### By Country')

if st.checkbox('Top 20 Countries with Most Accidents (Non-Military)'):
    graph_10 = plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 2)
    sns.barplot(y=top_countries_non_military.index, x=top_countries_non_military.values, palette='viridis')
    plt.title('Top 20 Countries with Most Accidents (Non-Military)')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Country')

    plt.tight_layout()
    st.pyplot(graph_10)

if st.checkbox('Top 20 Countries with Most Accidents (Military)'):
    graph_11 = plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.barplot(y=top_countries_military.index, x=top_countries_military.values, palette='viridis')
    plt.title('Top 20 Countries with Most Accidents (Military)')
    plt.xlabel('Number of Accidents')
    plt.ylabel('Country')

    plt.tight_layout()
    st.pyplot(graph_11)








