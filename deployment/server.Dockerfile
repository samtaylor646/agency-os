FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r ./server/requirements.txt
COPY . .
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "5000"]
