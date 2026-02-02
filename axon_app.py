import streamlit as st
from groq import Groq

# Configuração da página
st.set_page_config(page_title="Axon Mentor", page_icon="🧠")

st.title("🧠 Axon: Seu Mentor de Inglês")

# Sua chave da Groq
minha_chave = "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" 

client = Groq(api_key=minha_chave)

# Inicializa o histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é o Axon, mentor de inglês. Use 60% PT e 40% EN. Sempre termine com uma pergunta em inglês."}
    ]

# Exibe o chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada do usuário
if prompt := st.chat_input("Fale com o Axon..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Resposta da IA
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Erro na conexão: {e}")