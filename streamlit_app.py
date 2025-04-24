import streamlit as st

# Configuração da página
st.set_page_config(page_title="Painel AMA 2025", page_icon="🎓")

st.markdown("## Painel de Apoio à Recomposição das Aprendizagens")

st.markdown("""
Olá estudante, seja bem-vindo(a) ao **Painel de Apoio à Recomposição das Aprendizagens**.

Nele você terá a oportunidade de testar seu aprendizado e seus conhecimentos atuais em **Matemática** e **Língua Portuguesa**.

**Não perca esta oportunidade.**  
Responda com atenção e **só envie as respostas quando tiver certeza**, pois **só há uma oportunidade de envio**.

**Bons estudos.**
""")

# Frase final com fonte diferente
st.markdown("""
<p style='font-family: Georgia, serif; font-size: 18px; color: #444; margin-top: 30px;'>
Acesse a página <strong>Estudante</strong>, no menu lateral, e faça a atividade proposta pelo seu professor.
</p>
""", unsafe_allow_html=True)


