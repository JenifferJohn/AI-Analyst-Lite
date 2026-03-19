import duckdb
import pandas as pd


def run_duckdb(df,sql):

    con = duckdb.connect()
    con.register("data",df)

    return con.execute(sql).df()


def groupby_analysis(df,metric,dimension):

    sql=f"""
    SELECT {dimension},
    SUM({metric}) as value
    FROM data
    GROUP BY {dimension}
    ORDER BY value DESC
    """

    return run_duckdb(df,sql)


def trend_analysis(df,metric,time_col):

    if not time_col:
        return df[metric]

    sql=f"""
    SELECT {time_col},
    SUM({metric}) as value
    FROM data
    GROUP BY {time_col}
    """
    
    return run_duckdb(df,sql)


def share_analysis(df,metric,dimension):

    grouped = df.groupby(dimension)[metric].sum()

    return grouped / grouped.sum()


def correlation_analysis(df,metric):

    numeric = df.select_dtypes(include="number")

    return numeric.corr()[metric]


def detect_drivers(df,target_metric):

    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()[target_metric].drop(target_metric)
    drivers = corr.sort_values(ascending=False)
    
    return drivers.head(5)


def detect_anomalies(df):

    anomalies=[]
    numeric = df.select_dtypes(include="number")

    for col in numeric.columns:

        mean=numeric[col].mean()
        std=numeric[col].std()

        outliers = numeric[numeric[col] > mean + 3*std]

        if len(outliers)>0:

            anomalies.append({
                "column":col,
                "count":len(outliers)
            })

    return anomalies


def discover_highlevel_insights(df, profile):

    insights = []

    metrics = profile["metrics"]
    dims = profile["dimensions"]
    time_col = profile["time"]

    if not metrics:

        insights.append({
            "title": "Dataset Overview",
            "description": "No numeric metrics detected in dataset.",
            "evidence": df.head()
        })

        return insights

    metric = metrics[0]

    # top performer insight
    if dims:

        dim = dims[0]

        grouped = df.groupby(dim)[metric].sum().sort_values(ascending=False)

        insights.append({
            "title": "Top Performer",
            "description": f"{grouped.index[0]} has the highest {metric}",
            "evidence": grouped.head(5)
        })

    # trend insight
    if time_col:

        trend = trend_analysis(df, metric, time_col)

        if trend is not None and len(trend) > 1 and "value" in trend.columns:

            # sort properly
            trend = trend.sort_values(by=time_col)

            first = trend.iloc[0]["value"]
            last = trend.iloc[-1]["value"]

            if first != 0:

                change = last - first
                pct_change = (change / first) * 100

                direction = "increased" if change > 0 else "decreased"

                # peak detection
                peak_row = trend.loc[trend["value"].idxmax()]
                peak_time = peak_row[time_col]
                peak_value = peak_row["value"]

                insights.append({
                    "title": "Trend",
                    "description": f"{metric} {direction} by {abs(change):,.0f} ({abs(pct_change):.1f}%) over time. Peak in {peak_time} at {peak_value:,.0f}.",
                    "evidence": trend.tail(5)
                })

    return insights