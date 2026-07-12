from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

class DocumentLoader:

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir

    def load_pdf_files(self):
        return DirectoryLoader(
            self.data_dir,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        ).load()

    def load_docx_files(self):
        return DirectoryLoader(
            self.data_dir,
            glob="**/*.docx",
            loader_cls=Docx2txtLoader
        ).load()

    def load_txt_files(self):
        return DirectoryLoader(
            self.data_dir,
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        ).load()

    def load_all_documents(self):

        documents = []

        documents.extend(self.load_pdf_files())
        documents.extend(self.load_docx_files())
        documents.extend(self.load_txt_files())

        print(
            f"Loaded {len(documents)} documents from {self.data_dir}"
        )

        return documents