class MainRetriever:
    def __init__(self):
        pass
    def TopK(self,question,vector_db,top_k):
        retriever=vector_db.as_retriever(search_kwargs={"k":top_k})
        
        retrieved_docs=retriever.invoke(question)
        context="\n\n".join(doc.page_content for doc in retrieved_docs)
        return context