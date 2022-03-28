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



def process_input(input: str, return_int: bool = False) -> Union[None, List]:
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
        if return_int:
            return_list = [int(element) for element in input.split(",")]
            if len(return_list) > 1:
                return return_list
            else:
                return return_list[0]
        return input.split(",")
    else:
        return None

    