import json
import streamlit as st
from PIL import Image

# call render method to set the Footer on every page
def render(page_footer = None):
    # load page_footer from config
    if page_footer == None:
        if 'page_footer' in config:
            page_footer = config['page_footer']
        else:
            page_footer = "Powered by <a href="">M.A.P.E.S. </a> and <a href="">Nexus Gamez | (TM)</a>."
    st.footer(page_footer)