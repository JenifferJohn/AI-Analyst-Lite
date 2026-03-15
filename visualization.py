import pandas as pd
import matplotlib.pyplot as plt


def render_result(result):
    if isinstance(result, pd.Series):
        fig, ax = plt.subplots()
        result.plot(ax=ax)
        return fig

    if isinstance(result, pd.DataFrame):
        if result.shape[1] == 1:
            fig, ax = plt.subplots()
            result.plot(ax=ax)
            return fig
        return result

    return result