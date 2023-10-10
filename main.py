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

if st.checkbox('Dataframe'):
    st.dataframe(air_accidents)
    st.write("Rows: ", air_accidents.shape[0])
    st.write("Columns: ", air_accidents.shape[1])
