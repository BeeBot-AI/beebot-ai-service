from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)

def chunk_text(text: str) -> list[str]:
    """Split raw text into semantic chunks for embedding."""
    return text_splitter.split_text(text)
