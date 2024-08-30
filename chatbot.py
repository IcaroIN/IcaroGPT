import streamlit as st
import requests
import os

from dotenv import load_dotenv

load_dotenv()

# Substitua pelo seu token de acesso da Hugging Face
HUGGING_FACE_API_KEY = os.environ["HUGGING_FACE_API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

st.title("Icaro GPT com Hugging Face!🚀")

# Inicializar 'messages' no session_state se não existirem
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir as mensagens já presentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Receber entrada do usuário
if user_prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Preparando o payload para enviar para a API do Hugging Face
    payload = {
        "inputs": user_prompt,
        "options": {
            "wait_for_model": True,
        }
    }

    # Gerar resposta do assistente usando a API Hugging Face
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            full_response = response_json[0]['generated_text']
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.markdown("Erro ao se conectar à API Hugging Face.")

        # Armazenar a resposta do assistente
        st.session_state.messages.append({"role": "assistant", "content": full_response})
