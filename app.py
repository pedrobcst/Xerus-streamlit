import os

import streamlit as st

from config import AppSettings

os.makedirs(AppSettings.TMP_FOLDER, exist_ok=True)
from utils import read_input

st.title('XERUS Streamlit Interface Beta')
st.sidebar.image("https://raw.githubusercontent.com/pedrobcst/Xerus/master/img/g163.png", width=100)
file = st.sidebar.file_uploader("Upload data")
if file:
    path = read_input(file)
    st.write("File uploaded to:", path)
    st.write(f"Current file is {path}")

