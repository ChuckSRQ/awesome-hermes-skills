#!/usr/bin/env python3
"""List all collections in the vector database."""

import chromadb
from chromadb.config import Settings
from pathlib import Path

VECTOR_DB_PATH = Path.home() / ".hermes" / "vector_db"

def main():
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=str(VECTOR_DB_PATH),
        anonymized_telemetry=False
    ))
    
    collections = client.list_collections()
    
    if not collections:
        print("No collections found. Create one by storing a document.")
        return
    
    print(f"Found {len(collections)} collection(s):\n")
    for col in collections:
        count = col.count()
        print(f"  - {col.name}: {count} documents")

if __name__ == '__main__':
    main()
