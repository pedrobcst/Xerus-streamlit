import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
from peakutils import baseline
from plotly.graph_objects import Figure
from Xerus.readers.datareader import DataReader
from Xerus.settings.mplibcfg import Mplibcfg


def plot_read_data(data: str, format: str, poly_degree: int = 8, remove_base: bool = True) -> Figure:
    df_new, _, _, _, = DataReader().read_data(data, fmt=format)
    _y = df_new.int.copy()
    if _y is not None:
        background = baseline(_y, deg = poly_degree)
    df_new['background'] = background
    df_new['int_new'] = df_new.int - background
    fig = px.scatter(data_frame = df_new, x='theta', y = 'int', labels={"theta": "Theta", "int": "Intensity"}, template="presentation")
    fig.data[0].mode = "markers"
    fig.data[0].marker['color'] = 'purple'
    fig.data[0].marker['symbol'] = 'circle-open'
    fig.data[0].name = "Exp. Data"
    fig.data[0].showlegend = True

    if remove_base:
        fig.add_scatter(
            x=df_new.theta,
            y=df_new.background,
            name="Background",
            marker = {
                "symbol": "line-ns",
                "line_width": 1,
                "size": 12,
                "line": {"color": "blue"}
            }
        )
        fig.add_scatter(
            x=df_new.theta,
            y=df_new.int_new,
            name="Data - Background",
            marker = {
                "symbol": "line-ns",
                "line_width": 1,
                "size": 12,
                "line": {"color": "red"}
            }
        )
        fig.data[2].marker['color'] = "red"
        fig.data[1].marker['color'] = "blue"
    return fig

