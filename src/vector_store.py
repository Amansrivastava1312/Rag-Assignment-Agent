from pathlib import Path
from langchain_chroma import Chroma

CHROMA_DIR = "vector_db"

class VectorStore:

    def __init__(self):
        pass

    def create_vector_store(self,  embedding_model,chunks=None):

        if Path(CHROMA_DIR).exists():

            print("Loading existing vector database...")

            vector_db = Chroma(
                persist_directory=CHROMA_DIR,
                embedding_function=embedding_model
            )

        else:

            print("Creating new vector database...")

            vector_db = Chroma.from_documents(
                documents=chunks,
                embedding=embedding_model,
                persist_directory=CHROMA_DIR
            )

        return vector_db