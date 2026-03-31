import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.documents import Document

def parse_file(file_bytes: bytes, filename: str) -> list[Document]:
    """
    Extract text from uploaded file bytes and return LangChain Documents.
    Supports: PDF (.pdf), Word (.docx), plain text (.txt).
    """
    name_lower = filename.lower()
    
    # Langchain loaders usually require a file path, so we use a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        if name_lower.endswith(".pdf"):
            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            
        elif name_lower.endswith(".docx"):
            loader = Docx2txtLoader(temp_path)
            docs = loader.load()
            
        else:
            # Plain text fallback
            try:
                text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                text = file_bytes.decode("latin-1")
            
            docs = [Document(page_content=text, metadata={"source": filename})]
            
        # Ensure all docs have the basic source metadata
        for doc in docs:
            doc.metadata["source"] = filename
            
        return docs
        
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
