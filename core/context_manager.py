CONTEXT = {
    "metric": None,
    "dimension": None,
    "time_filter": None
}


def update_context(query: str):
    q = query.lower()

    if "sales" in q:
        CONTEXT["metric"] = "Sales Value (In INR)"

    if "market" in q:
        CONTEXT["dimension"] = "Markets"

    if "product" in q:
        CONTEXT["dimension"] = "Products"

    if "last 3 months" in q:
        CONTEXT["time_filter"] = "last_3_months"

    return CONTEXT


def get_context():
    return CONTEXT