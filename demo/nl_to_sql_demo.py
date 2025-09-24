import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # ou URL da Cloud

st.title("Chatbot Data Demo")

question = st.text_input("Digite sua pergunta:")

if st.button("Gerar SQL"):
    response = requests.post(f"{API_URL}/nl-to-sql", json={"question": question})
    data = response.json()
    st.subheader("SQL Gerado")
    st.code(data.get("sql", data.get("error")), language="sql")

    # Se quiser rodar direto o SQL e ver os dados:
    if "sql" in data:
        response2 = requests.post(f"{API_URL}/query-with-insights", json={"question": question, "sql": data["sql"]})
        result = response2.json()
        st.subheader("Insights")
        st.write(result.get("text_insight"))
        st.subheader("Dados")
        st.dataframe(result.get("data"))
