import pandas as pd

def to_text_insight(df):
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()
    
    text = ""
    
    if numeric_cols and categorical_cols:
        # Média das numéricas pela primeira categórica
        grouped = df.groupby(categorical_cols[0])[numeric_cols].mean().reset_index()
        text = f"Média das colunas numéricas por '{categorical_cols[0]}': " + \
               ", ".join([f"{row[categorical_cols[0]]}: " + 
                          ", ".join([f"{col}: {row[col]:.1f}" for col in numeric_cols])
                          for _, row in grouped.iterrows()])
    
    elif numeric_cols:
        means = df[numeric_cols].mean()
        text = "Média das colunas numéricas: " + ", ".join([f"{col}: {val:.2f}" for col, val in means.items()])
    
    elif categorical_cols:
        counts = df[categorical_cols[0]].value_counts()
        text = f"Contagem de '{categorical_cols[0]}': " + ", ".join([f"{idx}: {val}" for idx, val in counts.items()])
    
    return text
