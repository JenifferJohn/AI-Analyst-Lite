import pandas as pd
import difflib


BLOCKED_PATTERNS = [
    "import os",
    "import sys",
    "subprocess",
    "open(",
    "eval(",
    "exec("
]


def validate_code(code):

    for pattern in BLOCKED_PATTERNS:

        if pattern in code.lower():
            return False, pattern

    return True, None


def normalize_result(result):

    if result is None:

        return {
            "status": "empty",
            "message": "No results returned."
        }

    if isinstance(result, pd.DataFrame) and result.empty:

        return {
            "status": "empty",
            "message": "Query executed but returned no rows."
        }

    return {
        "status": "ok",
        "data": result
    }


def suggest_columns(query, df):

    columns = list(df.columns)

    matches = []

    for word in query.split():

        close = difflib.get_close_matches(
            word,
            columns,
            n=3,
            cutoff=0.6
        )

        matches.extend(close)

    return list(set(matches))