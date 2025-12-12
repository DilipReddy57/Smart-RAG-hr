import os
import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import uuid

# Configuration
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'hr_policies')
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'chroma_db')
EMBEDDING_MODEL_NAME = 'all-MiniLM-L6-v2'

class LocalEmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self, model_name):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        return self.model.encode(input).tolist()

def load_documents(data_dir):
    documents = []
    print(f"Scanning {data_dir}...")
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.pdf'):
                category = os.path.basename(root)
                filepath = os.path.join(root, file)
                print(f"Processing: {filepath} (Category: {category})")
                
                try:
                    reader = PdfReader(filepath)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    
                    documents.append({
                        'text': text,
                        'metadata': {
                            'source': file,
                            'category': category,
                            'filepath': filepath
                        }
                    })
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    return documents

def split_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def main():
    # 1. Setup ChromaDB
    print("Initializing ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # Use SentenceTransformer for embeddings
    embedding_func = LocalEmbeddingFunction(EMBEDDING_MODEL_NAME)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="hr_policies",
        embedding_function=embedding_func
    )

    # 2. Load and Chunk Documents
    docs = load_documents(DATA_DIR)
    
    ids = []
    documents = []
    metadatas = []
    
    print("Chunking and Indexing...")
    for doc in docs:
        chunks = split_text(doc['text'])
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['metadata']['source']}_{i}_{str(uuid.uuid4())[:8]}"
            
            ids.append(chunk_id)
            documents.append(chunk)
            # Add chunk index to metadata
            meta = doc['metadata'].copy()
            meta['chunk_index'] = i
            metadatas.append(meta)

    # 3. Add to Chroma
    if documents:
        # Chroma handles batching, but let's do it if it's huge. 
        # For this scale, it's fine.
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Successfully added {len(documents)} chunks to the database.")
    else:
        print("No documents found to ingest.")

if __name__ == "__main__":
    main()
