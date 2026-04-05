import os
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader, BSHTMLLoader
)
from langchain_core.documents import Document

class UniversalLoader:
    def __init__(self, dir: str):
        self.dir = dir

    def load(self) -> List[Document]:
        docs :List[Document] = []
        for filename in os.listdir(self.dir):
            path = os.path.join(self.dir, filename)
            if not os.path.isfile(path):
                continue

            if filename.lower().endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif filename.lower().endswith(".docx"):
                loader = Docx2txtLoader(path)
            elif filename.lower().endswith(".md"):
                loader = UnstructuredMarkdownLoader(path)
            elif filename.lower().endswith((".html", ".htm")):
                loader = BSHTMLLoader(path)
            else:
                continue

            file_docs = loader.load()
            for d in file_docs:
                d.metadata["source"] = filename
                docs.append(d)

        return docs
    

# loader = UniversalLoader("../data")
# document = loader.load()