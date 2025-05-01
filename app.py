import streamlit as st
import pandas as pd

from backend.schema_reader import extract_schema_context
from backend.local_llm_connector import generate_python_code_with_llm
from backend.safe_executor import execute_python_code

# Streamlit App Config
st.set_page_config(page_title="Enterprise AI-Powered Analytical Chatbot", layout="wide")
st.title("Enterprise AI Analyst (Local Model Powered)")

# Upload CSV
uploaded_file = st.file_uploader("Upload your excel file", type=["csv"])

# User input
query = st.text_area("Ask your question about the uploaded data:")

# Submit button
submit = st.button("Submit")

if uploaded_file and submit and query:
# Step 1: Read uploaded file
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        st.stop()

    # Step 2: Extract Schema Context
    schema_context = extract_schema_context(df)

# Step 3: Generate Python Code using Local LLM
    try:
        generated_code = generate_python_code_with_llm(schema_context, query,model="llama3")
        print("=== AI Generate Code ===")
        print(generated_code)
        if not generated_code or not generated_code.strip():
            st.error("Model retruned an empty response")
            st.stop()
        st.subheader("Generated Python Code by AI:")
        st.code(generated_code, language="python")
    except Exception as e:
        st.error(f"Error generating code from model: {str(e)}")
        st.stop()

    # Step 4: Execute the Generated Code
    result, fig = execute_python_code(generated_code, df)

    # Step 5: Display Result
    st.subheader("Answer:")
    if fig:
        st.pyplot(fig)
    elif isinstance(result, pd.DataFrame):
        st.dataframe(result)
    else:
        st.success(result)
