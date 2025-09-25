from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
from app.formatter import to_text_insight

# Imports locais
from app.nl_to_sql import run_pandas_query  


# -----------------------
# Carregar CSV
# -----------------------
df = pd.read_csv("credit_train.csv")

# -----------------------
# Inicialização do app
# -----------------------
app = FastAPI(title="Chatbot Data API")


# -----------------------
# Modelos
# -----------------------
class ChatMessage(BaseModel):
    message: str

class NLQuery(BaseModel):
    question: str


# -----------------------
# Endpoint POST /chat
# -----------------------
@app.post("/chat")
def chat(message: ChatMessage):
    """
    Apenas ecoa a pergunta do usuário (placeholder para futura lógica de chat).
    """
    print("Pergunta do usuário:", message.message)
    return {"message": "Pergunta recebida"}


# -----------------------
# Endpoint GET /schema
# -----------------------
@app.get("/schema")
def schema():
    """
    Retorna o schema do CSV.
    """
    return {
        "columns": [{"name": c, "type": str(df[c].dtype)} for c in df.columns]
    }


# -----------------------
# Endpoint POST /nl-to-pandas
# -----------------------
@app.post("/nl-to-pandas")
def nl_to_pandas_endpoint(nl: NLQuery):
    """
    Recebe pergunta em linguagem natural → gera código Pandas e executa.
    """
    try:
        code, result = run_pandas_query(nl.question)
        return {
            "pandas_code": code,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}


# -----------------------
# Endpoint POST /query-with-insights
# -----------------------
@app.post("/query-with-insights")
def query_with_insights(nl: NLQuery):
    """
    Recebe pergunta → executa Pandas → retorna dados + insight em linguagem natural.
    """
    try:
        code, result = run_pandas_query(nl.question)
        if isinstance(result, pd.DataFrame) and result.empty:
            return {"text_insight": "Nenhum dado encontrado.", "data": []}

        # Se o resultado for DataFrame, converte para dict
        if isinstance(result, pd.DataFrame):
            data_dict = result.where(pd.notnull(result), None).to_dict(orient="records")
        else:
            data_dict = result  # números ou valores únicos

        # Gera insight em linguagem natural (apenas se for DataFrame)
        if isinstance(result, pd.DataFrame):
            text_insight = to_text_insight(result)
        else:
            text_insight = f"Resultado: {result}"

        return {
            "text_insight": text_insight,
            "data": data_dict
        }

    except Exception as e:
        return {"text_insight": f"Erro: {str(e)}", "data": []}
