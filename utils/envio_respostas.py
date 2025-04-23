import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata
import time
import sys
import os
import json

# Ajusta o caminho para permitir importações do nível raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils.envio_respostas import enviar_respostas_em_blocos, escolher_credencial_aleatoria

st.set_page_config(page_title="Atividade Online AMA 2025", page_icon="✨")

st.subheader("Preencha seus dados abaixo:")

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

# Simulação: quando tiver as linhas preenchidas, envie
if st.button("📤 Enviar respostas de teste"):
    try:
        # Lê credenciais do secrets
        credenciais_dict = {
            "cred1": json.loads(st.secrets["gcp_service_accounts"]["cred1"]),
            "cred2": json.loads(st.secrets["gcp_service_accounts"]["cred2"]),
            "cred3": json.loads(st.secrets["gcp_service_accounts"]["cred3"])
        }

        # Escolhe aleatoriamente uma credencial
        credencial_escolhida = escolher_credencial_aleatoria(credenciais_dict)

        # Simulação de uma linha de resposta
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linha_teste = [[agora, codigo_atividade, st.session_state.nome_estudante, "Simulação", "A", "Certo"]]

        enviar_respostas_em_blocos(linha_teste, credencial_escolhida)
        st.success("✅ Respostas enviadas com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao enviar respostas: {e}")
