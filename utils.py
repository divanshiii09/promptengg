import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from io import StringIO
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=GOOGLE_API_KEY
)

def generate_python_code(question, df_sample):
    prompt = f"""
You are a smart data analyst. Based on the below DataFrame sample:

{df_sample}

Answer the question: "{question}" by generating only a Python code block that:
- Uses pandas or matplotlib
- Starts with 'import' statements if needed
- Uses a variable called 'df' as the DataFrame
- Do NOT include explanations

Provide only valid executable Python code.
"""
    
def clean_code(text):
    # Remove markdown-style code blocks
    lines = text.strip().split('\n')
    if lines[0].startswith("```"):
        lines = lines[1:]
    if lines[-1].startswith("```"):
        lines = lines[:-1]
    return "\n".join(lines)

def generate_python_code(question, df_sample):
    prompt = f"""
You are a smart data analyst. Based on the below DataFrame sample:

{df_sample}

Answer the question: "{question}" by generating only a Python code block that:
- Uses pandas or matplotlib
- Uses Streamlit to display outputs (like st.write, st.dataframe, st.pyplot)
- Starts with 'import' statements if needed
- Uses a variable called 'df' as the DataFrame
- Do NOT include explanations


Provide only valid executable Python code.
"""
    raw_response = llm.invoke(prompt).content
    return clean_code(raw_response)


def execute_python_code(code, df):
    try:
        local_vars = {"df": df, "st": st}
        exec(code, {}, local_vars)
        return "✅ Code ran successfully", None
    except Exception as e:
        return None, str(e)



