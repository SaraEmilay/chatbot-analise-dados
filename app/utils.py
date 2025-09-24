def format_insight(df, question):
    """Converte DataFrame em texto resumido"""
    if df.empty:
        return "Não há resultados para a query."
    # Protótipo: mostra as primeiras 10 linhas
    return df.head(10).to_dict(orient="records")
