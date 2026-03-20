def generate_insights(df):

    insights = []

    numeric = df.select_dtypes(include=["number"]).columns

    for col in numeric:
        insights.append(f"{col} avg: {round(df[col].mean(),2)}")
        insights.append(f"{col} max: {df[col].max()}")
        insights.append(f"{col} min: {df[col].min()}")

    return "\n".join(insights)