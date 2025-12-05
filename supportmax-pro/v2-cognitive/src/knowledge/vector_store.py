import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
from config.settings import settings
from knowledge.document_loader import DocumentLoader

class VectorStore:
    """
    Manages the ChromaDB vector store for RAG.
    """
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIRECTORY)
        
        # Use OpenAI embeddings by default
        self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=settings.OPENAI_API_KEY,
            model_name="text-embedding-3-small"
        )
        
        self.collection = self.client.get_or_create_collection(
            name=settings.COLLECTION_NAME,
            embedding_function=self.embedding_fn
        )

    def ingest_documents(self, directory_path: str):
        """
        Loads and indexes documents from a directory.
        """
        loader = DocumentLoader()
        chunks = loader.load_documents(directory_path)
        
        if not chunks:
            print("No documents found to ingest.")
            return

        ids = [f"doc_{i}" for i in range(len(chunks))]
        documents = [chunk.page_content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]

        self.collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Ingested {len(chunks)} document chunks.")

    def search(self, query: str, n_results: int = 3) -> List[str]:
        """
        Semantic search for relevant documents.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Flatten results
        if results["documents"]:
            return results["documents"][0]
        return []
