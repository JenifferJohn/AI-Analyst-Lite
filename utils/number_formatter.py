# core/number_formatter.py

def format_number_indian_to_international(value):
    # convert numeric value to readable international format with exact number

    if value is None:
        return "N/A"

    try:
        value = float(value)
    except Exception:
        return str(value)

    # exact format with commas
    exact = f"{value:,.0f}"

    abs_val = abs(value)

    # convert to international readable format
    if abs_val >= 1_000_000_000:
        readable = f"{value / 1_000_000_000:.2f} billion"
    elif abs_val >= 1_000_000:
        readable = f"{value / 1_000_000:.2f} million"
    elif abs_val >= 1_000:
        readable = f"{value / 1_000:.2f} thousand"
    else:
        readable = f"{value:.2f}"

    return f"{readable} ({exact})"


def format_percentage(value):
    # format percentage safely

    if value is None:
        return "N/A"

    try:
        return f"{float(value):.2f}%"
    except Exception:
        return str(value)


def format_currency(value, symbol="₹"):
    # format value as currency with readable scale

    formatted = format_number_indian_to_international(value)

    if formatted == "N/A":
        return formatted

    return f"{symbol}{formatted}"