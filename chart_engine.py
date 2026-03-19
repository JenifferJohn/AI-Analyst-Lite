import matplotlib.pyplot as plt

def generate_chart_safe(df):
    try:
        fig, ax = plt.subplots()
        df.plot(ax=ax)
        return fig
    except:
        return None