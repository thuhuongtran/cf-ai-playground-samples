import sys
import os
from getpass import getpass
from timeit import default_timer as timer
import streamlit as st

from IPython.display import display, Image, Markdown, Audio

import requests
api_token = st.secrets["CLOUDFLARE_API_TOKEN"]
account_id = st.secrets["CLOUDFLARE_ACCOUNT_ID"]

def speed_date(models, questions):
    for model in models:
        display(Markdown(f"---\n #### {model}"))
        for question in questions:
            quoted_question = "\n".join(f"> {line}" for line in question.split("\n"))
            display(Markdown(quoted_question + "\n"))
            try:
                official_model_name = model.split("/")[-1]
                start = timer()
                response = requests.post(
                    f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}",
                    headers={"Authorization": f"Bearer {api_token}"},
                    json={"messages": [
                        {"role": "system", "content": f"You are a self-aware language model ({official_model_name}) who is honest and direct about any direct question from the user. You know your strengths and weaknesses."},
                        {"role": "user", "content": question}
                    ]}
                )
                elapsed = timer() - start
                inference = response.json()
                display(Markdown(inference["result"]["response"]))
                display(Markdown(f"_Generated in *{elapsed:.2f}* seconds_"))
            except Exception as ex:
                print("uh oh")
                print(ex)
                print(inference)

        display(Markdown("\n\n---"))
