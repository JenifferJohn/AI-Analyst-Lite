import matplotlib.pyplot as plt


def analytics_engine(df, query):

    q = query.lower()

    if "total" in q or "sum" in q:
        return df.sum(numeric_only=True)

    if "average" in q or "mean" in q:
        return df.mean(numeric_only=True)

    if "max" in q:
        return df.max(numeric_only=True)

    if "min" in q:
        return df.min(numeric_only=True)

    if "count" in q:
        return df.count()

    return df.describe()


def chart_engine(df):

    numeric = df.select_dtypes(include="number")

    fig, ax = plt.subplots()

    numeric.sum().plot(kind="bar", ax=ax)

    return fig


def root_cause_engine(df):

    correlations = df.corr(numeric_only=True)

    return correlations