import pandas as pd
from sqlalchemy import create_engine

# ---------- Carregar dataset ----------
df = pd.read_csv("train.gz", compression="gzip")
print("Dimensões:", df.shape)
print("Colunas:", df.columns.tolist())
print(df.dtypes)
print(df.head())

# ---------- Separar colunas numéricas e categóricas ----------
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = df.select_dtypes(include='object').columns

# ---------- Imputação ----------
for col in numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

for col in categorical_cols:
    df[col].fillna('Desconhecido', inplace=True)

# ---------- Transformações ----------
df['data de referência'] = pd.to_datetime(df['REF_DATE'], utc=True)

# Renomear colunas
rename_dict = {
    "REF_DATE": "data_referencia",
    "TARGET": "alvo",
    "VAR1": "mau_pagador",
    "VAR2": "sexo",
    "VAR3": "idade",
    "VAR4": "flag_obito",
    "VAR5": "UF",
    "VAR6": "classe_social"
    # adicione demais colunas se precisar
}
df = df.rename(columns=rename_dict)

# Mapear flag_obito
df['flag_obito'] = df['flag_obito'].map({1: 'Sim', 0: 'Não'})

# ---------- Salvar CSV final ----------
df.to_csv("credit_train.csv", index=False, encoding="utf-8")
print("Arquivo credit_train.csv gerado com sucesso!")

# ---------- (Opcional) Enviar para PostgreSQL ----------
DATABASE_URL = "postgresql://postgres:senha@localhost:5432/meu_banco"
engine = create_engine(DATABASE_URL)
df.to_sql('credit_train', engine, if_exists='replace', index=False)
print("Dados enviados para o banco com sucesso!")
