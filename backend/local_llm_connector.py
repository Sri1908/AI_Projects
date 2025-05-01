import requests

def generate_python_code_with_llm(schema_context: str, user_query: str, model: str = "llama3") -> str:
    url = "http://localhost:11434/api/generate"
    full_prompt = f"""
    You are an expert Python data analyst.
    You must always answer ONLY by giving valid executable Python Pandas code, without explanation.
    Follow strictly:
    - Use 'df' as the input dataframe.
    - Calculate whatever the user is asking in the form of Python code.
    - Assign the final result to a variable named 'result'.
    - If visualization is needed, assign the figure to a variable called 'fig'.
    - DO NOT explain, DO NOT comment, only return raw code.

    Dataset Schema:
    {schema_context}

    User Question:
    {user_query}

    Reply ONLY in Python Code.
    """

    payload = {
    "model": model,
    "prompt": full_prompt,
    "stream": False
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()["response"].strip()

        cleaned_code = ""

        if result.startswith("```"):
            parts = result.split("```")
            if len(parts) >= 2:
                code_block = parts[1]
                if code_block.strip().startswith("python"):
                    code_block = code_block.strip()[len("python"):].strip()
                cleaned_code = code_block
        else:
            lines = result.splitlines()
            code_lines = [line for line in lines if "import" in line or "df" in line or "result" in line or "fig" in line]
            cleaned_code = "\n".join(code_lines)

        return cleaned_code.strip()
    else:
            raise Exception(f"Error from Ollama server: {response.text}")