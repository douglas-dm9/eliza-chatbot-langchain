# python 3.8 (3.8.16) or it doesn't work
# pip install streamlit streamlit-chat langchain python-dotenv
import streamlit as st
from streamlit_chat import message
import os

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)


def init():
    # Load the OpenAsI API key from the environment variable
    os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

    # setup streamlit page
    st.set_page_config(
        page_title="ELIZA - Terapeuta Virtual",
        page_icon="🤖"
    )


def main():
    init()

    chat = ChatOpenAI(temperature=0.5)

    # initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="Você vai atuar como Eliza, uma terapeuta virtual avançada.\
                           Você fará perguntas individualmente para compreender suas emoções e\
                           sentimentos, permitindo uma compreensão mais profunda do usuário (paciente).\
                           Essa abordagem resulta em respostas mais precisas e empáticas por sua parte.")\
        ]

    st.header("ELIZA - Terapeuta Virtual 🤖")

    # sidebar with user input
    with st.sidebar:
        user_input_to_show = st.text_input("Your message: ", key="user_input")
        user_input_to_chat = user_input_to_show+("Responda como o chatbot ELIZA de 1965")

        # handle user input
        if user_input_to_show:
            st.session_state.messages.append(HumanMessage(content=user_input_to_chat))
            with st.spinner("Thinking..."):
                response = chat(st.session_state.messages)
            st.session_state.messages.append(
                AIMessage(content=response.content))
            
    # display message history
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):
        if i % 2 == 0:
            message(msg.content[:-37], is_user=True, key=str(i) + '_user')
        else:
            message(msg.content, is_user=False, key=str(i) + '_ai')


if __name__ == '__main__':
    main()
