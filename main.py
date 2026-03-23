import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# 1. Page Config & UI Styling
st.set_page_config(page_title="AI PDF Tutor", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FC; }
    .main .block-container { padding: 2rem; max-width: 900px; }
    .stButton>button { background-color: #6366F1; color: white; border-radius: 12px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 2. API Setup
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Sidebar - PDF Upload
with st.sidebar:
    st.title("🎓 Study Material")
    uploaded_pdf = st.file_uploader("ඔබේ PDF ගොනුව මෙතනට දමන්න", type=['pdf'])
    st.info("PDF එක අප්ලෝඩ් කර ප්‍රශ්න අසන්න හෝ කෙටි සටහන් ඉල්ලන්න.")

# 4. PDF එකේ අකුරු කියවීමේ Function එක
def get_pdf_text(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 5. Main Content
st.title("📚 AI PDF Assistant")

if uploaded_pdf:
    # PDF එකෙන් Text ලබා ගැනීම
    with st.spinner("PDF එක කියවමින් පවතී..."):
        context_text = get_pdf_text(uploaded_pdf)
    
    st.success("PDF එක සාර්ථකව කියවන ලදී!")
    
    # කෙටි සටහන් සෑදීමේ Button එක
    if st.button("📝 මෙම පාඩමේ කෙටි සටහනක් (Summary) සාදන්න"):
        prompt = f"Please provide a detailed summary of this text in Sinhala and English: {context_text[:10000]}"
        response = model.generate_content(prompt)
        st.subheader("කෙටි සටහන:")
        st.write(response.text)

    st.markdown("---")
    
    # ප්‍රශ්න ඇසීමේ කොටස
    user_question = st.text_input("මෙම PDF එක ගැන ඕනෑම ප්‍රශ්නයක් අහන්න:")
    if user_question:
        full_prompt = f"Based on this content: {context_text[:10000]}\n\nAnswer the question: {user_question}"
        with st.chat_message("assistant"):
            response = model.generate_content(full_prompt)
            st.write(response.text)
else:
    st.warning("කරුණාකර ආරම්භ කිරීමට PDF ගොනුවක් අප්ලෝඩ් කරන්න.")
