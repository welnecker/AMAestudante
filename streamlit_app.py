import streamlit as st

# Configurações da página
st.set_page_config(page_title="Painel de Apoio à Recomposição", page_icon="📚")

# CSS para plano de fundo com a imagem
st.markdown("""
    <style>
    /* Fundo da aplicação com imagem */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/welnecker/questoesama/main/img/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Caixa de texto com fundo escuro translúcido */
    .custom-text {
        background-color: rgba(0, 0, 0, 0.7);  /* fundo preto com opacidade */
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 18px;
        line-height: 1.6;
        color: #ffffff !important;
    }

    /* Título principal */
    h3 {
        font-size: 28px;
        color: #ffffff;
        text-align: center;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6);
        font-weight: bold;
    }

    strong, u, b, p, li {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)
