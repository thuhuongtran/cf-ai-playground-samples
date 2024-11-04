import streamlit as st
import requests

"# Text Generation"

models = [
    "@hf/thebloke/zephyr-7b-beta-awq",
    "@hf/thebloke/mistral-7b-instruct-v0.1-awq",
    "@hf/thebloke/openhermes-2.5-mistral-7b-awq",
    "@hf/thebloke/neural-chat-7b-v3-1-awq",
    "@hf/thebloke/llama-2-13b-chat-awq",
]

with st.form("text_generation"):
    model = st.selectbox("Choose your Text Generation model", options=models)
    prompt = st.text_area("Enter your prompt")
    submitted = st.form_submit_button("Generate")

if submitted:
    account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
    headers = {"Authorization": f"Bearer {api_token}"}
    
    with st.spinner("Generating..."):
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        response = requests.post(url, headers=headers, json={"prompt": prompt})
        result = response.json().get("result", {}).get("response", "No response received")
        st.text_area("Generated Text", value=result, height=200)

    st.button("Copy to Clipboard", on_click=lambda: st.query_params(text=result))