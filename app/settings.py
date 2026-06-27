from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ollama_base_url: str = "http://ollama:11434"
    llm_model: str = "llama3.2"
    embed_model: str = "nomic-embed-text"
    llm_temperature: float = 0.1
    llm_num_ctx: int = 4096

    redis_url: str = "redis://redis:6379"
    redis_key_prefix: str = "soporte:"
    redis_ttl_seconds: int = 86400

    chroma_dir: str = "/app/data/chroma_db"
    chroma_collection: str = "docs_soporte"
    documents_dir: str = "/app/documentos_soporte"

    retriever_k: int = 4
    chunk_size: int = 512
    chunk_overlap: int = 64


@lru_cache
def get_settings() -> Settings:
    return Settings()
