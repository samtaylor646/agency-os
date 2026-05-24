FROM python:3.11-slim
WORKDIR /workspace
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r ./server/requirements.txt
COPY . .
CMD ["python", "server/api_server.py"]
