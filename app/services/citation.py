from typing import List, Dict

def format_citations(docs: List[Dict]) -> List[str]:
    """Format document citations"""
    citations = []
    for i, doc in enumerate(docs, 1):
        citation = f"[{i}] {doc['title']} - {doc['url']}"
        citations.append(citation)
    return citations
