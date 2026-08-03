"""
Streamlit chat interface for Lucid.
Run with: streamlit run lucid_chat_ui.py

Supports arriving from an email chat link with a specific paper pre-anchored,
via a URL query param: ?paper_id=2607.29626v1&title=AgentHPOBench
"""

import streamlit as st
import requests

# Point this at your deployed FastAPI server once it's hosted on Azure
API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(page_title="Lucid Chat", page_icon="🔬", layout="centered")

# --- Read anchor paper from URL, if the user arrived via an email chat link ---
query_params = st.query_params
anchor_paper_id = query_params.get("paper_id", None)
anchor_paper_title = query_params.get("title", None)

st.title("🔬 Lucid Chat")

if anchor_paper_title:
    st.info(f"Chatting about: **{anchor_paper_title}**  \nAsk anything else too — I can look beyond this paper if needed.")
else:
    st.info("Ask me anything about the papers in your Lucid digest.")

# --- Session-local chat history, just for displaying the conversation in the UI ---
# (Actual memory lives server-side in ChatService — this is purely visual)
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat input ---
user_message = st.chat_input("Ask a question about your papers...")

if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.write(user_message)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"user_message": user_message, "anchor_paper_id": anchor_paper_id},
                    timeout=30
                )
                response.raise_for_status()
                reply = response.json()["reply"]
            except requests.exceptions.RequestException as e:
                reply = f"Sorry, something went wrong reaching the chat server: {e}"

            st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})