from src.document_loader import DocumentLoader
from src.text_cleaner import TextCleaner
from src.chunking import Chunker
from src.embeddings import Embeddings
from src.vector_store import VectorStore
from pathlib import Path

from src.retriever import MainRetriever
from src.generator import Generation
class RagPipeLine:
    def __init__(self):
        self.vector_db = None
    def create_embedding(self):
        loader = DocumentLoader()
        docs = loader.load_all_documents()
        print("Document Loaded Success")

        clean = TextCleaner()
        cleaned_doc = clean.clean_documents(docs)
        print("Clean Success")

        chunking = Chunker()
        chunked_doc = chunking.chunk(cleaned_doc)
        print("chunking success")
        
        embd = Embeddings()
        embeding_model = embd.get_embedding_model() 
        print("embedding model success")

        vectorize=VectorStore()
        vector_db = vectorize.create_vector_store(embeding_model,chunked_doc)
        self.vector_db=vector_db
        print("Vectordb success")

        return vector_db
    
    def ask_question(self,question):
        
        rtrv = MainRetriever()
        context = rtrv.TopK(question,self.vector_db,3)

        generator = Generation()
        answer = generator.ask_question(question,context)
        return answer
    def load_db(self):
        embd = Embeddings()
        embedding_model = embd.get_embedding_model()
        vectorize = VectorStore()
        self.vector_db = vectorize.create_vector_store(
            embedding_model
            )
        print("Existing Vector DB Loaded")
    def check_db_exist(self):
            CHROMA_DIR = "vector_db"
            if Path(CHROMA_DIR).exists(): 
                 return True
            return False  

        

