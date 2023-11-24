import json
import streamlit as st
from PIL import Image

def render():
    with st.sidebar:
        # load endpoints from enpoints.json and model settings
        endpoints = []
        with open("src/endpoints.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            endpoints = list(data.keys())
        st.title("Settings")
        st.markdown("Warning! Changing these settings can make the app unable to connect to server.", unsafe_allow_html=True)
        endpoint = st.selectbox("endpoint", endpoints)
        user_content = ""
        stream = False
        max_tokens = st.number_input("max_tokens", value=8192, min_value=16, max_value=8192, step=1)
        temperature = st.number_input("temperature", value=0.05, min_value=0.05, max_value=2.00, step=0.05)
        top_p = st.number_input("top_p", value=0.95, min_value=0.0, max_value=1.0, step=0.05)
        top_k = st.number_input("top_k", value=40, min_value=1, max_value=200, step=1)
        repeat_penalty = st.number_input("repeat_penalty", value=1.1, min_value=1.0, max_value=1.5, step=0.05)
        stop =  st.text_input("stop", value=r'\n, ###')
        stop = stop.encode().decode('unicode_escape')
        stop = stop.replace(" ", "").split(",")
        if endpoint == "/v1/chat/completions":
            system_content = st.text_area("system_content", value="This is a conversation between a human and MAPES, a friendly Generative Artifical Intelegeence. MAPES is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision, based on the following context: ", height=200)
        else:
            system_content = st.text_area("system_content", value=r"\n\n### This is a conversation between a human and MAPES, a friendly Generative Artifical Intelegeence. MAPES is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision:\n{prompt}\n\n### Response:\n", height=200)
            system_content = system_content.encode().decode('unicode_escape')
            st.markdown("hint: the expression `{prompt}` must exist!", unsafe_allow_html=True)
        return endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content 
