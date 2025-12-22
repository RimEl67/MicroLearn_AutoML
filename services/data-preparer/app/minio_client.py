from minio import Minio
import os

client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False
)

def upload_file(bucket, object_name, file_path):
    client.fput_object(bucket, object_name, file_path)
