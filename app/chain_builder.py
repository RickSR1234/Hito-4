from functools import lru_cache
from pathlib import Path

from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.settings import get_settings


def get_embeddings():
    cfg = get_settings()
    return OllamaEmbeddings(model=cfg.embed_model, base_url=cfg.ollama_base_url)


def get_vectorstore():
    cfg = get_settings()
    return Chroma(
        persist_directory=cfg.chroma_dir,
        embedding_function=get_embeddings(),
        collection_name=cfg.chroma_collection,
    )


def index_documents():
    cfg = get_settings()
    loader = DirectoryLoader(
        cfg.documents_dir,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.chunk_size,
        chunk_overlap=cfg.chunk_overlap,
    )
    chunks = splitter.split_documents(docs)
    Path(cfg.chroma_dir).mkdir(parents=True, exist_ok=True)
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=cfg.chroma_dir,
        collection_name=cfg.chroma_collection,
    )
    return vs._collection.count()


def _format_docs(docs: list[Document]) -> str:
    return "\n\n---\n\n".join(
        f"[Fragmento {i+1} - Fuente: {d.metadata.get('source','doc')}]\n{d.page_content}"
        for i, d in enumerate(docs)
    )


@lru_cache
def get_soporte_chain():
    cfg = get_settings()

    llm = ChatOllama(
        model=cfg.llm_model,
        temperature=cfg.llm_temperature,
        base_url=cfg.ollama_base_url,
    )

    vs = get_vectorstore()
    retriever = vs.as_retriever(search_kwargs={"k": cfg.retriever_k})

    prompt = ChatPromptTemplate.from_messages([
        ("human",
         "Eres un asistente de soporte técnico. "
         "Responde la siguiente pregunta usando ÚNICAMENTE la documentación que se te entrega. "
         "Si la información está en los documentos, responde de forma detallada en español. "
         "Indica al final qué documento usaste.\n\n"
         "DOCUMENTACIÓN RECUPERADA:\n{context}\n\n"
         "PREGUNTA: {input}\n\n"
         "RESPUESTA:")
    ])

    def get_context(inp: dict) -> str:
        docs = retriever.invoke(inp["input"])
        return _format_docs(docs)

    def get_sources(inp: dict) -> list[str]:
        docs = retriever.invoke(inp["input"])
        return list({d.metadata.get("source", "doc") for d in docs})

    chain = (
        RunnablePassthrough.assign(context=RunnableLambda(get_context))
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain
