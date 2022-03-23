import os

import streamlit as st
from Xerus import XRay

from conf import AppSettings

os.makedirs(AppSettings.TMP_FOLDER, exist_ok=True)
os.makedirs(AppSettings.RESULTS_TMP_FOLDER, exist_ok=True)
from utils import read_input

st.title('XERUS Streamlit Interface Beta')
st.sidebar.image("https://raw.githubusercontent.com/pedrobcst/Xerus/master/img/g163.png", width=100)

if 'xerus_started' not in st.session_state:
    st.session_state['xerus_started'] = False



# Settings
with st.sidebar.expander("Settings"):
    name = st.text_input("Dataset name", key="name")
    file = st.file_uploader("Upload data", key="data_uploaded")
    data_format = st.text_input("Data format", value="ras", key="data_format")
    elements = st.text_input("Elements seperated by comma", value="Ho", key="element_list").split(",")
    max_oxygen = st.number_input("Max oxygen", min_value=0, max_value=10, step=1, value=2, key="max_oxy")
    use_preprocessed = st.checkbox("Use preprocessed data", value=False, key="use_pre")
    remove_background = st.checkbox("Remove background", value=True, key="remove_bg")
    if remove_background:
        poly_degree = st.number_input("Polynomial degree", min_value=2, max_value=12, step=1, value=8, key="poly_degree")
    
    st.write("Current element list is:", elements)
    st.write("data format is:", data_format)
    
    
if file:
    path = read_input(file)
    working_folder = os.path.join(AppSettings.RESULTS_TMP_FOLDER, file.name.split(".")[0])
    os.makedirs(working_folder, exist_ok=True)
    st.write("File uploaded to:", path)
    st.write(f"Current file is {path}")
    st.write(f"Working folder is {working_folder}")


analysis = st.sidebar.button("Initialize XERUS", key="xerus_init")
if analysis:
    st.session_state['xerus_started'] = True 
    analyzer = XRay(name=name, working_folder=working_folder, exp_data_file=path,
    elements=elements, max_oxy=max_oxygen, use_preprocessed=use_preprocessed,remove_background=remove_background,poly_degree=poly_degree, data_fmt=data_format)

if st.session_state['xerus_started']:
    with st.sidebar.expander('Analysis settings'):
        n_runs = st.text_input("Number of runs", value="auto", key="n_runs")
        if n_runs != "auto":
            n_runs = int(n_runs)
            st.write("Number of runs:", n_runs)
        g = st.number_input("g", min_value=1, max_value  = 999, value=3, step=1, key="grabtop")
        delta = st.number_input(r"delta", min_value=1.0, max_value=5.0, value=1.3, step=0.1, key="delta")
        ignore_ids = st.text_input("Ignore IDs", value="", key="ignore_ids")
        if ignore_ids:
            ignore_ids = ignore_ids.split(",")
        else:
            ignore_ids = None
        ignore_providers = st.text_input("Ignore providers", value="", key="ignore_providers")
        if ignore_providers:
            ignore_providers = ignore_providers.split(",")
        else:
            ignore_providers = None
        ignore_comb = st.text_input("Ignore combinations", value="", key="ignore_comb")
        if ignore_comb:
            ignore_comb = ignore_comb.split(",")
        else:
            ignore_comb = None
        
        st.write('ignore ids:', ignore_ids)
        st.write('ignore comb:', ignore_comb)
        st.write('ignore providers:', ignore_providers)
    # initialize = st.sidebar.button("Initialize XERUS", key="xerus_init")

    run_analysis = st.sidebar.button("Run analysis", key="run_analysis")
    if run_analysis:
        st.write(name)
        print("MARCOS DOGAO")
        # analyzer.analyze(n_runs=n_runs, g=g, delta=delta, ignore_ids=ignore_ids, ignore_providers=ignore_providers, ignore_comb=ignore_comb)
