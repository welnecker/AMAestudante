import streamlit as st

# Configuração da página
st.set_page_config(page_title="Painel AMA 2025", page_icon="🎓")

# Título com fonte menor e centralizado
st.markdown("<h3 style='text-align: center;'>Painel de Apoio à Recomposição das Aprendizagens</h3>", unsafe_allow_html=True)

# Texto de instrução principal
st.markdown("""
### Acesse a página <b><u>Estudante</u></b>, no menu lateral, e faça a atividade proposta pelo seu professor.
""", unsafe_allow_html=True)

# Texto explicativo adicional
st.markdown("""
Olá estudante, seja bem-vindo(a) ao Painel de Apoio à Recomposição das Aprendizagens.  
Nele você terá oportunidade de testar seu aprendizado e seus conhecimentos atuais em **Matemática** e **Língua Portuguesa**.  
Não perca esta oportunidade. Responda com atenção e **só envie as respostas quando tiver certeza**, pois **só há uma oportunidade de envio**.

**Bons estudos.**
""")
