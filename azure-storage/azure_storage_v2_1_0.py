from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage.blob.models import Blob
from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import requests

def list_files() -> []:
    file_list = []
    
    for root, dirs, files in os.walk("data"):
        for name in files:
            file_list.append({"file_name": name, "local_path": os.path.join(root,name)})
    
    return file_list

def get_filename_from_url(url: str) -> str:
    parsed=urlparse(url)

    return os.path.basename(parsed.path)


def get_random_images() -> []:
    # helper function uses loremflickr.com to get a random list of images 
    images = []

    for i in range(10):
        resp = requests.get(url=f"https://loremflickr.com/json/320/240?random={i}")
        resp_json = resp.json()
        images.append(resp_json["file"])

    return images

def create_blob_from_url(block_blob_service):

    # urls to fetch into blob storage
    url_list = get_random_images()

    for u in url_list:
        print(f"copying file: {u} to blob storage...")
        block_blob_service.copy_blob(container_name,get_filename_from_url(u),u)

def create_blob_from_path(block_blob_service):
    for f in list_files():
        print(f"uploading local file: {f} to blob storage...")
        block_blob_service.create_blob_from_path(container_name, f["file_name"], f["local_path"])

if __name__ == '__main__':

    # load en vars
    load_dotenv()
    # get storage account settings
    storage_name = os.environ["STORAGE_ACCOUNT_NAME"]
    storage_key = os.environ["STORAGE_KEY"]
    container_name = os.environ["STORAGE_CONTAINER"]

    block_blob_service = BlockBlobService(account_name=storage_name, account_key=storage_key)

    # Createcontainer - must be lowercase 
    # if the container already exists - it will do nothing
    block_blob_service.create_container(container_name)
    # [OPTIONAL] Set the permission so the blobs are public.
    block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

    # if you want to copy from a public url
    create_blob_from_url(block_blob_service)
    
    # OR if you want to upload form your local drive
    #create_blob_from_path(block_blob_service)

    print("done!")
