from dataclasses import dataclass
from typing import Tuple


@dataclass
class AppSettings:
    TMP_FOLDER: str = "tmp"
    RESULTS_TMP_FOLDER: str = "results_tmp"
    DROP_COLUMNS: Tuple = (
        "filename",
        "spacegroup_number",
        "full_path",
        "nruns",
        "pos",
        "gpx_path"
    )

