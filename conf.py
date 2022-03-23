from dataclasses import dataclass


@dataclass
class AppSettings:
    TMP_FOLDER: str = "tmp"
    RESULTS_TMP_FOLDER: str = "results_tmp"
