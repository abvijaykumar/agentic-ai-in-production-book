import streamlit as st
import requests
import uuid
import json

# Configuration
API_URL = "http://localhost:8000/api/v1/chat"

st.set_page_config(
    page_title="SupportMax Pro v0.5", 
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SupportMax Pro v0.5 - Baseline Agent")
st.markdown("""
This is the baseline agent for Chapter 1. It demonstrates:
- **FAQ Answering**: Matches queries against a knowledge base.
- **Ticket Creation**: Detects intent to create support tickets.
""")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm the SupportMax Pro baseline agent. I can answer FAQs or help you create a ticket."
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
    st.header("🧪 Example Queries")
    
    with st.expander("📚 FAQs", expanded=True):
        if st.button("Password Reset"):
            st.session_state.prompt_input = "How do I reset my password?"
        if st.button("Billing Info"):
            st.session_state.prompt_input = "Where can I find billing information?"
        if st.button("Support Hours"):
            st.session_state.prompt_input = "What are your support hours?"

    with st.expander("🎫 Ticket Management", expanded=True):
        if st.button("Create Ticket (Generic)"):
            st.session_state.prompt_input = "I need to create a support ticket about login issues"
        if st.button("Report Bug"):
            st.session_state.prompt_input = "I found a bug on the dashboard page, it returns 404"
        if st.button("Check Last Ticket (Placeholder)"):
             st.session_state.prompt_input = "What is the status of my ticket?"
        st.caption("To check a specific ticket, create one first and then copy the ID.")

    with st.expander("💬 General", expanded=True):
        if st.button("Greeting"):
            st.session_state.prompt_input = "Hello, who are you?"
        if st.button("Unknown Query"):
            st.session_state.prompt_input = "What is the weather in Tokyo?"

    st.markdown("---")
    st.caption(f"Session ID: {st.session_state.user_id}")

# Handle input from buttons or chat box
prompt = st.chat_input("Type your message here...")

# Check if a button set the input
if "prompt_input" in st.session_state and st.session_state.prompt_input:
    prompt = st.session_state.prompt_input
    del st.session_state.prompt_input

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Show metadata if available (for assistant messages)
        if message.get("metadata"):
            with st.expander("🔍 Agent Internals", expanded=False):
                st.json(message["metadata"])

# Process user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        action_metadata = {}
        
        with st.spinner("Agent is thinking..."):
            try:
                payload = {
                    "message": prompt,
                    "user_id": st.session_state.user_id
                }
                
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    full_response = data["response"]
                    
                    # Prepare metadata for display
                    action_metadata = {
                        "action_taken": data.get("action_taken"),
                        "details": data.get("metadata", {})
                    }
                else:
                    full_response = f"❌ Error: {response.status_code} - {response.text}"
                    
            except Exception as e:
                full_response = f"❌ Connection Error: {str(e)}. Ensure API is running at {API_URL}"

        message_placeholder.markdown(full_response)
        
        if action_metadata:
            with st.expander("🔍 Agent Internals", expanded=True):
                st.info(f"Action Taken: **{action_metadata['action_taken']}**")
                
                start_details = action_metadata.get('details', {})
                if 'steps' in start_details:
                    st.write("### 🧠 Agent Thought Process")
                    steps = start_details['steps']
                    for i, step in enumerate(steps):
                        # Use markdown for text wrapping instead of st.text/code which scrolls
                        with st.container():
                            st.markdown(f"**Step {i+1}**")
                            st.markdown(f"> {step}")
                            st.divider()
                    
                    # Remove steps from details to avoid duplicate display
                    start_details.pop('steps', None)
                
                if start_details:
                    st.json(start_details)
        
    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": full_response,
        "metadata": action_metadata
    })
