import os
from azure.storage.blob import BlobServiceClient

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "vectorstore-backup"
LOCAL_DIR = "./vectorstore"

def download_vectorstore():
    blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service.get_container_client(CONTAINER_NAME)

    os.makedirs(LOCAL_DIR, exist_ok=True)

    blobs = container_client.list_blobs()
    for blob in blobs:
        local_path = os.path.join(LOCAL_DIR, blob.name)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)  # handles nested folders inside vectorstore
        with open(local_path, "wb") as f:
            download_stream = container_client.download_blob(blob.name)
            f.write(download_stream.readall())

    print("Vectorstore downloaded from Blob Storage.")


def upload_vectorstore():
    blob_service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service.get_container_client(CONTAINER_NAME)

    for root, dirs, files in os.walk(LOCAL_DIR):
        for filename in files:
            local_path = os.path.join(root, filename)
            blob_name = os.path.relpath(local_path, LOCAL_DIR)  # preserves folder structure in blob names
            with open(local_path, "rb") as f:
                container_client.upload_blob(name=blob_name, data=f, overwrite=True)

    print("Vectorstore uploaded to Blob Storage.")