import re
class  text_cleaner:
    def __init__(self):
        pass
    import re

class TextCleaner:

    def __init__(self):
        pass

    def clean_documents(self, documents):

        for doc in documents:

            text = doc.page_content

            # Remove extra spaces
            text = re.sub(r'\s+', ' ', text)

            # Remove extra blank lines
            text = re.sub(r'\n+', '\n', text)

            # Remove tabs
            text = text.replace('\t', ' ')

            # Remove non-printable characters
            text = re.sub(r'[^\x20-\x7E\n]', '', text)

            # Strip leading/trailing spaces
            text = text.strip()

            doc.page_content = text

        print(f"Cleaned {len(documents)} documents")

        return documents
    