import os

import time

from tqdm import tqdm

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from llm_stack import embedding_model
from db_ops import insert_document

def document_to_text(file_path: str) -> list[str]:
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    separators=["\n \n", "\n", "\n\n"]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=separators
    )
    
    splitted_texts = text_splitter.split_documents(documents)
    splitted_texts = [text.page_content for text in splitted_texts]
    
    return splitted_texts

def add_doc_to_db(file_path: str, source: str):
    """
    Create embedding of chunks and add the chunks of the document to VectorDB
    """
    text_list = document_to_text(file_path)
    
    for text in text_list:
        doc_obj = {
            "text": text,
            "source": source,
            "embedding": embedding_model.embed_query(text)
        }
        response = insert_document(doc_obj)
        
        # adding delay to avoid google free tier rate limit
        time.sleep(5)
    
    return

def upload_files(directory_path):
    file_names = os.listdir(directory_path)
    
    for file_name in tqdm(file_names, total=len(file_names)):
        file_path = os.path.join(directory_path, file_name)
        
        add_doc_to_db(file_path, source=file_name)
        
    return

if __name__ == "__main__":
    directory = "../documents"
    upload_files(directory)