import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata
import time
import sys
import os

# 👉 Adiciona o caminho do projeto raiz para encontrar a pasta 'utils'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils.envio_respostas import enviar_respostas_em_blocos, escolher_credencial_aleatoria

st.set_page_config(page_title="Atividade Online AMA 2025", page_icon="✨")

st.subheader("Preencha abaixo somente seu nome completo, o código da atividade (em MAIÚSCULAS) e clique no botão Gerar Atividade:")

if "nome_estudante" not in st.session_state:
    st.session_state.nome_estudante = ""

if not st.session_state.get("atividades_em_exibicao"):
    st.session_state.nome_estudante = st.text_input("Nome do(a) Estudante:")
else:
    st.text_input("Nome do(a) Estudante:", value=st.session_state.nome_estudante, disabled=True)

st.subheader("Digite abaixo o código fornecido pelo(a) professor(a):")
codigo_atividade = st.text_input("Código da atividade (ex: ABC123):").strip().upper()

if "codigo_digitado" not in st.session_state:
    st.session_state.codigo_digitado = ""

if codigo_atividade:
    st.session_state.codigo_digitado = codigo_atividade

codigo_atividade = st.session_state.codigo_digitado

escola = st.session_state.get("escola_estudante", "")
turma = st.session_state.get("turma_estudante", "")
st.text_input("Escola:", value=escola, disabled=True)
st.text_input("Turma:", value=turma, disabled=True)

def normalizar_texto(txt):
    txt = txt.lower().strip()
    txt = ''.join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')
    return ''.join(c for c in txt if c.isalnum())

def gerar_id_unico(nome, escola, turma, codigo):
    return f"{normalizar_texto(nome)}_{normalizar_texto(escola)}_{normalizar_texto(turma)}_{normalizar_texto(codigo)}"

@st.cache_data(show_spinner=False, ttl=60)
def carregar_atividades():
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId="17SUODxQqwWOoC9Bns--MmEDEruawdeEZzNXuwh3ZIj8",
            range="ATIVIDADES_GERADAS!A1:Z"
        ).execute()

        values = result.get("values", [])
        if not values or len(values) < 2:
            return pd.DataFrame(columns=["CODIGO"])

        header = [col.strip().upper() for col in values[0]]
        rows = [row + [None] * (len(header) - len(row)) for row in values[1:]]
        df = pd.DataFrame(rows, columns=header)
        df["CODIGO"] = df["CODIGO"].astype(str).str.strip().str.upper()
        return df

    except Exception as e:
        st.error(f"Erro ao carregar atividades: {e}")
        return pd.DataFrame(columns=["CODIGO"])

@st.cache_data(show_spinner=False)
def carregar_gabarito():
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId="17SUODxQqwWOoC9Bns--MmEDEruawdeEZzNXuwh3ZIj8",
            range="MATEMATICA!A1:N"
        ).execute()
        values = result.get("values", [])
        if not values or len(values) < 2:
            return pd.DataFrame(columns=["ATIVIDADE", "GABARITO"])
        header = [col.strip().upper() for col in values[0]]
        rows = [row + [None] * (len(header) - len(row)) for row in values[1:]]
        df = pd.DataFrame(rows, columns=header)
        df["ATIVIDADE"] = df["ATIVIDADE"].astype(str).str.strip()
        df["GABARITO"] = df["GABARITO"].astype(str).str.strip().str.upper()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar gabarito: {e}")
        return pd.DataFrame()

if st.session_state.get("limpar_atividade"):
    st.cache_data.clear()
    chaves_para_limpar = [
        "atividades_em_exibicao", "codigo_digitado", "escola_estudante",
        "turma_estudante", "nome_estudante"
    ]
    for chave in chaves_para_limpar:
        st.session_state.pop(chave, None)
    for chave in list(st.session_state.keys()):
        if chave.startswith("resp_"):
            st.session_state.pop(chave)
    st.session_state.pop("limpar_atividade", None)
    st.rerun()

# ✨ Reexibir o botão Gerar Atividade (corrigido)
if not st.session_state.get("atividades_em_exibicao") and st.session_state.nome_estudante and codigo_atividade:
    if st.button("🗕️ Gerar Atividade"):
        st.session_state["atividades_em_exibicao"] = True
        st.rerun()
