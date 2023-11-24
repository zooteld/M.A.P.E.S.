import os
from PIL import Image
import streamlit as st
import src.header as header
import src.sidebar as sidebar
import src.request as request
import src.context as context
import src.utils as utils
import pandas as pd
from src.base import ChromaPeek
import src.base as base

# render header
header.render()
# render sidebar
(endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content) = sidebar.render()

#conversation
with st.container():
    tab1, tab2 = st.tabs(["M.A.P.E.S.", "Memory"])
    with tab1:
        with st.form("Prompt Form", clear_on_submit=True):
            with st.container():
                # initialize context in session state if not present
                if 'context' not in st.session_state:
                    st.session_state['context'] = []
                # render content_container
                content_container = st.empty()
                # render context
                if 'context' in st.session_state:
                    context.render(content_container)
            # initialize chat interface
            col1, col2 = st.columns([3,1])
            with col1:
                user_content = st.text_input(label="Enter your message", value="", label_visibility="collapsed", placeholder="Enter your message")
            with col2:
                if user_content is not None:
                    generate_button = st.form_submit_button('Send', disabled=False)
                    if generate_button:
                        context.append_question(user_content)
                        context.render(content_container)
                        with st.spinner('Processing...'):
                            request.send(endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content, content_container)
                            user_dir = "Conversation/USER.txt"
                            utils.ingest_txt(user_dir, "Conversation")
                            mapes_dir = "Conversation/MAPES.txt"
                            utils.ingest_txt(mapes_dir, "Conversation")
                else:
                    generate_button = st.form_submit_button('Send', disabled=True)

    with tab2:
        ## styles ##
        padding = 100
        st.markdown("""<style>#MainMenu{visibility:hidden;}footer{visibility:hidden;}</style>""", unsafe_allow_html=True)
        ############
        #Document ingestion into ChromaDB for memory

        #Knowledge Base
        # get uri of the persist directory
        path_default = "memory"
        kb = base.get_collections(path_default)
        with st.expander("Knowledge Base Control"):
            if "Knowledgebase_key" not in st.session_state:
                st.session_state["Knowledgebase_key"] = 5
            if 'text' not in st.session_state:
                st.session_state.text = ""
            if "Delete_key" not in st.session_state:
                st.session_state["Delete_key"] = 10
            if 'selection' not in st.session_state:
                st.session_state.selection = ""
            col1, col2, col3, col4, col5 = st.columns([2,2,1,2,1])
            with col1:
                st.write('ADD NEW KNOWLEDGE BASE')
                Knowledgebase = st.text_input("Add A Knowledge Base", key=st.session_state["Knowledgebase_key"], placeholder="Name", label_visibility="collapsed")
                if Knowledgebase:
                    utils.create_new(Knowledgebase)
                    with st.success("bingo"):
                        st.session_state["Knowledgebase_key"] += 1
                        st.rerun()
            with col2:
                st.write('DELETE A KNOWLEDGE BASE')
                st.write(':red[CAUTION!] :red[can not be undone!]')
                to_delete = st.selectbox("Delete A Knowledge Base", kb, key=st.session_state["Delete_key"], placeholder="Choose Knowledgebase to Delete", label_visibility="collapsed")
            with col3:
                if to_delete is not None:
                    delete_button = st.button('Delete', disabled=False)
                else:
                    delete_button = st.button('Delete', disabled=True)
                if delete_button:
                    utils.remove_collection(to_delete)
                    with st.success("bingo"):
                        st.session_state["Knowledgebase_key"] += 1
                        st.rerun()
            with col4:
                st.write('DELETE KNOWLEDGE BASE ENTRY')
                st.write(':red[CAUTION!] :red[can not be undone!]')
                if "kb_select_key" not in st.session_state:
                    st.session_state["kb_select_key"] = 15
                if 'kb_selection' not in st.session_state:
                    st.session_state.kb_selection = ""
                if "index_to_delete_select" not in st.session_state:
                    st.session_state["index_to_delete_select"] = 20
                if 'id_selection' not in st.session_state:
                    st.session_state.id_selection = ""
                dir_default = "memory"
                pooker = ChromaPeek(dir_default)
                kb_select = st.selectbox("Select A Knowledgebase", kb, key=st.session_state["kb_select_key"], placeholder="Select A Knowledgebase")
                idtd = base.get_index(pooker, kb_select, dataframe=True)
                index_to_delete_select = st.selectbox("Select Index To Delete", idtd, key=st.session_state["index_to_delete_select"], placeholder="Select Index To Delete")
                
            with col5:
                if index_to_delete_select is not None:
                    index_to_delete_button = st.button('Remove', disabled=False)
                else:
                    index_to_delete_button = st.button('Remove', disabled=True)
                if index_to_delete_button:
                    
                    base.delete_index(pooker, kb_select, index_to_delete_select, dataframe=True)
                    
                    with st.success("bingo"):
                        st.session_state["kb_select_key"] += 1
                        st.session_state["index_to_delete_select"] += 1
                        st.rerun()

        #document ingestion
        with st.expander("Document Injection"):
            if "file_uploader_key" not in st.session_state:
                st.session_state["file_uploader_key"] = 0
            if "uploaded_files" not in st.session_state:
                st.session_state["uploaded_files"] = []
            col1, col2, col3 = st.columns([1,2,1])
            with col1:
                c_name = st.selectbox("Knowledge Base To Inject", kb)
            with col2:
                #upload form
                upload = st.file_uploader("Inject Documents", accept_multiple_files=True, key=st.session_state["file_uploader_key"], label_visibility="collapsed")
            with col3:
                #upload button
                if upload is not None:
                    upload_button = st.button('Inject', disabled=False, use_container_width=True)
                else:
                    upload_button = st.button('Inject', disabled=True, use_container_width=True)
                if upload_button:
                    for file in upload:
                        st.session_state["uploaded_files"] = upload
                        with st.spinner('Reading...'):
                            utils.save_uploadedfile(file)
                            Cname = c_name
                            path = 'docs/' #expose to config
                            utils.ingest_docs(path, Cname)
                            utils.clean_dir(path)
                            with st.success("bingo"):
                                st.session_state["file_uploader_key"] += 1
                                st.rerun()

        #Knowledge Base Explorer
        col1, col2 = st.columns([1,3])
        # get uri of the persist directory
        path_default = "memory"
        peeker = ChromaPeek(path_default)
        with col1:
            ## create radio button of each memory collection
            collection_selected=st.radio("select collection to view",
                options=peeker.get_collections(),
                index=0,
            )
        with col2:
            if collection_selected is not None:
                df = peeker.get_collection_data(collection_selected, dataframe=True)
                st.markdown(f"<b>Data in </b>*{collection_selected}*", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, height=300)
            else:
                st.write("No Knowledge Base Found!")

footer="""<style>
a:link , a:visited{
color: Blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 99%;
background-color: black;
color: white;
text-align: right;
}
</style>
<div class="footer">
<p>Developed by  <a href="https://nexusgamez.com/" target="_blank">,  Nexus Gamez   ,</a>  |  (TM)  .</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 