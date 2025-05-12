import streamlit as st

# Configurações da página
st.set_page_config(page_title="Painel de Apoio à Recomposição", page_icon="📚", initial_sidebar_state="collapsed")


# CSS para plano de fundo com a imagem
st.markdown("""
    <style>
    /* Fundo com imagem */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/welnecker/questoesama/main/img/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Caixa de texto com fundo escuro sólido */
    .custom-text {
        background-color: #1c1c1c;  /* preto real */
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 18px;
        line-height: 1.6;
        color: #ffffff !important;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
    }

    /* Título principal com contraste */
    h3 {
        font-size: 28px;
        color: #ffffff;
        text-align: center;
        margin-top: 2rem;
        text-shadow: 1px 1px 3px #000;
    }

    /* Garante cor branca para todos textos internos */
    strong, u, b, p, li, span {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)


# Conteúdo com caixa semi-transparente
st.markdown("<h3 style='text-align: center;'>Painel de Apoio à Recomposição das Aprendizagens</h3>", unsafe_allow_html=True)

st.markdown("""
<div class="custom-text">
<p>Olá estudante, seja bem-vindo(a) ao <strong>Painel de Apoio à Recomposição das Aprendizagens</strong>.</p>

<p>Nele você terá a oportunidade de testar seu aprendizado e seus conhecimentos atuais em <strong>Matemática</strong> e <strong>Língua Portuguesa</strong>.</p>

<p><strong>Não perca esta oportunidade</strong>, responda com atenção e <strong>só envie as respostas quando tiver certeza</strong>, pois <strong>só há uma chance de envio</strong>.</p>

<p><strong>Bons estudos.</strong></p>

<p style='font-family:monospace; font-size:16px;'>Acesse a página <u><b>Estudante</b></u>, no menu lateral, e faça a atividade proposta pelo seu professor.</p>
</div>
""", unsafe_allow_html=True)

# Botão para ir à página do estudante
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
<div style="text-align: center; margin-top: 2rem;">
    <a href="/Estudante" target="_self" style="
        background-color: #3366cc;
        color: white;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    ">
        🎓 Ir para a página do Estudante
    </a>
</div>
""", unsafe_allow_html=True)

