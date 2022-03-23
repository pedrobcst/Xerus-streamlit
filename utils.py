import io
import os

from config import AppSettings


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
    with open(os.path.join(AppSettings.TMP_FOLDER, file.name), "w") as f:
        f.write(stringio.read())

    # Return path
    return os.path.join(AppSettings.TMP_FOLDER, file.name)
