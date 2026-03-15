def run_analysis(code, df):

    if "import" in code or "os." in code or "open(" in code:
        return "Unsafe code blocked"

    local_env = {"df": df}

    try:
        result = eval(code, {}, local_env)
        return result

    except Exception as e:
        return f"Error executing code: {e}"