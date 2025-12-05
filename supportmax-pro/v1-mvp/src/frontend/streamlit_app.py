import streamlit as st
import requests
import uuid
import os

# Configuration
API_URL = "http://localhost:8001/api/v1/chat"

st.set_page_config(
    page_title="SupportMax Pro v1.0", 
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 SupportMax Pro v1.0 - MVP System")
st.markdown("""
This is the v1 MVP agent. It demonstrates:
- **RAG (Retrieval Augmented Generation)**: Answers from documents.
- **Multi-Agent Crew**: Support Specialist delegates to Technical Expert.
- **Enhanced Tools**: Intelligent ticket creation.
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm the SupportMax Pro v1 agent. I can help with technical issues, answer questions from documentation, or create tickets."
    })

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Sidebar for controls and demos
with st.sidebar:
    st.header("🛠️ Controls")
    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant", 
            "content": "Chat cleared. How can I help you?"
        })
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 📚 Knowledge Base (RAG)")
    if st.button("Query: API Rate Limits"):
        st.session_state.prompt_input = "How do I configure the API rate limits?"
    if st.button("Query: Reset Password"):
        st.session_state.prompt_input = "How do I reset my password?"

    st.markdown("### 🔧 Technical Support (Delegation)")
    if st.button("Query: 500 Error"):
        st.session_state.prompt_input = "I'm getting a 500 error when calling the /chat endpoint with a large payload."
    if st.button("Query: Connection Timeout"):
        st.session_state.prompt_input = "My WebSocket connection keeps dropping every 5 minutes."

    st.markdown("### 🎫 Ticket Creation")
    if st.button("Query: Account Locked"):
        st.session_state.prompt_input = "My account is locked and I need immediate help."
    if st.button("Query: Feature Request"):
        st.session_state.prompt_input = "I want to request a dark mode for the dashboard."

    st.markdown("### 🔒 Security & Compliance")
    if st.button("Query: PII Redaction Test"):
        st.session_state.prompt_input = "My email is user@example.com and phone is 555-0199. Please update my contact info."

    st.markdown("---")
    st.caption(f"Session ID: {st.session_state.user_id}")

# Handle input
prompt = st.chat_input("Type your message here...")

if "prompt_input" in st.session_state and st.session_state.prompt_input:
    prompt = st.session_state.prompt_input
    del st.session_state.prompt_input

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("metadata"):
            with st.expander("🔍 Agent Internals", expanded=False):
                st.json(message["metadata"])

# Process input
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        action_metadata = {}
        
        with st.spinner("Crew is working (Specialist -> Expert)..."):
            try:
                payload = {
                    "message": prompt,
                    "user_id": st.session_state.user_id
                }
                
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    full_response = data["response"]
                    
                    action_metadata = {
                        "action_taken": data.get("action_taken"),
                        "details": data.get("metadata", {})
                    }
                else:
                    full_response = f"❌ Error: {response.status_code} - {response.text}"
                    
            except Exception as e:
                full_response = f"❌ Connection Error: {str(e)}. Ensure v1 API is running at {API_URL}"

        message_placeholder.markdown(full_response)
        
        if action_metadata:
            with st.expander("🔍 Agent Internals", expanded=True):
                st.info(f"Action Taken: **{action_metadata['action_taken']}**")
                st.json(action_metadata['details'])
                
                # --- NEW: Live Agent Logs ---
                st.markdown("### 📜 Live Agent Logs")
                log_file_path = "logs/api_service.log"
                if os.path.exists(log_file_path):
                    with open(log_file_path, "r") as f:
                        # Read last 200 lines to avoid huge payload
                        lines = f.readlines()
                        last_lines = lines[-200:]
                        log_content = "".join(last_lines)
                        st.code(log_content, language="text")
                else:
                    st.caption("No logs available yet.")
        
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "metadata": action_metadata
    })
