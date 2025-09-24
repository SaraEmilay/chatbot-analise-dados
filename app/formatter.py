import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Detecta tipo de coluna
def detect_data_type(df):
    types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            types[col] = 'numeric'
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = 'datetime'
        else:
            types[col] = 'categorical'
    return types

# Resumo em linguagem natural
def to_text_insight(df, question=""):
    types = detect_data_type(df)
    summary = []
    for col, dtype in types.items():
        if dtype == 'numeric':
            summary.append(f"{col}: média={df[col].mean():.2f}, min={df[col].min()}, max={df[col].max()}")
        elif dtype == 'categorical':
            top_val = df[col].value_counts().idxmax()
            summary.append(f"{col}: valor mais frequente='{top_val}'")
        elif dtype == 'datetime':
            summary.append(f"{col}: período de {df[col].min()} até {df[col].max()}")
    text = f"Pergunta: {question}\nResumo dos dados:\n" + "\n".join(summary)
    return text

# Gerar gráfico automaticamente
def to_plot(df, save_path="plot.png", chart_type="auto"):
    types = detect_data_type(df)
    
    plt.figure(figsize=(8,5))
    
    # Escolha automática de gráfico
    if chart_type == "auto":
        numeric_cols = [c for c, t in types.items() if t=='numeric']
        categorical_cols = [c for c, t in types.items() if t=='categorical']
        if len(numeric_cols) == 1:
            chart_type = "hist"
        elif len(numeric_cols) > 1:
            chart_type = "bar"
        elif categorical_cols:
            chart_type = "count"
        else:
            chart_type = "hist"

    # Plot
    if chart_type == "hist":
        plt.hist(df[numeric_cols[0]], bins=20)
        plt.title(f"Histograma de {numeric_cols[0]}")
    elif chart_type == "bar":
        df[numeric_cols].mean().plot(kind='bar')
        plt.title("Média das colunas numéricas")
    elif chart_type == "count":
        sns.countplot(y=categorical_cols[0], data=df, order=df[categorical_cols[0]].value_counts().index)
        plt.title(f"Contagem de {categorical_cols[0]}")

    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    return os.path.abspath(save_path)

# Gerar CSV para download
def to_csv(df, file_name="result.csv"):
    df.to_csv(file_name, index=False)
    return os.path.abspath(file_name)
