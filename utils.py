import io
import os

from config import AppSettings


def read_input(file: io.BytesIO) -> None:
    stringio = io.StringIO(file.getvalue().decode("shift-jis"))

    # Save
    with open(os.path.join(AppSettings.TMP_FOLDER, file.name), "w") as f:
        f.write(stringio.read())

    # Return path
    return os.path.join(AppSettings.TMP_FOLDER, file.name)
