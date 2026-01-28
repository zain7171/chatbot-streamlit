# Groq Chatbot with Memory

An **interactive AI chatbot** built with **Streamlit**, **LangChain**, and **Groq**, featuring **persistent chat memory**, **configurable models**, and **JSON export**.  

This project demonstrates how to build a memory-aware AI assistant using modern LLMs.


## Features

- Select from multiple LLMs (GPT-OSS, LLaMA, Qwen, etc.)  
- Persistent chat memory during sessions  
- Customizable system prompts  
- Download chat history as JSON  
- Clean, responsive Streamlit interface  


## Full Installation & Setup

Copy and run the entire block below from top to bottom:

```bash
# Clone the repository
git clone https://github.com/<your-username>/groq-chatbot.git
cd groq-chatbot

# Create and activate a virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt

# Create a .env file and add your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run the Streamlit app
streamlit run chatbot.py
