import streamlit as st

# Configurações da página
st.set_page_config(page_title="Painel de Apoio à Recomposição", page_icon="📚")

# CSS para plano de fundo com a imagem
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/welnecker/questoesama/main/img/fundo.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .custom-text {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 1.5rem;
        border-radius: 12px;
        font-size: 18px;
        line-height: 1.6;
    }
    h3 {
        font-size: 28px;
        color: #003366;
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
