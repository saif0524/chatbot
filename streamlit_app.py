import streamlit as st
import requests

# Hugging Face API setup
HF_API_KEY = st.secrets.get("HF_API_KEY") or st.text_input("Hugging Face API Key", type="password")

st.title("🍽️ Mood-to-Food Chatbot")

if not HF_API_KEY:
    st.info("Please enter your Hugging Face API key to continue.")
    st.stop()

# Setup session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("How are you feeling?"):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Hugging Face sentiment model
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_input}
    response = requests.post(
        "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
        headers=headers, json=payload
    )
    if response.status_code != 200:
        bot_reply = "😞 Sorry, I'm having trouble analyzing your mood."
    else:
        sentiment = response.json()[0][0]["label"]
        if sentiment == "POSITIVE":
            bot_reply = "You seem happy! How about celebrating with 🍰 cake?"
        elif sentiment == "NEGATIVE":
            bot_reply = "Sounds like you need some comfort food. Try 🍜 ramen or 🍫 chocolate!"
        else:
            bot_reply = "Pizza 🍕 is always a good choice!"

    # Display and store bot message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
