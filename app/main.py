import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chain_builder import get_soporte_chain, get_vectorstore, index_documents
from app.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Asistente de Soporte Técnico RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Consulta(BaseModel):
    consulta: str
    session_id: str = "default"


@app.on_event("startup")
def startup():
    cfg = get_settings()
    try:
        vs = get_vectorstore()
        count = vs._collection.count()
        if count == 0:
            logger.info("ChromaDB vacío, indexando...")
            n = index_documents()
            logger.info("Indexados %s fragmentos", n)
        else:
            logger.info("ChromaDB ya tiene %s fragmentos", count)
    except Exception as e:
        logger.warning("Error al verificar ChromaDB, indexando: %s", e)
        try:
            n = index_documents()
            logger.info("Indexados %s fragmentos", n)
        except Exception as e2:
            logger.error("Error indexando: %s", e2)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/ready")
def ready():
    import httpx
    import redis as r

    checks = {"redis": False, "chroma": False, "ollama": False}

    try:
        client = r.from_url(get_settings().redis_url)
        client.ping()
        checks["redis"] = True
    except Exception as e:
        checks["redis_error"] = str(e)

    try:
        vs = get_vectorstore()
        count = vs._collection.count()
        checks["chroma"] = count > 0
        checks["chroma_chunks"] = count
    except Exception as e:
        checks["chroma_error"] = str(e)

    try:
        resp = httpx.get(f"{get_settings().ollama_base_url}/api/tags", timeout=5)
        checks["ollama"] = True
        checks["ollama_models"] = [m["name"] for m in resp.json().get("models", [])]
    except Exception as e:
        checks["ollama_error"] = str(e)

    return {"status": "ready", "checks": checks}


@app.post("/soporte/consultar")
def consultar(body: Consulta):
    chain = get_soporte_chain()
    try:
        respuesta = chain.invoke({"input": body.consulta})
    except Exception as e:
        logger.exception("Error en cadena")
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "respuesta": respuesta,
        "fuentes": [],
        "session_id": body.session_id,
    }


@app.post("/admin/reindex")
def reindex():
    get_soporte_chain.cache_clear()
    try:
        n = index_documents()
        return {"status": "ok", "chunks_indexados": n}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
