import streamlit as st
import dotenv
from Bot import Bot


def main():
    dotenv.load_dotenv()
    # App page config
    st.set_page_config(page_title="Vestibot Unicamp", page_icon=":books:", layout="wide")
    st.header("Vestibot Unicamp 2025:books:")
    #st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # Initialize chatbot
    if "bot" not in st.session_state:
        st.session_state.bot = Bot()


    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
                        
    # Get user input
    if user_input := st.chat_input("Tire suas dúvidas sobre o vestibular Unicamp 2025!"):
        st.chat_message("user").markdown(user_input)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        response = st.session_state.bot.get_reponse(user_input, st.session_state.conversation)
        st.chat_message("assistant").markdown(response)
        st.session_state.conversation.append({"role": "assistant", "content": response})

        
if __name__ == '__main__':
    main()