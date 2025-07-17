import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Fetch the key
api_key = os.getenv("OPENROUTER_API_KEY")

import requests

def query_llama(prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "google/gemma-3n-e2b-it:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()

    # Debug print
    print("🔍 Full API response:", result)

    try:
        return result['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        return f"⚠️ API Error: {result.get('error', str(e))}"


import streamlit as st

st.set_page_config(page_title="EcoBot Chat")
st.title("♻️ Eco-Friendly Product Recommender")

user_input = st.text_input("Enter a product (e.g., shampoo, bottle, detergent):")

if st.button("Get Eco-Friendly Alternatives"):
    if user_input:
        prompt = f"""Suggest 3 eco-friendly alternative products for {user_input}. 
        Each product should include:
        - Name
        - Description (1-2 lines)
        - A real or placeholder URL link
        - Environmental Score from 1 to 10

        Format the reply clearly with bullets or numbered list."""

        with st.spinner("Thinking..."):
            output = query_llama(prompt)
            st.markdown(output)
