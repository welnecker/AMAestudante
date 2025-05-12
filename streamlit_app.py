import streamlit as st

# Configurações da página
st.set_page_config(page_title="Painel de Apoio à Recomposição", page_icon="📚")

# CSS para plano de fundo com a imagem
st.markdown("""
    <style>
    /* Fundo da aplicação */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/welnecker/questoesama/main/img/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #111 !important;
    }

    /* Caixa de texto com contraste e legibilidade */
    .custom-text {
        background-color: rgba(255, 255, 255, 0.92); /* mais opaco para leitura */
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 18px;
        line-height: 1.6;
        color: #111 !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
    }

    /* Título principal */
    h3 {
        font-size: 28px;
        color: #002244;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.7);
        text-align: center;
        font-weight: bold;
    }

    strong {
        color: #000 !important;
    }

    p, b, u, li {
        color: #111 !important;
    }
    </style>
""", unsafe_allow_html=True)
