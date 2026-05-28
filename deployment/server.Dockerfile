FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git sqlite3 docker.io && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r ./server/requirements.txt

# Copy only what's needed for the server to run
COPY server/ ./server/
COPY config/ ./config/
COPY agents/ ./agents/
COPY scripts/ ./scripts/
# COPY seed_db.py ./

# Explicitly set PYTHONPATH so that imports work
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "5000"]
