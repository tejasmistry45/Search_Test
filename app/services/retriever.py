import asyncio
from typing import List, Dict
from tavily import TavilyClient
import chromadb
from chromadb.config import Settings
from app.config import settings
from app.utils.embeddings import embed_text
import os

# Initialize Tavily client
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)

# Initialize ChromaDB with new PersistentClient API
os.makedirs(settings.CHROMA_DB_PATH, exist_ok=True)
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection("search_results")


async def search_and_retrieve(query: str) -> List[Dict]:
    """Search using Tavily and store/retrieve results"""
    try:
        # Search using Tavily
        search_response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=settings.MAX_SEARCH_RESULTS,
            include_answer=True,
            include_raw_content=True
        )

        documents = []
        for idx, result in enumerate(search_response.get('results', [])):
            content = result.get('content', '')
            if len(content) > settings.MAX_CONTENT_LENGTH:
                content = content[:settings.MAX_CONTENT_LENGTH] + "..."

            doc = {
                'content': content,
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'score': result.get('score', 0.0)
            }
            documents.append(doc)

            # Store in ChromaDB for future retrieval
            try:
                embedding = embed_text(content)
                collection.add(
                    documents=[content],
                    embeddings=[embedding.tolist()],
                    metadatas=[{
                        'title': doc['title'],
                        'url': doc['url'],
                        'score': doc['score']
                    }],
                    ids=[f"doc_{idx}_{hash(doc['url']) % 1000000}"]
                )
            except Exception as e:
                print(f"Error storing document: {e}")
                continue

        return documents

    except Exception as e:
        print(f"Error in search_and_retrieve: {e}")
        return []


async def hybrid_retrieve(query: str, top_k: int = 5) -> List[Dict]:
    """Combine Tavily search with ChromaDB retrieval"""
    # First get fresh results from Tavily
    fresh_results = await search_and_retrieve(query)

    # Also search existing ChromaDB
    try:
        query_embedding = embed_text(query)
        chroma_results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        stored_docs = []
        if chroma_results['documents']:
            for doc, meta in zip(chroma_results['documents'][0], chroma_results['metadatas'][0]):
                stored_docs.append({
                    'content': doc,
                    'title': meta.get('title', ''),
                    'url': meta.get('url', ''),
                    'score': meta.get('score', 0.0)
                })
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        stored_docs = []

    # Combine and deduplicate
    all_docs = fresh_results + stored_docs
    seen_urls = set()
    unique_docs = []

    for doc in all_docs:
        if doc['url'] not in seen_urls:
            seen_urls.add(doc['url'])
            unique_docs.append(doc)

    # Sort by score and return top results
    unique_docs.sort(key=lambda x: x['score'], reverse=True)
    return unique_docs[:top_k]
