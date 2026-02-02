import streamlit as st
from groq import Groq
from gtts import gTTS
import io

st.set_page_config(page_title="Axon Mentor", page_icon="🧠")

st.title("🧠 Axon: Seu Mentor de Inglês")

# --- SUA CHAVE (Lembre-se de pegar uma NOVA se der erro 401) ---
minha_chave = "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" 
client = Groq(api_key=minha_chave)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Você é o Axon, mentor de inglês. Use 60% PT e 40% EN. Sempre termine com uma pergunta em inglês."}
    ]

# Função para gerar e tocar o áudio
def tocar_audio(texto):
    # Criamos o áudio com sotaque em inglês
    tts = gTTS(text=texto, lang='en', tld='com') 
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    # Exibe o player e toca automaticamente
    st.audio(audio_fp, format='audio/mp3', autoplay=True)

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
            axon_reply = response.choices[0].message.content
            st.markdown(axon_reply)
            
            # O Axon fala agora!
            tocar_audio(axon_reply)
            
            st.session_state.messages.append({"role": "assistant", "content": axon_reply})
        except Exception as e:
            st.error(f"Erro: {e}")