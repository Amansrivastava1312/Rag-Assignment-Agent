from src.rag_pipeline import RagPipeLine

def main():
    rg = RagPipeLine()
    print("Initializing RAG Pipeline")

    print("check db already exist")
    db_exist = rg.check_db_exist()
    if not db_exist: 
        print("Creating new  db")
        db = rg.create_embedding()
    else:
        print("Loading Existing Vector Database")
        rg.load_db()

    print("RAG Ready ")

    while True:

        question = input("\nAsk Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            break

        answer = rg.ask_question_agentic(question)

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    main()