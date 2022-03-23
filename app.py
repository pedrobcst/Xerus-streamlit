import os

import streamlit as st
from Xerus import XRay

from conf import AppSettings

os.makedirs(AppSettings.TMP_FOLDER, exist_ok=True)
os.makedirs(AppSettings.RESULTS_TMP_FOLDER, exist_ok=True)
from utils import read_input

st.title('XERUS Streamlit Interface Beta')
st.sidebar.image("https://raw.githubusercontent.com/pedrobcst/Xerus/master/img/g163.png", width=100)

# Settings
with st.sidebar.expander("Settings"):
    file = st.file_uploader("Upload data", key="data_uploaded")
    data_format = st.text_input("Data format", value="ras", key="data_format")
    elements = st.text_input("Elements seperated by comma", value="Ho", key="element_list").split(",")
    max_oxygen = st.number_input("Max oxygen", min_value=0, max_value=10, step=1, value=2, key="max_oxy")
    use_preprocessed = st.checkbox("Use preprocessed data", value=False, key="use_pre")
    remove_background = st.checkbox("Remove background", value=True, key="remove_bg")
    if remove_background:
        poly_degree = st.number_input("Polynomial degree", min_value=2, max_value=12, step=1, value=8, key="poly_degree")

    st.write("Current element list is:", elements)
    
    
if file:
    path = read_input(file)
    st.write("File uploaded to:", path)
    st.write(f"Current file is {path}")

initialize = st.sidebar.button("Initialize XERUS", key="xerus_init")
if initialize:
    pass
