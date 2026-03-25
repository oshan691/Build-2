import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# 2. API Key Setup
if "GEMINI_API_KEY" not in st.secrets:
    st.error("කරුණාකර Streamlit Secrets වල 'GEMINI_API_KEY' ඇතුළත් කරන්න.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. වැඩ කරන Model එක හොයා ගැනීම (NotFound Error එක මගහැරීමට)
@st.cache_resource
def load_model():
    try:
        # මුලින්ම gemini-1.5-flash බලනවා, ඒක නැත්නම් gemini-pro බලනවා
        model = genai.GenerativeModel('gemini-1.5-flash')
        

model = load_model('gemini-1.5-flash')

# 4. UI එක
st.title("🎓 AI අධ්‍යාපනික සහායක")
st.write("ඕනෑම විෂයක ගැටලුවක් මෙතනින් අහන්න.")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ පණිවිඩ පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
if prompt := st.chat_input("ඔබට ඉගෙන ගැනීමට අවශ්‍ය මොනවාද?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    try:
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"පොඩි ගැටලුවක් ආවා: {str(e)}")
