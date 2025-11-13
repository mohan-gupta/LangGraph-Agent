from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

from langchain_qdrant import QdrantVectorStore

from src.cfg import qdrant_api_key, qdrant_cluster_url
from src.llm_stack import embedding_model

qdrant_client = QdrantClient(
    url=qdrant_cluster_url, 
    api_key=qdrant_api_key,
)

collection_name = "nlp_vectorstore"

def setup_vectordb():
    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
    )
    
def insert_document(doc):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=doc["embedding"],
            payload={"text":doc["text"], "source":doc["source"]}
        )
    ]
    
    response = qdrant_client.upsert(
        collection_name=collection_name,
        points=points
    )
    
    return response
    
def vector_search(query: str, top_k:int = 3):
    query_embedding = embedding_model.embed_query(query)
    
    search_results = qdrant_client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )
    
    context = [item.payload["text"] for item in search_results]
    
    return context

if __name__ == "__main__":
    # set up the vectorDB
    setup_vectordb()
    collections = qdrant_client.get_collections()
    print(collections)