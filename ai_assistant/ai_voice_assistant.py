import streamlit as st
import speech_recognition as sr
import pyttsx3
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
# Load AI model from Ollama
llm = OllamaLLM(model="mistral")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()
    
# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)  # Set speech rate
# Initialize speech recognition
recognizer = sr.Recognizer()
# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()
# Function to listen for speech input
def listen():
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        st.write(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        st.write("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        st.write("Could not request results; check your network connection.")
        return None
# Define a prompt template
prompt = PromptTemplate(
    input_variables=["question", "chat_history"],
    template="previous conversation: {chat_history}\n\nUser: {question}\nAI:"
)
# Function to run AI and chat history
def run_chain(question):
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])
    
    # Run the AI response
    response = llm.invoke(prompt.format(chat_history=chat_history_text, question=question))
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)
    return response
# Streamlit app for AI voice assistant
st.title("🤖AI Voice Assistant (Web UI)")
st.write("click the button below to speak to your AI assistant !")
# Button to start listening
if st.button("🎤 Speak to AI"):
    query = listen()
    if query:
        response = run_chain(query)
        speak(response)
        st.write(f"**You**: {query}")
        st.write(f"**AI Response**: {response}")
    # Show full chat history
    st.subheader("Chat History")
    for msg in st.session_state.chat_history.messages:
        st.write(f"{msg.type.capitalize()}: {msg.content}")
        
        