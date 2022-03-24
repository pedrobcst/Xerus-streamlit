import codecs
import io
import os
from typing import List, Union

import pandas as pd

from conf import AppSettings


def read_input(file: io.BytesIO) -> None:
    """Helper function to save the input file into a temporary folder.

    Parameters
    ----------
    file : io.BytesIO
        An UploadedFile from Streamlit st.file_uploader.

    Returns
    -------
    _type_
        Nothing. Save files into the temporary folder.
    """
    stringio = io.StringIO(file.getvalue().decode("shift-jis"))

    # Save
    with codecs.open(os.path.join(AppSettings.TMP_FOLDER, file.name), "w", "shift-jis") as f:
        f.write(stringio.read())

    # Return path
    return os.path.join(AppSettings.TMP_FOLDER, file.name)



def process_input(input: str) -> Union[None, List]:
    """Helper function to process streamlit inputs.

    Parameters
    ----------
    input : str
        A streamlit input that is seperated by comma.

    Returns
    -------
    Union[None, List]
        Returns a list if the input is not empty. Otherwise, returns None.
    """
    if input:
        return input.split(",")
    else:
        return None

def create_st_df(df: pd.DataFrame) -> pd.DataFrame:

    def transform(element) -> str:
        # if isinstance(element, float):
        #     return element
        # if isinstance(element, int):
        #     return element
        # if isinstance(element, str):
        #     return element
        
        return str(element)

    return df.applymap(transform)
