

import streamlit as st
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
# Load AI model from Ollama
llm = OllamaLLM(model="mistral")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()
    
# Define a prompt template
prompt = PromptTemplate(
    input_variables=["question", "chat_history"],
    template="previous conversation: {chat_history}\n\nUser: {question}\nAI:"
)
# function to run ai and chat history
def run_chain(question):
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    
    # run the ai response
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    return response
# Streamlit app for AI chat with history
st.title("🤖AI ChatBOT with Memory")
st.write("Ask me anything!")
user = st.text_input("💬Your question:")
if user:
    response = run_chain(user)
    st.write(f"User: {user}")
    st.write(f"AI Response: {response}")
# Show full history
st.subheader("Chat History")
for msg in st.session_state.chat_history.messages:
    st.write(f"{msg.type.capitalize()}: {msg.content}")
    
    






 