import streamlit as st
import google.generativeai as genai

with open("academic_prompt.txt", "r", encoding="utf-8") as prompt:
    system_prompt = prompt.read()

# -----------------------
# Configure Streamlit app
# -----------------------
st.set_page_config(page_title="Myy Chat App 🤖...app.py", layout="centered")

# Main app UI
st.markdown("<h1 style='text-align:center;'>Foot-y AI 👾 ⚽️</h1>",unsafe_allow_html=True)

st.markdown("<h5 style='text-align:center;'>Your personal AI assistant for football insights and analysis</h5>",unsafe_allow_html=True)

st.markdown("<h5 style='text-align:center;'>Made with Streamlit by Nduoma</h5>",unsafe_allow_html=True)

st.markdown("<h5 style='text-align:center;'>Welcome back, Chief!😉</h5>",unsafe_allow_html=True)

st.markdown(
    '''
    <div style='text-align:center;'>
        <a href="https://github.com/Nduoma132/" target="_blank" style="text-decoration: none; font-weight: bold; text-align: center;">
        🚀 Check out my GitHub projects!
        </a>
    </div>
    ''',
    unsafe_allow_html=True
)


st.divider()

# -----------------------
# Sidebar UI
# -----------------------
with st.sidebar:
    st.title("💬 Footy-AI by Nduoma")
    st.header("Settings ⚙️")
    st.selectbox("Choose preferred model", ["Gemini-1.5-Flash", "Gemini-1.5-Flash-Plus", "Gemini-2.0-Flash", "Gemini-2.5-Flash"], index=0)
    
    if 'GEMINI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        api_key = st.secrets['GEMINI_API_KEY']
    else:
        api_key = st.text_input('Enter Gemini API token:', type='password')
        if not api_key:
            st.warning('Please enter your API key!', icon='⚠️')
        else:
            st.success('API key set. Ready to chat!', icon='👉')

# Exit if no key
if not api_key:
    st.stop()

# -----------------------
# Configure Gemini
# -----------------------
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize chat with system prompt
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(
        history=[
            {"role": "user", "parts": [system_prompt]}
        ])
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["parts"])

# Handle user input
if prompt := st.chat_input("Ask your football related question ⚽..."):

    # Save user message
    user_msg = {"role": "user", "parts": [prompt]}
    st.session_state.messages.append(user_msg)

    # Show user bubble
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get Gemini response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for chunk in st.session_state.chat.send_message(prompt, stream=True):
            full_response += chunk.text
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    assistant_msg = {"role": "model", "parts": [full_response]}
    st.session_state.messages.append(assistant_msg)