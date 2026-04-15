#!/usr/bin/env python3
"""
Search for similar content in ChromaDB vector database.
Usage: python3 search.py --query "your search query" --limit 5
"""

import json
import argparse
import chromadb
from chromadb.config import Settings
from pathlib import Path

VECTOR_DB_PATH = Path.home() / ".hermes" / "vector_db"

def main():
    parser = argparse.ArgumentParser(description='Search vector DB')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--limit', '-l', type=int, default=5, help='Max results')
    parser.add_argument('--collection', '-c', default='research', help='Collection name')
    args = parser.parse_args()
    
    # Initialize ChromaDB
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=str(VECTOR_DB_PATH),
        anonymized_telemetry=False
    ))
    
    # Get collection
    try:
        collection = client.get_collection(name=args.collection)
    except Exception as e:
        print(f"Collection '{args.collection}' not found. Error: {e}")
        return
    
    # Get embedding for query
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([args.query]).tolist()
    
    # Search
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=args.limit
    )
    
    # Print results
    if not results['documents'] or not results['documents'][0]:
        print(f"No results found for '{args.query}'")
        return
    
    print(f"Found {len(results['documents'][0])} results:\n")
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        print(f"{i}. {doc[:200]}...")
        print(f"   Metadata: {json.dumps(meta)}")
        print()

if __name__ == '__main__':
    main()
