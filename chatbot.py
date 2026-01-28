import os
import json
from dotenv import load_dotenv
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
st.set_page_config(page_title="Chatbot with Memory",page_icon="💬")
st.title("💬 Groq Chatbot With Memory")
with st.sidebar:
    st.subheader("Chatbot Controls")
    model_name = st.selectbox(
        "Groq Models",
        ["openai/gpt-oss-120b","meta-llama/llama-guard-4-12b","llama-3.3-70b-versatile","qwen/qwen3-32b"],
        index = 0
    )
    temperature = st.slider("Temperature (Creativity of the model)",0.0,1.0,0.7)
    max_tokens = st.slider("Max Tokens",50,300,150)
    system_prompt = st.text_area(
        "System prompt(rules)",
        value="You are the smartest assistant who always gives concise answers with clear explanations."
    )
    st.caption("Tip: Lower temperature for straight-forward task, increase for brainstorming")
    if st.button("🧹Clear Chat"):
        st.session_state.pop("history",None)
        st.rerun()
if not groq_api_key:
    st.error("Your API key is missing, please add it to the .env file")
    st.stop()
if "history" not in st.session_state:
    st.session_state.history = InMemoryChatMessageHistory()
llm = ChatGroq(
    model = model_name,
    temperature = temperature,
    max_tokens = max_tokens
)
prompt = ChatPromptTemplate.from_messages([
    ("system","{system_prompt}"),
    MessagesPlaceholder(variable_name="history"),
    ("human","{input}")
])
chain = prompt | llm | StrOutputParser()
chat_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: st.session_state.history,
    input_messages_key="input",
    history_messages_key="history"
)
for msg in st.session_state.history.messages:
        role = getattr(msg,"type",None) or getattr(msg,"role","")
        content = msg.content
        if role == "human":
             st.chat_message("user").write(content)
        elif role in ("ai","assistant"):
             st.chat_message("assistant").write(content)
user_input = st.chat_input("Start typing.....")
if user_input:
     st.chat_message("user").write(user_input)
     with st.chat_message("assistant"):
          placeholder = st.empty()
          try:
               response_text = chat_with_history.invoke(
                    {"input":user_input,"system_prompt":system_prompt},
                    config={"configurable":{"session_id":"default"}}
               )
               st.write(response_text)
          except Exception as e:
               st.error(f"Model error: {e}")
               response_text=""
               typed=""
               for ch in response_text:
                    typed = typed + ch
                    placeholder.markdown(typed)
export = []                   
if st.session_state.history.messages:
     for m in st.session_state.history.messages:
          role = getattr(m,"type",None) or getattr(m,"role","")
          if role=="human":
               export.append({"role":"user","text":m.content})
          elif role in ("ai","assistant"):
               export.append({"role":"assistant","text":m.content})
st.download_button(
     "⬇️Download Chat JSON (Chat history)",
     data = json.dumps(export,ensure_ascii=False,indent=2),
     file_name="chat_history.json",
     mime="application/json",
     use_container_width=True
)