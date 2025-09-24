import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Chatbot Data API", layout="wide")
st.title("Chatbot Data API 🧠")

# ------------------ Histórico ------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ Input do usuário ------------------
question = st.text_input("Digite sua pergunta em linguagem natural:")

if st.button("Enviar pergunta") and question:
    # 1️⃣ Chama endpoint NL → SQL
    payload = {"question": question}
    try:
        resp_sql = requests.post("http://127.0.0.1:8000/nl-to-sql", json=payload)
        resp_sql.raise_for_status()
        sql_data = resp_sql.json()
    except Exception as e:
        st.error(f"Erro ao chamar NL → SQL: {e}")
        sql_data = {}

    if "error" in sql_data:
        st.error(f"Erro ao gerar SQL: {sql_data['error']}")
    else:
        sql_query = sql_data.get("sql", "")
        st.subheader("SQL gerado pelo chatbot")
        st.code(sql_query, language="sql")

        # 2️⃣ Chama endpoint Query with Insights
        payload_insight = {"question": question, "sql": sql_query}
        try:
            resp_insight = requests.post("http://127.0.0.1:8000/query-with-insights", json=payload_insight)
            resp_insight.raise_for_status()
            data = resp_insight.json()
        except Exception as e:
            st.error(f"Erro ao executar SQL: {e}")
            data = {}

        # Adiciona ao histórico
        st.session_state.history.append({
            "question": question,
            "sql": sql_query,
            "insight": data.get("text_insight", ""),
            "data": data.get("data", [])
        })

# ------------------ Exibição do histórico ------------------
st.subheader("Histórico de perguntas e respostas")
for idx, h in enumerate(reversed(st.session_state.history), 1):
    st.markdown(f"### Pergunta {idx}: {h['question']}")
    st.markdown("**SQL gerado:**")
    st.code(h['sql'], language="sql")
    if h['insight']:
        st.markdown("**Insight:**")
        st.write(h['insight'])
    if h['data']:
        st.markdown("**Dados completos:**")
        df = pd.DataFrame(h['data'])
        st.dataframe(df)
        # Botão para download CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Baixar CSV",
            data=csv,
            file_name=f"resultado_{idx}.csv",
            mime="text/csv"
        )
    st.markdown("---")
