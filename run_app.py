import streamlit as st
import requests
import pandas as pd
from PIL import Image


# URL da API FastAPI local ou em cloud
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Chatbot Data", layout="wide")

st.title("🤖 Chatbot de Análise de Dados")

# -----------------------
# Upload opcional de CSV
# -----------------------
uploaded_file = st.file_uploader("Faça upload do seu dataset (opcional)", type=["csv", "gz"])
if uploaded_file:
    df_upload = pd.read_csv(uploaded_file)
    st.write("📊 Preview do dataset carregado:")
    st.dataframe(df_upload.head())

# -----------------------
# Campo de texto do chatbot
# -----------------------
user_question = st.text_input("Digite sua pergunta em linguagem natural:")

if st.button("Enviar"):
    if not user_question.strip():
        st.warning("Digite uma pergunta antes de enviar.")
    else:
        with st.spinner("Processando sua pergunta..."):
            try:
                # -----------------------
                # 1️⃣ Chamada ao endpoint /query-with-insights
                # -----------------------
                response = requests.post(
                    f"{API_URL}/query-with-insights",
                    json={"question": user_question}
                )
                data = response.json()

                if "error" in data:
                    st.error(f"Erro: {data['error']}")
                else:
                    # -----------------------
                    # 2️⃣ Exibir texto do insight
                    # -----------------------
                    st.subheader("📋 Resumo / Insight")
                    st.text(data["text_insight"])

                    # -----------------------
                    # 3️⃣ Exibir gráfico
                    # -----------------------
                    st.subheader("📈 Gráfico")
                    try:
                        img = Image.open(data["plot_path"])
                        st.image(img)
                    except Exception as e:
                        st.warning(f"Não foi possível exibir gráfico: {e}")

                    # -----------------------
                    # 4️⃣ Botão para download CSV
                    # -----------------------
                    st.subheader("💾 Download CSV")
                    with open(data["csv_path"], "rb") as f:
                        st.download_button(
                            label="Baixar CSV",
                            data=f,
                            file_name="resultado.csv",
                            mime="text/csv"
                        )

            except Exception as e:
                st.error(f"Erro ao chamar API: {e}")

# -----------------------
# Histórico opcional
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []

if user_question.strip():
    st.session_state.history.append(user_question)

if st.session_state.history:
    st.subheader("📝 Histórico de perguntas")
    for i, q in enumerate(st.session_state.history[::-1], 1):
        st.write(f"{i}. {q}")
