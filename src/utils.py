import os
import json
import subprocess
import streamlit as st
from dotenv import load_dotenv
#from langchain.embeddings import LocalAIEmbeddings
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import Chroma
from IPython.display import Markdown, display
from langchain.document_loaders import TextLoader
import chromadb

def create_new(NEW_NAME):
    chroma_client = chromadb.PersistentClient("memory")
    collection = chroma_client.create_collection(name=NEW_NAME)
    return st.success("New")

def ingest_docs(folder, Cname):
    load_dotenv()
    #Embed model from HF ~To Do: build in a local embedding server~
    embed = HuggingFaceInstructEmbeddings(model_name="vectoriseai/instructor-large")
    # Load Document/s
    loader = DirectoryLoader(path=folder, glob="**/*.*", show_progress=True)
    text = loader.load()
    #client = LocalAIEmbeddings(openai_api_base="http://192.168.1.117:8089/get_all_embedding_vectors_for_document")
    #embed = client.embed_documents(docs)
    # set up ChromaVectorStore and load in data
    storage_context = Chroma.from_documents(text, embedding=embed, collection_name=Cname, persist_directory="./memory")
    return st.success("Upload Embedded")

def ingest_txt(folder, Cname):
    load_dotenv()
    #Embed model from HF ~To Do: build in a local embedding server~
    embed = HuggingFaceInstructEmbeddings(model_name="vectoriseai/instructor-large")
    # Load Document/s
    loader = TextLoader(folder)
    text = loader.load()
    #docs = "{text}, json_format='values', send_back_json_or_zip_file='JSON'"  
    #client = LocalAIEmbeddings(openai_api_base="http://192.168.1.117:8089/get_all_embedding_vectors_for_document")
    #embed = client.embed_documents(text)
    # set up ChromaVectorStore and load in data
    storage_context = Chroma.from_documents(text, embedding=embed, collection_name=Cname, persist_directory="memory")
    return st.success("Upload Embedded")


def save_uploadedfile(uploadedfile):
    with open(os.path.join("docs", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())

def clean_dir(dir):
    command = (f'rm -r {dir}*')  #"rm -r docs/*"
    subprocess.Popen(command, shell=True)
    return st.success("Digested")

def remove_collection(collection_to_delete):
    chroma_client = chromadb.PersistentClient("memory")
    deletion = chroma_client.delete_collection(collection_to_delete)
    return st.success("Deleted")

#def ingest_context():
    #todo add context to ChromaDB
