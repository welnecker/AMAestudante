# --- IMPORTAÇÕES ---
import streamlit as st
import pandas as pd
from datetime import datetime
import unicodedata
import time
import sys
import os
import streamlit.components.v1 as components
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils.envio_respostas import enviar_respostas_em_blocos, escolher_credencial_aleatoria

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

# --- INTERFACE INICIAL ---
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

id_unico = gerar_id_unico(st.session_state.get("nome_estudante", ""), escola, turma, codigo_atividade)
codigo_valido = not linha_codigo.empty
ja_respondeu = id_unico in st.session_state.respostas_enviadas

# 🎯 BOTÕES "Gerar Atividade" e "Reiniciar Tudo"
col1, col2 = st.columns([3, 2])
with col1:
    gerar = st.button("🗕️ Gerar Atividade")
with col2:
    st.info("ℹ️ Clique duas vezes no botão abaixo para Reiniciar:")
    if st.button("🔄 Reiniciar Tudo"):
        with st.spinner("Reiniciando tudo..."):
            st.cache_data.clear()
            st.session_state.clear()
            components.html("<script>window.location.reload(true);</script>", height=0)

if gerar and not st.session_state.get("atividades_em_exibicao"):
    if not all([st.session_state.get("nome_estudante", "").strip(), codigo_atividade.strip()]):
        st.warning("⚠️ Por favor, preencha os campos Nome e Código.")
        st.stop()
    if not codigo_valido:
        st.warning("⚠️ Código da atividade inválido.")
        st.stop()
    st.session_state["atividades_em_exibicao"] = True
    st.rerun()

# --- EXIBIÇÃO DAS QUESTÕES ---
if st.session_state.get("atividades_em_exibicao"):
    linha = dados[dados["CODIGO"] == codigo_atividade.upper()]
    atividades = [
        linha[col].values[0] for col in linha.columns if col.startswith("ATIVIDADE") and linha[col].values[0]
    ]
    st.subheader("Responda cada questão marcando uma alternativa:")

    respostas = {}

    try:
        disciplina = str(linha["DISCIPLINA"].values[0]).strip().lower()
    except:
        disciplina = "matematica"

    base_url = "https://raw.githubusercontent.com/welnecker/questoesama/main"
    pasta = "matematica" if disciplina == "matematica" else "portugues"

    for idx, atividade in enumerate(atividades):
        st.markdown(f"### Questão {idx + 1}")
        url = f"{base_url}/{pasta}/{atividade}.jpg"
        st.image(url, use_container_width=True)

        if ja_respondeu:
            resposta_salva = st.session_state.respostas_salvas.get(id_unico, {}).get(atividade, "❓")
            st.radio("Escolha a alternativa:", ["A", "B", "C", "D", "E"], key=f"resp_{idx}", index=None, disabled=True)
            st.markdown(f"**Resposta enviada:** {resposta_salva}")
        else:
            resposta = st.radio("Escolha a alternativa:", ["A", "B", "C", "D", "E"], key=f"resp_{idx}", index=None)
            respostas[atividade] = resposta



    if not ja_respondeu:
        if st.button("📤 Enviar Respostas"):
            if id_unico in st.session_state.respostas_enviadas:
                st.warning("❌ Você já respondeu essa atividade.")
                st.stop()

            if any(r is None for r in respostas.values()):
                st.warning("⚠️ Há questões não respondidas.")
                st.stop()

            try:
                gabarito_df = carregar_gabarito()
                acertos = 0
                acertos_detalhe = {}
                linha_envio = [
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    codigo_atividade,
                    nome_aluno,
                    escola,
                    turma,
                ]
                for atividade, resposta in respostas.items():
                    linha_gabarito = gabarito_df[gabarito_df["ATIVIDADE"] == atividade]
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
                    start = time.time()
                    enviar_respostas_em_blocos([linha_envio], credencial=cred)
                    fim = time.time()

                st.session_state.respostas_enviadas.add(id_unico)
                st.session_state.respostas_salvas[id_unico] = acertos_detalhe
                st.success(f"✅ Respostas enviadas! Você acertou {acertos}/{len(respostas)}. Tempo: {fim - start:.2f}s")
                st.balloons()
                st.markdown(
                    """
                    <div style='
                        background-color: #d4edda;
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        font-size: 24px;
                        font-weight: bold;
                        color: #155724;
                        border: 2px solid #c3e6cb;
                        margin-top: 20px;
                    '>
                        🎉 Atividade concluída com sucesso!
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Aguarda 3 segundos e reroda
            #    time.sleep(3)
             #   st.rerun()



            except Exception as e:
                st.error(f"❌ Erro ao enviar respostas: {e}")

    elif ja_respondeu:
        acertos_detalhe = st.session_state.respostas_salvas.get(id_unico, {})
        st.markdown("---")
        for idx, atividade in enumerate(atividades):
            situacao = acertos_detalhe.get(atividade, "❓")
            cor = "✅" if situacao == "Certo" else "❌"
            st.markdown(f"**Questão {idx+1}:** {cor}")
        st.markdown("---")

        st.info("ℹ️ Clique duas vezes no botão abaixo para limpar a atividade.")
if st.button("🔄 Limpar Atividade"):
    with st.spinner("🧹 Aguarde, limpando a atividade..."):
        st.cache_data.clear()
        st.session_state.clear()
        components.html(
            "<script>window.location.reload(true);</script>",
            height=0,
        )
        
#
