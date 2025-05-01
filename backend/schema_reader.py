import pandas as pd

def extract_schema_context(df: pd.DataFrame) -> str:
    schema_description = "Here is the schema of the uploaded dataset:\n"
    for col in df.columns:
        dtype = str(df[col].dtype)
        sample_values = df[col].dropna().unique()[:3]
        samples_text = ", ".join([str(val) for val in sample_values])
        schema_description += f"- {col} ({dtype}) e.g., {samples_text}\n"
    return schema_description
