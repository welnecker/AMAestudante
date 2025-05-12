import streamlit as st

# Configurações da página
st.set_page_config(page_title="Painel de Apoio à Recomposição", page_icon="📚")

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
