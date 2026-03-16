def plan_query(intent):

    if intent=="groupby":
        return "groupby"

    if intent=="trend":
        return "trend"

    if intent=="share":
        return "share"

    if intent=="correlation":
        return "correlation"

    if intent=="drivers":
        return "drivers"

    if intent=="anomaly":
        return "anomaly"

    return "summary"