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
st.markdown("## Painel de Apoio à Recomposição das Aprendizagens")

st.markdown("""
**Acesse a página _Estudante_, no menu lateral, e faça a atividade proposta pelo seu professor.**

Olá estudante, seja bem-vindo(a) ao **Painel de Apoio à Recomposição das Aprendizagens**.

Nele você terá a oportunidade de testar seu aprendizado e seus conhecimentos atuais em **Matemática** e **Língua Portuguesa**.

**Não perca esta oportunidade.**  
Responda com atenção e **só envie as respostas quando tiver certeza**, pois **só há uma oportunidade de envio**.

**Bons estudos.**
""")


