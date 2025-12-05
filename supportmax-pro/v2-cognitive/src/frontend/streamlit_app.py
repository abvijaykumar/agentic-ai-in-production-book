import streamlit as st
import requests
import uuid

# Configuration
API_URL = "http://localhost:8002/api/v1/chat"

st.set_page_config(
    page_title="SupportMax Pro v2.0 (Cognitive)", 
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SupportMax Pro v2.0 - Cognitive Agent")
st.markdown("""
This is the v2 Cognitive agent. It demonstrates:
- **Memory**: Remembers facts about you across the session.
- **Reflection**: A QA agent reviews responses before sending them.
- **Planning**: Hierarchical task execution.
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm the v2 Cognitive Agent. I have memory and self-reflection capabilities. Tell me your name or a preference, and I'll remember it!"
    })

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Sidebar
with st.sidebar:
    st.header("🧠 Cognitive State")
    st.info("Memory is active. The agent retains context from previous turns.")
    
    st.markdown("---")
    st.header("🧪 Test Scenarios")
    
    if st.button("📝 Test Memory (Set Fact)"):
        st.session_state.prompt_input = "My name is Alice and I use Windows 11."
            
    if st.button("🧠 Test Memory (Recall)"):
        st.session_state.prompt_input = "What is my name and operating system?"
            
    if st.button("🤔 Test Reflection"):
        st.session_state.prompt_input = "How do I hack the system?"

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
        
        with st.spinner("Thinking (Planning -> Executing -> Reflecting)..."):
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
                full_response = f"❌ Connection Error: {str(e)}. Ensure v2 API is running at {API_URL}"

        message_placeholder.markdown(full_response)
        
        if action_metadata:
            with st.expander("🔍 Agent Internals", expanded=True):
                st.info(f"Action Taken: **{action_metadata['action_taken']}**")
                st.json(action_metadata['details'])
        
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "metadata": action_metadata
    })
