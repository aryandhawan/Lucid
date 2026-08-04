#!/bin/bash
python -m venv antenv
source antenv/bin/activate
pip install -r src/api/requirements_chat.txt
uvicorn src.api.chat_server:app --host 0.0.0.0 --port 8000