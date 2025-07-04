import streamlit as st
import pandas as pd
import google.generativeai as genai

# --- CONFIGURE GOOGLE GEMINI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

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
    # Use a native Streamlit image component for the logo
    st.image("kepler-logo.png", width=120)
    st.header("Navigation") #sidebar header 

    # Only "Chatbot" and "About Me" buttons remain
    if st.button("💬 Chatbot", use_container_width=True, key="chat_btn"):
        st.query_params['page'] = 'chat'
        st.rerun()
    if st.button("ℹ️ About Me", use_container_width=True, key="about_btn"):
        st.query_params['page'] = 'about'
        st.rerun()

# --- MAIN CONTENT AREA: DISPLAY PAGE BASED ON URL PARAMETER ---
# Default page is now 'chat' since 'home' is removed
current_page = st.query_params.get('page', 'chat')

if current_page == "chat":
    # --- Chatbot Page Content ---
    st.image("kepler-logo.png", width=120)
    st.markdown("<h2 style='color:#2A527A; text-align:center;'>Welcome to Kepler CampusBot 🎓</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Ask about Kepler College rules, policies, or services.</p>", unsafe_allow_html=True)

    # --- CHAT DISPLAY ---
    if "history" not in st.session_state:
        st.session_state.history = []

    for msg in st.session_state.history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- CHAT INPUT AREA (Simplified) ---
    # Use st.chat_input for a clean chat interface
    user_input = st.chat_input("Type your question...", key="chat_input")

    # --- PROCESS USER QUESTION ---
    if user_input:
        # Add user message to chat history
        st.session_state.history.append({"role": "user", "content": user_input})
        with st.chat_message("user"): st.markdown(user_input)
        
        # Generate response from Gemini based on context
        prompt = f"""You are Kepler CampusBot. Use this Q&A to help answer:\n{context}\n\nUser: {user_input}"""
        response = model.generate_content(prompt)
        answer = response.text.strip()

        # Display and save assistant's response
        st.session_state.history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"): st.markdown(answer)
        
        # Rerun to clear the input box and update chat history
        st.rerun() 

elif current_page == "about":
    # --- About Me Page Content ---
    st.title("About Kepler College Chatbot")
    st.markdown(
        """
        I am CampusBot, an AI assistant designed to help you with a wide range of tasks and questions about Kepler College. 
        My knowledge is based on official college resources, and my goal is to provide you with instant, accurate information.
        """
    )
    
    st.markdown("---") # Add a horizontal rule for separation

    st.markdown(
        """
        ### Contact Us
        For more detailed information, personalized assistance, or questions beyond my knowledge base, you can contact the Kepler College team:
        
        - **Phone:** `+250789773042`
        - **Website:** Visit the official Kepler website at [**keplercollege.ac.rw**](https://keplercollege.ac.rw)
        - **Admissions:** For admissions-related questions, contact the Admissions team at [**admissions@keplercollege.ac.rw**](mailto:admissions@keplercollege.ac.rw)
        """
    )
    
    st.markdown("---")