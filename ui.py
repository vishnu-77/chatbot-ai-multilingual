import streamlit as st
from backend import MultilingualChatbot
import json
from datetime import datetime

st.title("Vishnu's Multi Lingual chatbot")

# Initialize sessions
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.all_chats[st.session_state.current_chat_id] = []

# Sidebar
with st.sidebar:
    language = st.selectbox("Language", [
        "Auto-detect", "English", "Spanish", "French", "German",
        "Hindi", "Japanese", "Chinese", "Arabic"
    ])
    
    # New chat button
    if st.button("➕ New Chat"):
        st.session_state.current_chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.all_chats[st.session_state.current_chat_id] = []
        st.rerun()
    
    st.markdown("---")
    
    # Show all previous chats
    st.markdown("### 💬 Chat History")
    for chat_id in reversed(list(st.session_state.all_chats.keys())):
        chat_messages = st.session_state.all_chats[chat_id]
        if chat_messages:
            # Get first message preview
            first_msg = chat_messages[0]["content"][:30]
            is_current = chat_id == st.session_state.current_chat_id
            
            # Show chat button
            if st.button(
                f"{'🟢' if is_current else '💬'} {first_msg}...",
                key=chat_id,
                use_container_width=True
            ):
                st.session_state.current_chat_id = chat_id
                st.rerun()

# Get current chat messages
current_messages = st.session_state.all_chats[st.session_state.current_chat_id]

# Display current chat
for msg in current_messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    
    # Show user message
    current_messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Decide language first (detection is local and does not require API key)
    if language == "Auto-detect":
        try:
            detected = MultilingualChatbot.detect_language(prompt)
            language_to_use = detected
        except Exception as e:
            # If detection fails, fallback to English and show a notice
            st.warning(f"Language detection failed, defaulting to English: {e}")
            language_to_use = "English"
    else:
        language_to_use = language

    # Now create the chatbot client (this requires GROQ_API_KEY). If the key
    # is not set, show a friendly error instead of crashing.
    try:
        chatbot = MultilingualChatbot()
    except RuntimeError as e:
        st.error(
            "GROQ_API_KEY is not set. Set your Groq API key in the app settings or as an environment variable."
        )
        st.info("See README.md for instructions on obtaining a Groq API key.")
        # Stop execution so we don't attempt to call the API without a key.
        st.stop()

    response = chatbot.chat(prompt, language_to_use, current_messages)
    
    # Show bot message
    current_messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
    
    # Update chat in session
    st.session_state.all_chats[st.session_state.current_chat_id] = current_messages
    
    # Refresh
    st.rerun()