# Chatbot de Análise de Dados
 (link do arquivo de video funcionando no google drive: https://drive.google.com/file/d/1kLreNXW2TpQCky-cc_eYyA5rhQESblEq/view?usp=sharing )
Este projeto é um **chatbot de análise de dados** que permite fazer perguntas em linguagem natural sobre um dataset e obter respostas em **código Pandas**, resultado e insights.

O chatbot utiliza:
- Python
- Pandas
- Streamlit
- Modelo NLP `google/flan-t5-small` para transformar perguntas em código Pandas seguro.

---

# 📁 Estrutura do projeto

chatbot-analise-dados/
├─ app/ # Código Python principal
├─ data/ # CSVs de exemplo
├─ demo/ # Exemplos de uso
├─ README.md
├─ requirements.txt
├─ streamlit_app.py


---

# ⚡ Pré-requisitos

- Python >= 3.10  
- Git  
- Streamlit  

> Recomenda-se criar um **ambiente virtual** (`venv`) para instalar as dependências.

---
# 🎯 Como usar

Digite perguntas sobre os dados e o chatbot retornará:

Código Pandas correspondente à consulta

Resultado da consulta

Insight em linguagem natural

Prévia dos dados (se aplicável)

# 📌 Observações

A pasta venv/ não é enviada ao GitHub.

Dataset de exemplo: credit_train.csv. (link do arquivo no google drive: https://drive.google.com/drive/folders/1lr_Ooi4XROpp8XPwESlpsLyFkLkY8IL7?usp=sharing)

Se desejar, use seu próprio CSV, mas certifique-se de que as colunas estejam consistentes com as esperadas pelo chatbot (REF_DATE, TARGET, VAR1… etc.).

# 🛠️ Instalação e execução

1. Clone o repositório:

```bash
git clone https://github.com/SaraEmilay/chatbot-analise-dados.git
cd chatbot-analise-dados
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
pip install pandas streamlit transformers torch


streamlit run streamlit_app.py


