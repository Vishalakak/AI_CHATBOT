import requests
from bs4 import BeautifulSoup
import streamlit as st
from langchain_ollama import OllamaLLM
# Load AI model from Ollama
llm = OllamaLLM(model="mistral")
# Function to scrape web content
def scrape_website(url):
    try:
        st.write(f"Scraping {url}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return f"failed to retrieve content from {url}"
        # extract text content from HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = "\n".join([para.get_text() for para in paragraphs])
        return text[:2000]
    except Exception as e:
        return f"An error occurred: {str(e)}"
# function to summarize content using ai
def summarize_content(content):
    st.write("Summarizing content...")
    return llm.invoke(f"Summarize the following content:\n\n{content[:2000]}")
# Streamlit app for web scraping and summarization
st.title("🌐 AI Web Scraper and Summarizer")
st.write("Enter a URL to scrape and summarize its content.")
# URL input
url = st.text_input("Enter URL:")
if url:
    content = scrape_website(url)
    if "failed" in content or "An error occurred" in content:
        st.write(content)
    else:
        st.write("Content scraped successfully!")
        st.write(content)
        # Summarize content
        summary = summarize_content(content)
        st.subheader("Summary")
        st.write(summary)
        
