from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.cfg import gemini_api_key

llm = ChatGoogleGenerativeAI(api_key=gemini_api_key, model="gemini-2.5-flash-lite")

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=gemini_api_key,
    )

# Couldn't use this function, due to rate limit error on bulk generation
def get_embeddings(text: str|list[str])-> list[str] | list[list[str]]:
    """Generates embeddings of size: 3072"""
    if isinstance(text, str):
        embedding = embedding_model.embed_query(text)
    elif isinstance(text, list):
        embedding = embedding_model.embed_documents(text)
    else:
        return -1
    
    return embedding
