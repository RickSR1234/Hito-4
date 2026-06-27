# Hito-4

#ejecutar todo ello en orden , para correr el proyecto
docker compose up -d

powershelldocker compose exec ollama ollama pull nomic-embed-text

powershelldocker compose exec ollama ollama pull llama3.2

powershelldocker compose exec api python -c "from app.chain_builder import index_documents; n=index_documents(); print('Fragmentos indexados:', n)"

powershelldocker compose restart api
