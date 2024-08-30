import streamlit as st
import cohere
import os

from dotenv import load_dotenv

load_dotenv()

# Substitua pelo seu token de acesso da Cohere
COHERE_API_KEY = os.environ["COHERE_API_KEY"]

# Inicialize o cliente da Cohere
co = cohere.Client(COHERE_API_KEY)

st.title("Icaro GPT com Cohere!🚀")

# Inicializar 'messages' no session_state se não existirem
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibir as mensagens já presentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Receber entrada do usuário
if user_prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Gerar resposta do assistente usando a API Cohere
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Chamada para a API do Cohere
        response = co.generate(
            model='command-xlarge-nightly',  # Use um modelo adequado da Cohere
            prompt=user_prompt,
            max_tokens=300,  # Ajuste conforme necessário
            temperature=0.5  # Ajuste conforme necessário
        )

        if response:
            full_response = response.generations[0].text.strip()
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.markdown("Erro ao se conectar à API Cohere.")

        # Armazenar a resposta do assistente
        st.session_state.messages.append({"role": "assistant", "content": full_response})
