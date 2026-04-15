#!/usr/bin/env python3
"""
Store text with metadata in ChromaDB vector database.
Usage: python3 store.py --text "Your text here" --metadata '{"key": "value"}'
"""

import json
import argparse
import chromadb
from chromadb.config import Settings
from pathlib import Path

VECTOR_DB_PATH = Path.home() / ".hermes" / "vector_db"

def get_embedding(text, embedding_model):
    """Get embedding for text using the model."""
    return embedding_model.encode([text]).tolist()[0]

def main():
    parser = argparse.ArgumentParser(description='Store text in vector DB')
    parser.add_argument('--text', '-t', required=True, help='Text to store')
    parser.add_argument('--metadata', '-m', required=True, help='JSON metadata string')
    parser.add_argument('--collection', '-c', default='research', help='Collection name')
    args = parser.parse_args()
    
    metadata = json.loads(args.metadata)
    
    # Initialize ChromaDB
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=str(VECTOR_DB_PATH),
        anonymized_telemetry=False
    ))
    
    # Get or create collection
    try:
        collection = client.get_collection(name=args.collection)
    except:
        collection = client.create_collection(name=args.collection)
    
    # Get embedding
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = get_embedding(args.text, model)
    
    # Add to collection
    collection.add(
        embeddings=[embedding],
        documents=[args.text],
        metadatas=[metadata],
        ids=[f"doc_{hash(args.text)}"]
    )
    
    print(f"Stored in collection '{args.collection}': {args.text[:100]}...")

if __name__ == '__main__':
    main()
