from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    """
    Create the embedding model used by the vector database.
    """

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


# ---------------------------------------------------------
# Load Markdown Documents
# ---------------------------------------------------------

def load_knowledge_base():
    """
    Load all Markdown files from knowledge_base/.
    """

    documents = []

    for file_path in KNOWLEDGE_BASE_DIR.rglob("*.md"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        category = file_path.parent.name

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": str(file_path),
                    "category": category,
                    "filename": file_path.name
                }
            )
        )

    return documents


# ---------------------------------------------------------
# Split Documents
# ---------------------------------------------------------

def split_documents(documents):
    """
    Split large documents into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    return chunks


# ---------------------------------------------------------
# Create Vector Store
# ---------------------------------------------------------

def create_vectorstore():
    """
    Create a Chroma vector database from the knowledge base.
    """

    documents = load_knowledge_base()

    if not documents:
        raise ValueError(
            "No Markdown files found in knowledge_base/"
        )

    chunks = split_documents(documents)

    embeddings = get_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(VECTORSTORE_DIR),
        collection_name="smart_city_knowledge"
    )

    return vectorstore


# ---------------------------------------------------------
# Load Existing Vector Store
# ---------------------------------------------------------

def get_vectorstore():
    """
    Load the existing Chroma vector database.
    """

    embeddings = get_embeddings()

    vectorstore = Chroma(
        persist_directory=str(VECTORSTORE_DIR),
        embedding_function=embeddings,
        collection_name="smart_city_knowledge"
    )

    return vectorstore


# ---------------------------------------------------------
# Retriever
# ---------------------------------------------------------

def get_retriever(k=4):
    """
    Return a retriever that finds the most relevant
    knowledge-base chunks.
    """

    vectorstore = get_vectorstore()

    return vectorstore.as_retriever(
        search_kwargs={
            "k": k
        }
    )


# ---------------------------------------------------------
# Search Knowledge Base
# ---------------------------------------------------------

def search_knowledge(query, k=4):
    """
    Search the knowledge base using the user's query.

    Returns relevant documents.
    """

    vectorstore = get_vectorstore()

    results = vectorstore.similarity_search(
        query,
        k=k
    )

    return results




# ---------------------------------------------------------
# Format Retrieved Context
# ---------------------------------------------------------

def get_context(query, k=4):
    """
    Retrieve relevant documents and combine them
    into a context string for the LLM.
    """

    documents = search_knowledge(
        query,
        k=k
    )

    if not documents:
        return ""

    context_parts = []

    for document in documents:

        source = document.metadata.get(
            "filename",
            "Unknown"
        )

        context_parts.append(
            f"Source: {source}\n"
            f"{document.page_content}"
        )

    return "\n\n---\n\n".join(
        context_parts
    )


def retrieve_context(query, k=4):
    """
    Retrieve relevant context from the knowledge base.
    Used by the AI agent.
    """
    return get_context(query, k=k)
