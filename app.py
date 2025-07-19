import streamlit as st
import pandas as pd
from utils import generate_python_code, execute_python_code

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("📊 AI-Powered Data Analyst (Gemini)")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("📄 **Data Preview:**", df.head())

    question = st.text_input("Ask a question about your data")

    if st.button("Analyze") and question:
        sample = df.head(3).to_markdown()
        with st.spinner("Analyzing with Gemini..."):
            code = generate_python_code(question, sample)

        st.subheader("🧠 Generated Code:")
        st.code(code, language="python")

        with st.spinner("Executing code..."):
            result, _ = execute_python_code(code, df)

        st.subheader("📈 Result / Output:")
        if "plt" in code:
            st.pyplot()
        else:
            st.write(result)

result, error = execute_python_code(code, df)
if error:
    st.error(error)
else:
    st.success(result)