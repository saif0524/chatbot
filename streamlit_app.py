import streamlit as st
import requests

HF_API_KEY = st.secrets.get("HF_API_KEY") or st.text_input("Hugging Face API Key", type="password")

st.title("CodeGen Bot with Code Llama")

if not HF_API_KEY:
    st.info("Please enter your Hugging Face API key to continue.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("What code do you need help with?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": f"### Instruction:\n{user_input}\n### Response:\n",
        "parameters": {"max_new_tokens": 256}
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/meta-llama/CodeLlama-7b-hf",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        bot_reply = f"❌ Error: {response.status_code} — {response.text}"
    else:
        output = response.json()
        if isinstance(output, list):
            bot_reply = output[0]["generated_text"].split("### Response:\n")[-1].strip()
        else:
            bot_reply = "🤖 Couldn't parse the model's response."

    with st.chat_message("assistant"):
        st.code(bot_reply, language="python")

    st.session_state.messages.append({"role": "assistant", "content": f"```python\n{bot_reply}\n```"})
