from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class DocumentLoader:
    """
    Loads and chunks documents for the knowledge base.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def load_documents(self, directory_path: str) -> List[Document]:
        """
        Loads all supported files from a directory.
        """
        documents = []
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return []

        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if filename.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif filename.endswith(".txt") or filename.endswith(".md"):
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {filename}: {e}")

        return self.text_splitter.split_documents(documents)
