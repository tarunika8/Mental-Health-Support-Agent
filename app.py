import streamlit as st
import ollama
import base64
import time

# ---------- Page config ----------
st.set_page_config(page_title="Mental Health Chatbot")

# ---------- Background ----------
def get_base64(background):
    with open(background, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bin_str = get_base64("background1.jpg")

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{bin_str}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
.center-button {{
    display: flex;
    justify-content: center;
}}
</style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
st.session_state.setdefault("conversation_history", [])
st.session_state.setdefault("show_main_buttons", True)

# ---------- Chatbot response ----------
def generate_response(user_input):
    system_prompt = {
        "role": "system",
        "content": (
            "You are a supportive mental health assistant. "
            "Be empathetic, encouraging, and practical.(1-3 sentences)"
        )
    }

    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input
    })

    messages = [system_prompt] + st.session_state.conversation_history

    response = ollama.chat(
        model="mistral:7b",
        messages=messages
    )

    ai_response = response["message"]["content"]

    st.session_state.conversation_history.append({
        "role": "assistant",
        "content": ai_response
    })

    return ai_response

# ---------- Affirmation ----------
def generate_affirmations_list():
    response = ollama.chat(
        model="mistral:7b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate 5 short positive affirmations starting with 'I am'. "
                    "Keep them informal, friendly, optimistic, and <=10 words. "
                    "Return each affirmation on a new line without numbers."
                )
            },
            {
                "role": "user",
                "content": "Give me 5 positive affirmations."
            }
        ]
    )

    affirmations = response["message"]["content"].split("\n")
    affirmations = [a.strip() for a in affirmations if a.strip()]
    return affirmations[:5]

# ---------- Title ----------
st.title("Mental Health Support Agent")

# ---------- Chat history ----------
for msg in st.session_state.conversation_history:
    role = "You" if msg["role"] == "user" else "AI"
    st.markdown(f"**{role}:** {msg['content']}")

# ---------- User input ----------
if st.session_state.show_main_buttons:
    user_message = st.text_input("How can I help you today?")

    if user_message:
        with st.spinner("Thinking..."):
            ai_response = generate_response(user_message)
            st.markdown(f"**AI:** {ai_response}")

# ---------- Positive Affirmation Button ----------
affirmation_clicked = False

if st.session_state.show_main_buttons:
    col1, col2, col3 = st.columns([9,8,9])
    with col2:
        affirmation_clicked = st.button("Get Positive Affirmations")

# ---------- Affirmation Display ----------
affirm_placeholder = st.empty()

if affirmation_clicked:
    st.session_state.show_main_buttons = False

    affirmations = generate_affirmations_list()

    for a in affirmations:
        affirm_placeholder.markdown(
            f"""
            <h1 style='text-align:center; font-size:40px; font-weight:bold; margin-top:10px;'>
            {a}
            </h1>
            """,
            unsafe_allow_html=True
        )
        time.sleep(5)

    affirm_placeholder.empty()
    st.session_state.show_main_buttons = True 