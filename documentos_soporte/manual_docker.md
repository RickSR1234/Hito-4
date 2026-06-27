# Manual Docker — Soporte Técnico

## ¿Qué es Docker?
Docker es una plataforma de contenedores que permite empaquetar aplicaciones junto a sus dependencias en unidades portables llamadas contenedores.

## Cómo crear una imagen Docker
Para crear una imagen se usa el comando `docker build`.

Pasos:
1. Crear un archivo `Dockerfile` en el directorio del proyecto.
2. Definir la imagen base:
```
FROM python:3.11-slim
```
3. Copiar archivos con `COPY`.
4. Instalar dependencias con `RUN`.
5. Exponer el puerto con `EXPOSE`.
6. Definir el comando de inicio con `CMD`.
7. Ejecutar:
```
docker build -t nombre-imagen:tag .
```

Ejemplo de Dockerfile completo:
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Cómo ejecutar un contenedor
```
docker run -d -p 8080:8000 --name mi-app nombre-imagen:tag
```
- `-d`: segundo plano
- `-p host:contenedor`: mapear puertos
- `--name`: nombre del contenedor

## Listar contenedores
```
docker ps          # en ejecución
docker ps -a       # todos
```

## Detener y eliminar contenedores
```
docker stop nombre
docker rm nombre
```

## Ver logs
```
docker logs nombre
docker logs -f nombre
```

## Docker Compose
```
docker compose up -d
docker compose down
docker compose logs -f
docker compose exec servicio bash
```

## Publicar imagen en Docker Hub
```
docker login
docker tag nombre usuario/repo:tag
docker push usuario/repo:tag
```

## Limpiar recursos
```
docker system prune
docker volume prune
docker image prune -a
```

## Preguntas frecuentes
¿Cómo ver imágenes descargadas?
```
docker images
```
¿Cómo entrar a un contenedor?
```
docker exec -it nombre bash
```
