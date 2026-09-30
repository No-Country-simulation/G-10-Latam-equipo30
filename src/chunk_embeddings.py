from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import SecretStr

from the_keys import GEMINI_API_KEY
from the_models import GEMINI_EMBEDDINGS


def chunk_embeddings(docs):

    print("\n--- chunk_embeddings -- Muestra del texto limpio ---")
    print(docs[0].page_content[:300])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs_splits = splitter.split_documents(docs)

    # Crear Embeddings
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    modelo_embeddings = GoogleGenerativeAIEmbeddings(
        model=GEMINI_EMBEDDINGS,
        api_key=SecretStr(GEMINI_API_KEY) if GEMINI_API_KEY else None,
    )

    # Generando el Vector Store
    from langchain_community.vectorstores import FAISS

    vectorstore = FAISS.from_documents(docs_splits, modelo_embeddings)

    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.3, "k": 4},
    )

    vectorstore.save_local("vectorstore")
