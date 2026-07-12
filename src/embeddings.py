from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class Embeddings:

    def __init__(self):
        pass

    def get_embedding_model(self):

        embedding_model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )

        return embedding_model
