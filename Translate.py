import streamlit as st
import requests

"# Translation"

models = [
    "@hf/thebloke/neural-chat-7b-v3-1-awq",
    "@hf/thebloke/mistral-7b-instruct-v0.1-awq"
]

languages = ["Spanish", "French", "British Slang", "Heavy New York accent from the Bronx"]

with st.form("translation"):
    model = st.selectbox("Choose your Translation model", options=models)
    phrase = st.text_area("Enter the phrase to translate")
    language = st.selectbox("Choose the target language", options=languages)
    submitted = st.form_submit_button("Translate")

if submitted:
    account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
    headers = {"Authorization": f"Bearer {api_token}"}
    
    with st.spinner("Translating..."):
        url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
        question = f'Translate "{phrase}" from "English" to "{language}"'
        response = requests.post(url, headers=headers, json={"prompt": question})
        result = response.json().get("result", {}).get("response", "No response received")
        st.text_area("Translation Result", value=result, height=200)

    st.button("Copy to Clipboard", on_click=lambda: st.query_params(text=result))