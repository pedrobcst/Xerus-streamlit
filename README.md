# Xerus-streamlit
This is the repository for the Streamlit interface of XRay Estimation Using Refinement and Similarity (XERUS)
Currently, we are in beta phase. Most of functionalities of *Xerus* is already implemented and can be use via the interface without the need of any coding or use of jupyter notebooks.

# INSTALLATION:

Please first install the latest version of Xerus following the instructions in the [main repository](https://www.github.com/pedrobcst/Xerus/)

After, you can clone this repository and install the Streamlit dependencies doing:

```bash
git clone https://www.github.com/pedrobcst/Xerus-streamlit
pip install -r requirements.txt
```

# USING
To use please be aware this is just an **interface** around *Xerus*, and thus all the requirements to use *Xerus* are still necessary.
That is:
1. MongoDB server is running (and/or the configurations for a remote server is set in *Xerus* package)
2. The api-key settings (for materials project) are correctly set in *Xerus*

If this is set, just run:
```bash
streamlit run app.py
```
And the interface should load in the web (defaulting to port 8501).\
We are currently working in writing a documentation describing how to use step by step, and a Streamlit recording of the usage should be available soon.
