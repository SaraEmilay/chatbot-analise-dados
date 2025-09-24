# nl_to_pandas.py
import re
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# -----------------------
# Carregar CSV
# -----------------------
df = pd.read_csv("credit_train.csv")
ALLOWED_COLUMNS = df.columns.tolist()

# -----------------------
# Modelo NLP
# -----------------------
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# -----------------------
# Dicionário de aliases
# -----------------------
COLUMN_ALIASES = {
    "idade": "IDADE",
    "uf": "UF",
    "sexo": "sexo",
    "alvo": "alvo",
    "classe social": "classe_social",
    "data de referência": "data_referencia",
    "crédito": "CREDITO",
}

# -----------------------
# Prompt template few-shot
# -----------------------
FEW_SHOT_PROMPT = f"""
Você é um assistente que transforma perguntas em código Pandas seguro.
O DataFrame se chama df.
Colunas disponíveis: {', '.join(ALLOWED_COLUMNS)}

Exemplo 1:
Pergunta: Qual a média de idade por UF?
Pandas esperado: df.groupby("UF")["IDADE"].mean()

Exemplo 2:
Pergunta: Quantos clientes são do sexo feminino?
Pandas esperado: df[df["sexo"] == "F"].shape[0]

Exemplo 3:
Pergunta: Quantos clientes são mau pagadores?
Pandas esperado: df[df["alvo"] == 1].shape[0]

Exemplo 4:
Pergunta: Qual a média de idade dos clientes que têm crédito acima de 1000?
Pandas esperado: df[df["CREDITO"] > 1000]["IDADE"].mean()

Agora gere apenas código Pandas seguro para a seguinte pergunta:
Pergunta: {{user_question}}
Pandas:
"""

# -----------------------
# Função principal
# -----------------------
def run_pandas_query(user_question: str):
    lower_q = user_question.lower()

    # Capturas rápidas - contagem por sexo
    if "sexo feminino" in lower_q:
        return 'df[df["sexo"] == "F"].shape[0]', df[df["sexo"] == "F"].shape[0]
    if "sexo masculino" in lower_q:
        return 'df[df["sexo"] == "M"].shape[0]', df[df["sexo"] == "M"].shape[0]

    # Capturas rápidas - idade
    match_idade_acima = re.search(r'idade\s*(acima|maior|mais)\s*(de|que)?\s*(\d+)', lower_q)
    if match_idade_acima:
        valor = int(match_idade_acima.group(3))
        return f'df[df["IDADE"] > {valor}].shape[0]', df[df["IDADE"] > valor].shape[0]

    match_idade_menor = re.search(r'idade\s*(menor|menos)\s*(de|que)?\s*(\d+)', lower_q)
    if match_idade_menor:
        valor = int(match_idade_menor.group(3))
        return f'df[df["IDADE"] < {valor}].shape[0]', df[df["IDADE"] < valor].shape[0]

    # Captura rápida - média de idade por UF
    if "média de idade por uf" in lower_q or "idade média por uf" in lower_q:
        return 'df.groupby("UF")["IDADE"].mean()', df.groupby("UF")["IDADE"].mean()

    # Captura rápida - média idade filtrada por crédito
    match_credito = re.search(r'cr[eé]dito\s*(acima|maior|mais)\s*(de|que)?\s*(\d+)', lower_q)
    if match_credito:
        valor = int(match_credito.group(3))
        return f'df[df["CREDITO"] > {valor}]["IDADE"].mean()', df[df["CREDITO"] > valor]["IDADE"].mean()

    # Se não entrou em captura rápida, gera via LLM
    prompt = FEW_SHOT_PROMPT.format(user_question=user_question)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150)
    pandas_code = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extrair código que começa com df
    match = re.search(r'(df[^\n;]*)', pandas_code)
    if not match:
        return pandas_code, "Não foi possível gerar código Pandas."
    pandas_code = match.group(1)

    # Executar código com segurança
    try:
        result = eval(pandas_code, {"df": df, "pd": pd})
    except Exception as e:
        result = f"Erro ao executar código: {e}"

    return pandas_code, result

# -----------------------
# Teste rápido (CLI)
# -----------------------
if __name__ == "__main__":
    print("Colunas detectadas no CSV:", ALLOWED_COLUMNS)
    perguntas = [
        "Qual a média de idade por UF?",
        "Quantos clientes são do sexo feminino?",
        "Quantos clientes são do sexo masculino?",
        "Quantos clientes têm mais de 30 anos?",
        "Quantos clientes têm mais de 25 anos?",
        "Qual a média de idade dos clientes com crédito acima de 1000?"
    ]
    for p in perguntas:
        code, res = run_pandas_query(p)
        print(f"\nPergunta: {p}")
        print("Código Pandas gerado:", code)
        print("Resultado:", res)
