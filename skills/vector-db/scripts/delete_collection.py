#!/usr/bin/env python3
"""Delete a collection from the vector database."""

import argparse
import chromadb
from chromadb.config import Settings
from pathlib import Path

VECTOR_DB_PATH = Path.home() / ".hermes" / "vector_db"

def main():
    parser = argparse.ArgumentParser(description='Delete a collection')
    parser.add_argument('--collection', '-c', required=True, help='Collection name to delete')
    args = parser.parse_args()
    
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
    client = chromadb.Client(Settings(
        persist_directory=str(VECTOR_DB_PATH),
        anonymized_telemetry=False
    ))
    
    try:
        client.delete_collection(name=args.collection)
        print(f"Deleted collection '{args.collection}'")
    except Exception as e:
        print(f"Error deleting collection: {e}")

if __name__ == '__main__':
    main()
