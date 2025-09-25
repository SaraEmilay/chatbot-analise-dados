import streamlit as st
import pandas as pd
from io import BytesIO
from app.nl_to_sql import run_pandas_query
from app.formatter import to_text_insight

st.title("Chatbot de Análise de Dados")

# ---------- Upload do dataset ----------
uploaded_file = st.file_uploader("Envie seu arquivo credit_train.csv", type=["csv"])

if uploaded_file is not None:
    # Ler CSV direto
    df = pd.read_csv(uploaded_file)

    # ---------- Preprocessamento ----------
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    categorical_cols = df.select_dtypes(include='object').columns

    for col in numeric_cols:
        df[col].fillna(df[col].median(), inplace=True)
    for col in categorical_cols:
        df[col].fillna('Desconhecido', inplace=True)

    if 'REF_DATE' in df.columns:
        df['data_referencia'] = pd.to_datetime(df['REF_DATE'], utc=True)

    rename_dict = {
        "REF_DATE": "data_referencia",
        "TARGET": "alvo",
        "VAR1": "mau_pagador",
        "VAR2": "sexo",
        "VAR3": "idade",
        "VAR4": "flag_obito",
        "VAR5": "UF",
        "VAR6": "classe_social"
    }
    df = df.rename(columns=rename_dict)

    if 'flag_obito' in df.columns:
        df['flag_obito'] = df['flag_obito'].map({1: 'Sim', 0: 'Não'})

    st.success("Dataset processado e pronto para perguntas!")

    # ---------- Entrada do usuário ----------
    pergunta = st.text_input("Faça uma pergunta sobre os dados:")

    if st.button("Gerar resultado e insight"):
        try:
            pandas_code, result = run_pandas_query(pergunta)

            st.subheader("Código Pandas gerado")
            st.code(pandas_code, language="python")

            if isinstance(result, pd.DataFrame):
                resultado_insight = to_text_insight(result)
                st.subheader("Insight em linguagem natural")
                st.write(resultado_insight)

                if not result.empty:
                    st.subheader("Prévia dos dados")
                    st.dataframe(result.head(20))
                else:
                    st.info("Nenhum dado retornado para essa consulta.")
            else:
                st.subheader("Resultado")
                st.write(result)
                st.subheader("Insight")
                st.write(f"Resultado: {result}")

        except Exception as e:
            st.error(f"Erro ao gerar resultado ou insight: {e}")
else:
    st.info("Envie um arquivo credit_train.csv para começar.")
