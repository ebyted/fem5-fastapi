# Dockerfile for Becalm FastAPI/Flask app
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8034

CMD ["python", "app.py"]
