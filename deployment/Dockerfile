FROM python:3.11-slim
WORKDIR /app
RUN pip install pyyaml flask flask-cors
COPY server/ /app/server/
COPY config/ /app/config/
ENV PYTHONPATH=/app
EXPOSE 5000
CMD ["python3", "server/api_server.py"]
