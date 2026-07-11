"""
Run this once from your project root to scaffold the entire folder/file structure.
Usage: python setup_structure.py
"""

import os

# Files that should have starter content instead of being blank
STARTER_CONTENT = {
    "config/config.yaml": "# All tunable pipeline parameters go here\n",
    ".gitignore": (
        "venv/\n"
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        "*.log\n"
        "chroma_db/\n"
        ".DS_Store\n"
    ),
    ".env": "# API keys go here — never commit this file\n",
    "README.md": "# Research Digest Automation\n\nAgentic RAG pipeline for staying current on GPU/LLM research.\n",
    "requirements.txt": "",  # you already have this filled in
    "Dockerfile": "# Dockerfile goes here\n",
}

STRUCTURE = {
    "config": ["config.yaml"],
    "src": ["__init__.py"],
    "src/entity": [
        "__init__.py",
        "ingestion_config.py",
        "relevance_config.py",
        "summarization_config.py",
        "vectorstore_config.py",
        "email_config.py",
    ],
    "src/config": ["__init__.py", "configuration.py"],
    "src/components": [
        "__init__.py",
        "ingestion.py",
        "relevance_gate.py",
        "summarizer.py",
        "vectorstore.py",
        "email_sender.py",
    ],
    "src/services": [
        "__init__.py",
        "query_router.py",
        "retrieval_service.py",
        "chat_service.py",
    ],
    "src/pipeline": ["__init__.py", "ingestion_pipeline.py"],
    "src/api": ["__init__.py", "main.py"],
    "src/api/routes": ["__init__.py", "chat.py", "digest.py"],
    "src/constants": ["__init__.py", "constants.py"],
    "src/utils": ["__init__.py", "common.py"],
    "frontend": [],
    ".github/workflows": ["ingestion_schedule.yml", "deploy.yml"],
}

ROOT_FILES = [".env", ".gitignore", "Dockerfile", "requirements.txt", "setup.py", "README.md"]


def create_file(path: str):
    if os.path.exists(path):
        print(f"  skip (exists): {path}")
        return
    content = STARTER_CONTENT.get(path.replace(os.sep, "/"), "")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  created: {path}")


def main():
    print("Scaffolding project structure...\n")

    for folder, files in STRUCTURE.items():
        os.makedirs(folder, exist_ok=True)
        print(f"folder: {folder}/")
        for fname in files:
            create_file(os.path.join(folder, fname))

    print("\nroot files:")
    for fname in ROOT_FILES:
        create_file(fname)

    print("\nDone. Structure created.")


if __name__ == "__main__":
    main()