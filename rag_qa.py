import argparse
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from llm_client import get_llm

CHROMA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'chroma_db')
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

class LocalEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        return self.model.encode(input).tolist()

def retrieve_context(query, n_results=3):
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_func = LocalEmbeddingFunction(EMBEDDING_MODEL_NAME)
    collection = client.get_collection(name="hr_policies", embedding_function=embedding_func)
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    context = ""
    for i, doc in enumerate(results['documents'][0]):
        meta = results['metadatas'][0][i]
        context += f"\n--- Source: {meta['source']} (Category: {meta['category']}) ---\n{doc}\n"
    
    return context

def rag_pipeline(query):
    print(f"\nQuery: {query}")
    print("Retrieving context...")
    context = retrieve_context(query)
    print(f"Context found:\n{context}\n") 
    
    prompt = f"""Context:
{context}

Question: {query}

Answer the question based on the context above. If you don't know, say so.
Answer:"""

    print("Generating answer...")
    llm = get_llm()
    answer = llm.generate(prompt, max_tokens=300)
    print("\n=== ANSWER ===\n")
    print(answer)
    print("\n=============\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        rag_pipeline(query)
    else:
        print("Usage: python rag_qa.py 'Your question here'")
