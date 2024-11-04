import streamlit as st
import requests

"# Code Generation"

models = [
    "@hf/thebloke/deepseek-coder-6.7b-instruct-awq"
]
system_message = "The user is going to give you code that isn't working. Explain to the user what might be wrong. Or the user would like to have tests written in the Python unittest module"

with st.form("text_generation"):
    model = st.selectbox("Choose your Code Generation model", options=models)
    prompt = st.text_area("Enter your prompt")
    submitted = st.form_submit_button("Generate")

if submitted:
    account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]
    api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
    headers = {"Authorization": f"Bearer {api_token}"}

    with st.spinner("Generating..."):
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
            headers={"Authorization": f"Bearer {api_token}"},
            json={"messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ]}
        )
        result = response.json().get("result", {}).get("response", "No response received")
        st.text_area("Generated Code", value=result, height=200)

    st.button("Copy to Clipboard", on_click=lambda: st.query_params(text=result))