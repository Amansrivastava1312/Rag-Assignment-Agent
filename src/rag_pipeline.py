from src.document_loader import DocumentLoader
from src.text_cleaner import TextCleaner
from src.chunking import Chunker
from src.embeddings import Embeddings
from src.vector_store import VectorStore
from pathlib import Path
from src.agent_tool import send_email,export_pdf,export_txt
from src.retriever import MainRetriever
from src.generator import Generation
from src.intent_log import log_intent
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
    def ask_question_agentic(self, question):
        generator = Generation()

        plan = generator.parse_intent(question)
        print("Intent:", plan)

        real_question = plan.get("question") or question
        rtrv = MainRetriever()
        context = rtrv.TopK(real_question, self.vector_db, 3)
        answer = generator.ask_question(real_question, context)

        log_intent(question, plan, answer)

        # ---- ACT ON INTENT ----
        file_path = None
        if plan.get("export") == "pdf":
            file_path = export_pdf(real_question, answer)
        elif plan.get("export") == "txt":
            file_path = export_txt(real_question, answer)

        if plan.get("email"):
            to_addr = plan.get("email_to") or "aman@yopmail.com"
            send_email(
                to_address=to_addr,
                subject="Your AI Advisor Response",
                body=f"Question:\n{real_question}\n\nAnswer:\n{answer}",
                attachment=file_path,      # attaches PDF/TXT if created
            )

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

        

