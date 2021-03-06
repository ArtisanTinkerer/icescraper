import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings


def upload(local_file_name: str):
    """
    Upload to Azure using FTP
    https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-blob/azure/storage/blob/_blob_client.py#L375
    """
    az_key: str = os.getenv("AZ_STORAGE_KEY")
    az_string: str = os.getenv("AZ_STORAGE_CONNECTION_STRING")
    container_name: str = '$web'

    try:
        blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(az_string)
        blob_client: BlobClient = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

        print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)
        my_content_settings: ContentSettings = ContentSettings(content_type='text/html')

        with open('populated.html', "rb") as data:
            blob_client.upload_blob(data, overwrite=True, content_settings=my_content_settings)

    except Exception as ex:
        print('Exception:')
        print(ex)
