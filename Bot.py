import os

from langchain_groq import ChatGroq
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

class Bot():
    def __init__(self):
        self.api_key = st.secrets["GROQ_API_KEY"]
        self.llm_model = ChatGroq(
            model="llama3-70b-8192",
            temperature=0,
            api_key=self.api_key,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
        with open('data/base_text.txt', 'r', encoding='utf-8') as file:
            text = file.read()

        text_chunks = self.create_text_chunk(text)

        vectorstore = self.create_vectorstore(text_chunks)

        self.retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":4})

        self.prompt_template = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """Você é um assistente que responde perguntas sobre o Vestibular da Unicamp 2025 a partir da publicação da Resolução GR-029/2024, de 10/07/2024 que "Dispõe sobre o Vestibular Unicamp 2025 para vagas no ensino de Graduação.
                Considere o histórico da conversa: \n{chat_history}\n, o contexto: {context} e a pergunta: {question} para gerar a resposta.
                Se não souber a resposta ou não tiver informações o suficiente, diga que não sabe. Não minta ou invente informações."""),
            HumanMessagePromptTemplate.from_template(
                """Pergunta:{question}"""),
        ])

    def create_text_chunk(self, text):
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        return chunks


    def create_vectorstore(self, text_chunks):
        '''
        Create a vectorstore from the embeddings
        '''
        embeddings = HuggingFaceEmbeddings()
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

        return vectorstore


    def get_reponse(self, user_input, chat_history):
        context = self.retriever.get_relevant_documents(query=user_input)
        # Join all messages to a string
        role_map = { "user": "Usuário", "assistant": "Sistema"}
        chat_history_formatted = [ f"{role_map[message['role']]}: {message['content']}" for message in chat_history ]
        chat_history_str = '\n'.join(chat_history_formatted)
        
        # Create prompt template with input and output languages as Portuguese
        prompt = self.prompt_template.format_messages(
            input_language="Portuguese", 
            output_language="Portuguese", 
            question=user_input,
            context=context,
            chat_history=chat_history_str
        )

        answer = self.llm_model(prompt)
        return answer.content

