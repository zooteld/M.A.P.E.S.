import json
import streamlit as st
from PIL import Image

favicon = Image.open('static/favicon.png')

# adds the logo to the sidebar
def logo():
    im = Image.open('static/logo.png')
    im.draft('RGB',(1008,756))
    # render logo
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] {{
                background-image: url(app/static/logo.png);
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: auto 80px;
            }}
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                padding-top: 20px;
            }}
            [data-testid="stForm"] {{
                border: none;
                padding-left: 0px;
            }}
            [data-testid="stMarkdownContainer"] p {{
                font-weight: normal;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# call render method to set the header on every page
def render(page_title = None):
    # load title from config-file
    with open("src/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        # load page_title from config
        if page_title == None:
            if 'page_title' in config:
                page_title = config['page_title']
            else:
                page_title = "M.A.P.E.S."
    # page setup
    st.set_page_config(
        page_icon=favicon,
        page_title=page_title,
        layout='wide',
        initial_sidebar_state='collapsed',
    )
    # logo
    logo()
    st.title(page_title)