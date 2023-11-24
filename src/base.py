import chromadb
from datetime import datetime
import pandas as pd
import src.utils as utils
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceBgeEmbeddings

class ChromaPeek:
    def __init__(self, path):
        self.client = chromadb.PersistentClient(path)
    ## function that returs all collection's name
    def get_collections(self):
        collections = []
        for i in self.client.list_collections():
            collections.append(i.name)
        return collections
    
    ## function to return documents/ data inside the collection
    def get_collection_data(self, collection_name, dataframe=False):
        data = self.client.get_collection(name=collection_name).get()
        if dataframe:
            return pd.DataFrame(data)
        return data

## function that returs all collection's name
def get_collections(path):
    collections = []
    self = chromadb.PersistentClient(path)
    for i in self.list_collections():
        collections.append(i.name)
    return collections

def get_index(self, collection_name, dataframe=False):
    ids = self.client.get_collection(name=collection_name).get()
    if dataframe:
        return pd.DataFrame(ids)
    return ids

def delete_index(self, collection_name, id_td, dataframe=False):
    idk = self.client.get_collection(name=collection_name)
    idd = idk.delete([id_td])
    if dataframe:
        return pd.DataFrame(idd)
    return idd

def ingest_conversation(msg, stick, dataframe=False):
    now = int(datetime.now().timestamp())
    if stick == "MAPES":
        with open('./Conversation/MAPES.txt', 'w') as f:
            lines = f"{now}, {stick}, {msg}"
            f.writelines(lines)
            f.close()
    else:    
        with open('./Conversation/USER.txt', 'w') as f:
            lines = f"{now}, {stick}, {msg}"
            f.writelines(lines)
            f.close()

def get_rag(system_content, user_message):
    dir_default = "memory"
    #sys_dir = "/memory/system"                     <----------uncomment lines #56 thru #79 and delete this message and lines #63, #64?, #72 and #73 for production
    db = chromadb.PersistentClient(dir_default)
    collection_name = "Conversation"
    #collection1 = get_collections(sys_dir)
    #collection = get_collections(dir_default)
    #collection2 = get_collections(dir_default)
    collection = db.get_collection(name=collection_name)
    result2 = collection.get(where_document={"$contains":user_message})
    #result2 = db.collection2.get(where_document={"$contains":user_message})
    #result = f"{system_content}, {result1}, {result2}"
    #if collection1 is not None:
        #if collection2 is not None:
        #    return result
        #else:
        #    resultA = f"{system_content}, {result1}"
    resultA = f"{system_content}, {result2}"
    return resultA
        #    return resultA
    #else:
        #if collection2 is not None:
        #    resultB = f"{system_content}, {result2}"
        #    return 
        #else:
        #    return system_content