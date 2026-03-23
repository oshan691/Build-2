import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Tutor", page_icon="🎓")

# API Key Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# AI එකට දෙන විශේෂ උපදෙස් (System Instruction)
# මෙතැනදී අපි AI එකට කියනවා ඔහු දක්ෂ ගුරුවරයෙක් වගේ කරුණු සරලව කියල දෙන්න කියලා.
instruction = "You are a helpful and patient educational tutor. Explain concepts simply in Sinhala and English. Use examples."
model = # වැඩ කරන Model එක ස්වයංක්‍රීයව හඳුනා ගැනීමට
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
# සාමාන්‍යයෙන් පළමු model එක තෝරා ගනී
model_name = available_models[0] if available_models else 'gemini-1.5-flash'
model = genai.GenerativeModel(model_name)

st.title("🎓 AI අධ්‍යාපනික සහායක")
st.write("ඕනෑම විෂයක ගැටලුවක් මෙතනින් අහන්න.")

# Chat History එක තබා ගැනීමට
if "messages" not in st.session_state:
    st.session_state.messages = []

# පරණ මැසේජ් පෙන්වීම
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User ගෙන් ප්‍රශ්නය ලබා ගැනීම
if prompt := st.chat_input("ඔබට ඉගෙන ගැනීමට අවශ්‍ය මොනවාද?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI එකෙන් පිළිතුර ලබා ගැනීම
    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
