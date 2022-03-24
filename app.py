import os

import streamlit as st

from conf import AppSettings
from xerus_plot import plot_read_data
from xerus_run import run_xerus

os.makedirs(AppSettings.TMP_FOLDER, exist_ok=True)
os.makedirs(AppSettings.RESULTS_TMP_FOLDER, exist_ok=True)
from utils import create_st_df, process_input, read_input

st.title('XERUS Streamlit Interface Beta')
st.sidebar.image("https://raw.githubusercontent.com/pedrobcst/Xerus/master/img/g163.png", width=100)

if 'xerus_started' not in st.session_state:
    st.session_state['xerus_started'] = False

if 'xerus_object' not in st.session_state:
    st.session_state['xerus_object'] = None


@st.cache
def run_analysis(args_xerus, args_analysis):
    return run_xerus(args_xerus, args_analysis)

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
    else:
        poly_degree = 10
    
    st.write("Current element list is:", elements)
    st.write("data format is:", data_format)
    
    
if file:
    path = read_input(file)
    working_folder = os.path.join(AppSettings.RESULTS_TMP_FOLDER, file.name.split(".")[0])
    os.makedirs(working_folder, exist_ok=True)
    st.write("File uploaded to:", path)
    st.write(f"Current file is {path}")
    st.write(f"Working folder is {working_folder}")


analysis = st.sidebar.button("View data", key="xerus_init")
if analysis:
    st.session_state['xerus_started'] = True
    st.session_state['xerus_object'] = None 
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
        ignore_providers = process_input(st.text_input("Ignore providers", value="", key="ignore_providers"))
        ignore_comb = process_input(st.text_input("Ignore combinations", value="", key="ignore_comb"))        
        st.write('ignore ids:', ignore_ids)
        st.write('ignore comb:', ignore_comb)
        st.write('ignore providers:', ignore_providers)
    # initialize = st.sidebar.button("Initialize XERUS", key="xerus_init")

    run = st.sidebar.button("Run analysis", key="run_analysis")
    if run:
        args_xerus = dict(name=name, working_folder=working_folder, exp_data_file=path,elements=elements, max_oxy=max_oxygen, use_preprocessed=use_preprocessed,remove_background=remove_background,poly_degree=poly_degree, data_fmt=data_format)

        args_analysis = dict(n_runs=n_runs, grabtop=g, delta=delta, ignore_ids=ignore_ids, ignore_provider=ignore_providers, ignore_comb=ignore_comb)

        results_search  = run_analysis(args_xerus, args_analysis)
        st.write('Finished')
        st.session_state['xerus_object'] = results_search
    if st.session_state.xerus_object:
        st.header('Analysis Results')
        results_search = st.session_state.xerus_object
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                df = create_st_df(results_search.results.copy())
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.dataframe(df)
            except NameError:
                st.write("Press Run analysis again.")
            # st.dataframe(results_search.results)   
        with st.sidebar.expander("Results Viz"):
            viz_number = int(st.number_input("viz number", min_value=-1, max_value=len(df) -1 , step=1))
        with col2:
            if viz_number != -1:
               fig = results_search.plot_result(viz_number, width=500, height=500)
               fig.update_layout(title=None)
               st.plotly_chart(fig, use_container_width=False)

        

