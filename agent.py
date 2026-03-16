from utilities import StepLogger,cache_get,cache_store,dataset_hash
from intelligence_engine import classify_intent,map_column,generate_insight
from data_intelligence import analyze_dataset
from query_planner import plan_query
from analytics_engine import *


def run_agent(query,df,persona,embeddings):

    logger=StepLogger()

    key = dataset_hash(df)+query

    cached=cache_get(key)

    if cached:
        return cached

    profile=analyze_dataset(df)

    logger.log("Dataset analyzed")

    intent,confidence = classify_intent(query)

    logger.log(f"Intent → {intent}")
    logger.log(f"Confidence → {confidence}")

    if confidence < 0.6:

        return {
            "type":"clarification",
            "message":"Intent unclear",
            "options":["summary","trend","groupby","drivers"]
        }

    metric = map_column(query,embeddings)

    logger.log(f"Metric mapped → {metric}")

    dimension=None

    for d in profile["dimensions"]:
        if d in query.lower():
            dimension=d

    plan = plan_query(intent)

    if plan=="groupby":
        result = groupby_analysis(df,metric,dimension)
        logger.engine("DuckDB")

    elif plan=="trend":
        result = trend_analysis(df,metric,profile["time"])

    elif plan=="share":
        result = share_analysis(df,metric,dimension)

    elif plan=="correlation":
        result = correlation_analysis(df,metric)

    elif plan=="drivers":
        result = detect_drivers(df,metric)

    elif plan=="anomaly":
        result = detect_anomalies(df)

    else:
        result = df.describe()

    logger.log("Analysis executed")

    insight = generate_insight(query,result,persona)

    output={
        "data":result,
        "insight":insight,
        "steps":logger.steps
    }

    cache_store(key,output)

    return output