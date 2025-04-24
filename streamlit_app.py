import streamlit as st

# Configuração da página
st.set_page_config(page_title="Painel AMA 2025", page_icon="🎓")

# Título centralizado com fonte maior
st.markdown("""
<h1 style='text-align: center; font-size: 32px;'>
    Painel de Apoio à Recomposição das Aprendizagens
</h1>
""", unsafe_allow_html=True)

# Espaçamento
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# Texto de orientação com ênfase na palavra "Estudante"
st.markdown("""
<h4 style='font-size: 20px;'>
    Acesse a página <b><u>Estudante</u></b>, no menu lateral, e faça a atividade proposta pelo seu professor.
</h4>
""", unsafe_allow_html=True)

# Espaçamento
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# Texto explicativo dividido e com fonte maior
st.markdown("""
<div style='font-size: 18px; line-height: 1.6;'>
    <p>Olá estudante, seja bem-vindo(a) ao <strong>Painel de Apoio à Recomposição das Aprendizagens</strong>.</p>

    <p>Nele você terá a oportunidade de testar seu aprendizado e seus conhecimentos atuais em <strong>Matemática</strong> e <strong>Língua Portuguesa</strong>.</p>

    <p><strong>Não perca esta oportunidade.</strong> Responda com atenção e <strong>só envie as respostas quando tiver certeza</strong>, pois <strong>só há uma oportunidade de envio</strong>.</p>

    <p><strong>Bons estudos.</strong></p>
</div>
""", unsafe_allow_html=True)
