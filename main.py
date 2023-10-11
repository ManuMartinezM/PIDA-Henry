import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from PIL import Image

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.title('Air Accidents - PIDA')
st.write('Manuel Martínez Margalef')
st.markdown('***') # Línea horizontal

cover_image = Image.open('cover_image.jpg')
st.image(cover_image, use_column_width=True)

st.write('### Dataset')

air_accidents = pd.read_csv('Air_Accidents.csv')
air_accidents["Date"] = pd.to_datetime(air_accidents["Date"], format="%Y-%m-%d")

# Create a slider for selecting the year range
year_range_filter = st.slider('Select a year range', air_accidents['Date'].dt.year.min(), air_accidents['Date'].dt.year.max(), (2002, 2021))

# Filter the DataFrame based on the selected year range
filtered_data = air_accidents[(air_accidents['Date'].dt.year >= year_range_filter[0]) & (air_accidents['Date'].dt.year <= year_range_filter[1])]

if st.checkbox('Dataframe'):
    st.dataframe(filtered_data)
    st.write("Rows: ", filtered_data.shape[0])
    st.write("Columns: ", filtered_data.shape[1])