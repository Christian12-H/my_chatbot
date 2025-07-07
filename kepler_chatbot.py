import streamlit as st
import pandas as pd
import openai

# --- CONFIGURE OPENAI ---
openai.api_key = st.secrets["openai"]["api_key"]
model_id = "gpt-3.5-turbo"  # or use "gpt-4" if your key has access

# --- LOAD DATA FROM XLSX ---
try:
    df = pd.read_excel('Chatbot Questions & Answers.xlsx')
    qa_pairs = [f"Q: {q}\nA: {a}" for q, a in zip(df['Question'], df['Answer'])]
    context = "\n".join(qa_pairs)
except FileNotFoundError:
    st.error("Data file 'Chatbot Questions & Answers.xlsx' not found. Please make sure it's in the same directory.")
    st.stop()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kepler CampusBot", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.image("kepler-logo.png", width=120)
    st.header("Navigation")

    if st.button("💬 Chatbot", use_container_width=True, key="chat_btn"):
        st.query_params['page'] = 'chat'
        st.rerun()
    if st.button("ℹ️ About Me", use_container_width=True, key="about_btn"):
        st.query_params['page'] = 'about'
        st.rerun()

# --- MAIN CONTENT AREA ---
current_page = st.query_params.get('page', 'chat')

if current_page == "chat":
    st.image("kepler-logo.png", width=120)
    st.markdown("<h2 style='color:#2A527A; text-align:center;'>Welcome to Kepler CampusBot 🎓</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Ask about Kepler College rules, policies, or services.</p>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your question...", key="chat_input")

    if user_input:
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # OpenAI prompt with Q&A context
        prompt = f"""You are Kepler CampusBot. Use this Q&A to help answer:\n{context}\n\nUser: {user_input}\nAnswer:"""

        try:
            response = openai.ChatCompletion.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Kepler College."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"Error from OpenAI: {e}"

        st.session_state.history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

        st.rerun()

elif current_page == "about":
    st.title("About Kepler College Chatbot")
    st.markdown(
        """
        I am CampusBot, an AI assistant designed to help you with a wide range of tasks and questions about Kepler College. 
        My knowledge is based on official college resources, and my goal is to provide you with instant, accurate information.
        """
    )
    st.markdown("---")
    st.markdown(
        """
        ### Contact Us
        - **Phone:** +250789773042  
        - **Website:** [keplercollege.ac.rw](https://keplercollege.ac.rw)  
        - **Admissions:** [admissions@keplercollege.ac.rw](mailto:admissions@keplercollege.ac.rw)
        """
    )
    st.markdown("---")
