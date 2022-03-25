import os
import shutil

import numpy as np
import streamlit as st
from st_aggrid import AgGrid

from conf import AppSettings
from xerus_plot import plot_read_data
from xerus_run import run_xerus

os.makedirs(AppSettings.TMP_FOLDER, exist_ok=True)
os.makedirs(AppSettings.RESULTS_TMP_FOLDER, exist_ok=True)
from utils import process_input, read_input

st.title('XERUS Streamlit Interface Beta')
st.sidebar.image("https://raw.githubusercontent.com/pedrobcst/Xerus/master/img/g163.png", width=100)

if 'xerus_started' not in st.session_state:
    st.session_state['xerus_started'] = False

if 'xerus_object' not in st.session_state:
    st.session_state['xerus_object'] = None
if 'zip_file' not in st.session_state:
    st.session_state['zip_file'] = False
    


@st.cache
def run_analysis(args_xerus, args_analysis):
    return run_xerus(args_xerus, args_analysis)

# Settings
with st.sidebar.expander("Settings", expanded=False):
    name = st.text_input("Dataset name", key="name")
    file = st.file_uploader("Upload data", key="data_uploaded")
    data_format = st.text_input("Data format", value="ras", key="data_format")
    elements = st.text_input("Elements seperated by comma", value="Ho", key="element_list").split(",")
    max_oxygen = st.number_input("Max oxygen", min_value=0, max_value=10, step=1, value=2, key="max_oxy")
    use_preprocessed = st.checkbox("Use preprocessed data", value=False, key="use_pre")
    remove_background = st.checkbox("Remove background", value=True, key="remove_bg")
    if remove_background:
        poly_degree = st.number_input("Polynomial degree", min_value=2, max_value=12, step=1, value=8, key="poly_degree")
    else:
        poly_degree = 10
    
    st.write("Current element list is:", elements)
    st.write("data format is:", data_format)
    
    
if file:
    path = read_input(file)
    working_folder = os.path.join(AppSettings.RESULTS_TMP_FOLDER, file.name.split(".")[0]) + f"_{name}"
    os.makedirs(working_folder, exist_ok=True)
    st.write("File uploaded to:", path)
    st.write(f"Current file is {path}")
    st.write(f"Working folder is {working_folder}")

if file:
    analysis = st.sidebar.button("View data", key="xerus_init")
    if analysis:
        st.session_state['xerus_started'] = True
        st.session_state['xerus_object'] = None 
        st.session_state['zip_file'] = False
        # st.session_state.xerus_object = XRay(name=name, working_folder=working_folder, exp_data_file=path,
        # elements=elements, max_oxy=max_oxygen, use_preprocessed=use_preprocessed,remove_background=remove_background,poly_degree=poly_degree, data_fmt=data_format)

if st.session_state['xerus_started']:
    st.header('Loaded data')
    if path:
        figure = plot_read_data(path, format=data_format, poly_degree=int(poly_degree), remove_base=remove_background)
        st.plotly_chart(figure)
    with st.sidebar.expander('Analysis settings'):
        n_runs = st.text_input("Number of runs", value="auto", key="n_runs")
        if n_runs != "auto":
            n_runs = int(n_runs)
            st.write("Number of runs:", n_runs)
        g = int(st.number_input("g", min_value=1, max_value  = 999, value=3, step=1, key="grabtop"))
        delta = st.number_input(r"delta", min_value=1.0, max_value=5.0, value=1.3, step=0.1, key="delta")
        ignore_ids = process_input(st.text_input("Ignore IDs", value="", key="ignore_ids"))
        ignore_providers = process_input(st.text_input("Ignore providers", value="AFLOW", key="ignore_providers"))
        ignore_comb = process_input(st.text_input("Ignore combinations", value="", key="ignore_comb"))        
        st.write('ignore ids:', ignore_ids)
        st.write('ignore comb:', ignore_comb)
        st.write('ignore providers:', ignore_providers)
    # initialize = st.sidebar.button("Initialize XERUS", key="xerus_init")
    st.markdown("<hr>", unsafe_allow_html=True)

    run = st.sidebar.button("Run analysis", key="run_analysis")
    if run:
        args_xerus = dict(name=name, working_folder=working_folder, exp_data_file=path,elements=elements, max_oxy=max_oxygen, use_preprocessed=use_preprocessed,remove_background=remove_background,poly_degree=poly_degree, data_fmt=data_format)

        args_analysis = dict(n_runs=n_runs, grabtop=g, delta=delta, ignore_ids=ignore_ids, ignore_provider=ignore_providers, ignore_comb=ignore_comb)

        with st.spinner('Running analysis...'):
            results_search  = run_analysis(args_xerus, args_analysis)
        st.write('Finished')
        st.balloons()
        st.session_state['xerus_object'] = results_search
    if st.session_state.xerus_object:
        st.header('Analysis Results')
        results_search = st.session_state.xerus_object
        df = results_search.results.copy()
        df.drop(list(AppSettings.DROP_COLUMNS), axis=1, inplace=True)
        df['id'] = df.index
        df = df[['id', 'name', 'rwp', 'wt', 'spacegroup', 'crystal_system', 'system_type']]
        AgGrid(df, width='50%', height=200)
        with st.sidebar.expander("Viz Settings"):
            viz_number = int(st.number_input("viz number", min_value=-1, max_value=len(df) -1 , step=1, key='viz_number'))
        
        if viz_number != -1:
            fig = results_search.plot_result(viz_number)
            fig.update_layout(title=None, width=800, height=600)
            st.plotly_chart(fig, use_container_width=False)
        
        if st.sidebar.button('Zip Contents'):
            shutil.make_archive(working_folder, 'zip', working_folder)
            st.session_state['zip_file'] = True
        
        if st.session_state['zip_file']:
            if os.path.exists(f"{working_folder}.zip"):
                with open(f"{working_folder}.zip", "rb") as fp:
                    btn = st.sidebar.download_button(
                        label="Download ZIP file",
                        data=fp,
                        file_name="results.zip",
                        mime="application/zip"
                    )

        with st.sidebar.expander('Optimizer Settings'):
            n_trials = int(st.number_input("Number of trials", min_value=20, max_value=99999, value=200, step=1, key="n_trials"))





        

