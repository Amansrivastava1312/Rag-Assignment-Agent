from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

class Chunker:
    def __init__(self):
        pass
    def chunk(self,documents):
        embedding = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        text_splitter = SemanticChunker(
            embeddings=embedding
        )
        chunks = text_splitter.split_documents(
            documents=documents
        )
        return chunks