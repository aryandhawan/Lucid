FROM python:3.12-slim

WORKDIR /app

COPY . . 

RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r src/api/requirements_chat.txt

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "src.api.chat_server:app", "--host", "0.0.0.0", "--port", "8000"]
