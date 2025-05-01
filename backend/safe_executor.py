def execute_python_code(code, df):
    import pandas as pd
    import matplotlib.pyplot as plt
    import io

    # Clean code: remove any accidental read_csv or read_excel line
    cleaned_code = "\n".join(
    line for line in code.splitlines() if "read_csv" not in line and "read_excel" not in line)

    local_vars = {"df": df}
    fig = None

    try:
        exec(cleaned_code, {}, local_vars)
        result = local_vars.get('result', None)

        # Handle plotting
        if 'fig' in local_vars:
            fig = local_vars['fig']

        return result, fig

    except Exception as e:
        return f"Execution error: {str(e)}", None