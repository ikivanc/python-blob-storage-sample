from azure.storage.blob import BlobClient
from dotenv import load_dotenv
import os
import json
from urllib.parse import urlparse
import requests

def list_files() -> []:
    file_list = []
    
    for root, dirs, files in os.walk("data"):
        for name in files:
            file_list.append({"file_name": name, "local_path": os.path.join(root,name)})
    
    return file_list

def get_filename_from_url(url: str) -> str:
    file_name=url.split('/')[-1]
    
    return file_name


def get_random_images() -> []:
    # helper function uses loremflickr.com to get a random list of images 
    images = []

    for i in range(10):
        resp = requests.get(url=f"https://loremflickr.com/json/320/240?random={i}")
        resp_json = resp.json()
        images.append(resp_json["file"])

    return images

def create_blob_from_url(storage_connection_string,container_name):
    # urls to fetch into blob storage
    url_list = get_random_images()

    for u in url_list:
        print(f"copying file: {u} to blob storage...")

        # Download file from url to push as blob
        r = requests.get(u, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            block_blob_service = BlobClient.from_connection_string(conn_str=storage_connection_string, container_name=container_name, blob_name=get_filename_from_url(u))
            block_blob_service.upload_blob(r.raw,overwrite=True)

def create_blob_from_path(storage_connection_string,container_name):
    for f in list_files():
        print(f"uploading local file: {f} to blob storage...")
        block_blob_service = BlobClient.from_connection_string(conn_str=storage_connection_string, container_name=container_name, blob_name=f["file_name"])
        with open(f["local_path"], "rb") as data:
            block_blob_service.upload_blob(data,overwrite=True)

if __name__ == '__main__':

    # load en vars
    load_dotenv()
    # get storage account settings
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    container_name = os.environ["STORAGE_CONTAINER"]

    # if you want to copy from a public url
    #create_blob_from_url(storage_connection_string,container_name)
    
    # OR if you want to upload form your local drive
    create_blob_from_path(storage_connection_string,container_name)

    print("done!")
