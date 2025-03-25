FROM python:3.9

RUN pip install kfserving scikit-learn joblib pandas

COPY model_server.py /app/model_server.py
ENV MODEL_NAME=sklearn-model
ENV STORAGE_URI=/mnt/models

CMD ["python", "/app/model_server.py"]
