# --- IMPORTAÇÕES ---
import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata
import time
import sys
import os
import re
import streamlit.components.v1 as components
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils.envio_respostas import enviar_respostas_em_blocos, escolher_credencial_aleatoria

# --- FUNÇÃO AUXILIAR ---
def limpar_nome_atividade(atividade):
    """Remove a extensão .jpg, mantendo letras e prefixos intactos."""
    return atividade.strip().replace(".jpg", "")

def gerar_id_unico(nome, escola, turma, codigo):
    """Gera um identificador único em maiúsculas baseado em nome + escola + turma + código."""
    return f"{nome.strip().upper()}__{escola.strip().upper()}__{turma.strip().upper()}__{codigo.strip().upper()}"

@st.cache_data(ttl=300, show_spinner=False)
def verificar_resposta_enviada(id_unico):
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId="17SUODxQqwWOoC9Bns--MmEDEruawdeEZzNXuwh3ZIj8",
            range="ATIVIDADES!A1:Z"
        ).execute()
        values = result.get("values", [])[1:]
        for linha in values:
            if id_unico in ' '.join(linha):
                return True
        return False
    except Exception as e:
        st.warning(f"⚠️ Erro ao verificar respostas anteriores: {e}")
        return False

# --- CONFIGURAÇÃO STREAMLIT ---
st.set_page_config(page_title="Atividade Online AMA 2025", page_icon="✨")

# --- INICIALIZA VARIÁVEIS DE ESTADO ---
for chave in ["nome_estudante", "codigo_digitado", "respostas_enviadas", "respostas_salvas", "dados_atividades"]:
    if chave not in st.session_state:
        if chave == "respostas_enviadas":
            st.session_state[chave] = set()
        elif chave == "respostas_salvas":
            st.session_state[chave] = {}
        elif chave == "dados_atividades":
            pass
        else:
            st.session_state[chave] = ""

# --- ENTRADA DO USUÁRIO ---
st.subheader("Preencha abaixo somente seu nome completo, o código da atividade (em MAIÚSCULAS) e clique no botão Gerar Atividade:")
if not st.session_state.get("atividades_em_exibicao"):
    st.session_state.nome_estudante = st.text_input("Nome do(a) Estudante:")
else:
    st.text_input("Nome do(a) Estudante:", value=st.session_state.nome_estudante, disabled=True)

st.subheader("Digite abaixo o código fornecido pelo(a) professor(a):")
codigo_atividade = st.text_input("Código da atividade (ex: ABC123):").strip().upper()
if codigo_atividade:
    st.session_state.codigo_digitado = codigo_atividade
codigo_atividade = st.session_state.codigo_digitado
nome_aluno = st.session_state.get("nome_estudante", "")

# --- CARREGAMENTO DAS ATIVIDADES E GABARITO ---
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
        URLS = {
            "matematica": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhv1IMZCz0xYYNGiEIlrqzvsELrjozHr32CNYHdcHzVqYWwDUFolet_2XOxv4EX7Tu3vxOB4w-YUX9/pub?gid=2127889637&single=true&output=csv",
            "portugues": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQhv1IMZCz0xYYNGiEIlrqzvsELrjozHr32CNYHdcHzVqYWwDUFolet_2XOxv4EX7Tu3vxOB4w-YUX9/pub?gid=1217179376&single=true&output=csv"
        }
        url = URLS.get(st.session_state.get("disciplina", "matematica"), URLS["matematica"])
        df = pd.read_csv(url)
        df["ATIVIDADE"] = df["ATIVIDADE"].astype(str).str.strip()
        df["GABARITO"] = df["GABARITO"].astype(str).str.strip()
        df["ATIVIDADE_NORMALIZADA"] = df["ATIVIDADE"].apply(limpar_nome_atividade)
        return df
    except Exception as e:
        st.warning(f"⚠️ Falha ao carregar gabarito: {e}")
        return pd.DataFrame(columns=["ATIVIDADE", "GABARITO", "ATIVIDADE_NORMALIZADA"])

# --- PROCESSAMENTO DO CÓDIGO ---
if "dados_atividades" not in st.session_state:
    st.session_state.dados_atividades = carregar_atividades()

dados = st.session_state.dados_atividades
linha_codigo = dados[dados["CODIGO"] == codigo_atividade]
if not linha_codigo.empty:
    st.session_state["escola_estudante"] = linha_codigo.iloc[0].get("ESCOLA", "")
    st.session_state["turma_estudante"] = linha_codigo.iloc[0].get("TURMA", "")

escola = st.session_state.get("escola_estudante", "")
turma = st.session_state.get("turma_estudante", "")
st.text_input("Escola:", value=escola, disabled=True)
st.text_input("Turma:", value=turma, disabled=True)

id_unico = gerar_id_unico(nome_aluno, escola, turma, codigo_atividade)
ja_respondeu = verificar_resposta_enviada(id_unico)
codigo_valido = not linha_codigo.empty

# --- BOTÕES ---
col1, col2 = st.columns([3, 2])
with col1:
    if "gerar_clicado" not in st.session_state:
        st.session_state.gerar_clicado = False

    gerar = st.button("🗕️ Gerar Atividade", disabled=st.session_state.gerar_clicado)

    if gerar:
        st.session_state.gerar_clicado = True
        st.rerun()

with col2:
    st.info("ℹ️ Clique duas vezes no botão abaixo para Reiniciar:")
    if st.button("🔄 Reiniciar Tudo"):
        with st.spinner("Reiniciando tudo..."):
            st.cache_data.clear()
            st.session_state.clear()
            st.session_state.gerar_clicado = False  # Garante que o botão será reativado

            components.html("<script>window.location.reload(true);</script>", height=0)

if st.session_state.get("gerar_clicado") and not st.session_state.get("atividades_em_exibicao"):

    if not all([st.session_state.get("nome_estudante", "").strip(), codigo_atividade.strip()]):
        st.warning("⚠️ Por favor, preencha os campos Nome e Código.")
        st.stop()
    if not codigo_valido:
        st.warning("⚠️ Código da atividade inválido.")
        st.stop()
    if ja_respondeu:
        st.error(
            f"❌ Você já enviou essa atividade.\n\n"
            f"Nome: **{nome_aluno.strip()}**\n"
            f"Código: **{codigo_atividade}**\n"
            f"Turma: **{turma}** — Escola: **{escola}**"
        )
        st.stop()
    st.session_state["atividades_em_exibicao"] = True
    st.rerun()

# --- EXIBIÇÃO DAS QUESTÕES E ENVIO ---
# (continua normalmente conforme o restante do seu script...)


# --- EXIBIÇÃO DAS QUESTÕES E ENVIO DAS RESPOSTAS ---

# Se atividade foi finalizada, exibe botão "Finalizar"
if st.session_state.get("atividade_finalizada") and not st.session_state.get("atividade_encerrada"):
    if st.button("✅ Finalizar"):
        st.session_state["atividade_encerrada"] = True
        st.success("🎉 Atividade Finalizada. Obrigado.")
    st.stop()
elif st.session_state.get("atividade_encerrada"):
    st.success("🎉 Atividade Finalizada. Obrigado.")
    st.stop()
dados = st.session_state.dados_atividades = carregar_atividades()
linha_codigo = dados[dados["CODIGO"] == codigo_atividade]
if not linha_codigo.empty:
    st.session_state["escola_estudante"] = linha_codigo.iloc[0].get("ESCOLA", "")
    st.session_state["turma_estudante"] = linha_codigo.iloc[0].get("TURMA", "")

escola = st.session_state.get("escola_estudante", "")
turma = st.session_state.get("turma_estudante", "")
id_unico = gerar_id_unico(nome_aluno, escola, turma, codigo_atividade)
ja_respondeu = verificar_resposta_enviada(id_unico)

if linha_codigo.empty:
    st.warning("⚠️ Código da atividade inválido.")
elif ja_respondeu:
    st.warning("⚠️ Você já respondeu essa atividade.")
else:
    atividades = [
        linha_codigo[col].values[0] for col in linha_codigo.columns if col.startswith("ATIVIDADE") and linha_codigo[col].values[0]
    ]
    disciplina = str(linha_codigo["DISCIPLINA"].values[0]).strip().lower() if "DISCIPLINA" in linha_codigo.columns else "matematica"
    base_url = "https://raw.githubusercontent.com/welnecker/questoesama/main"
    pasta = "matematica" if disciplina == "matematica" else "portugues"

    st.session_state["atividades_em_exibicao"] = True
    respostas = {}
    for idx, atividade in enumerate(atividades):
        st.markdown(f"### Questão {idx + 1}")
        url = f"{base_url}/{pasta}/{atividade.strip()}"
        st.image(url, use_container_width=True)
        if st.session_state.get("atividade_finalizada"):
            resposta_salva = st.session_state.respostas_salvas.get(id_unico, {}).get(atividade, "❓")
            st.radio("Escolha a alternativa:", ["A", "B", "C", "D", "E"], key=f"resp_{idx}", index=None, disabled=True)
            st.markdown(f"**Resposta enviada:** {resposta_salva}")
        else:
            respostas[atividade] = st.radio("Escolha a alternativa:", ["A", "B", "C", "D", "E"], key=f"resp_{idx}", index=None)

    if st.button("📤 Enviar Respostas"):
        if any(r is None for r in respostas.values()):
            st.warning("⚠️ Há questões não respondidas.")
            st.stop()

        try:
            gabarito_df = carregar_gabarito()
            acertos = 0
            acertos_detalhe = {}
            linha_envio = [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                id_unico,
                codigo_atividade,
                nome_aluno,
                escola,
                turma,
            ]
            for atividade, resposta in respostas.items():
                atividade_limpa = limpar_nome_atividade(atividade)
                linha_gabarito = gabarito_df[gabarito_df["ATIVIDADE_NORMALIZADA"] == atividade_limpa]
                gabarito = linha_gabarito["GABARITO"].values[0] if not linha_gabarito.empty else "?"
                situacao = "Certo" if resposta.upper() == gabarito.upper() else "Errado"
                if situacao == "Certo":
                    acertos += 1
                acertos_detalhe[atividade] = situacao
                linha_envio.extend([atividade, resposta, situacao])

            contas = st.secrets["gcp_service_accounts"]
            cred = escolher_credencial_aleatoria({
                "cred1": contas["cred1"],
                "cred2": contas["cred2"],
                "cred3": contas["cred3"]
            })

            with st.spinner("Enviando suas respostas... Aguarde."):
                enviar_respostas_em_blocos([linha_envio], credencial=cred)

            st.session_state.respostas_enviadas.add(id_unico)
            st.session_state.respostas_salvas[id_unico] = acertos_detalhe

            st.success(f"✅ Respostas enviadas com sucesso! Você acertou {acertos}/{len(respostas)}")
            for idx, atividade in enumerate(atividades):
                situacao = acertos_detalhe.get(atividade, "❓")
                cor = "✅" if situacao == "Certo" else "❌"
                st.markdown(f"**Questão {idx+1}:** {cor} ({situacao})")

            # Botão de finalização opcional
            st.session_state["atividade_finalizada"] = True

        except Exception as e:
            st.error(f"❌ Erro ao enviar respostas: {e}")

#