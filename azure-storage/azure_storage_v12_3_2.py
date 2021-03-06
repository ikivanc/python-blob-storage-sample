from azure.storage.blob import BlobClient, BlobServiceClient
from dotenv import load_dotenv
import os
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

    # Instantiate a new BlobServiceClient and a new ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    for u in url_list:
        print(f"copying file: {u} to blob storage...")
        # Download file from url then upload blob file
        r = requests.get(u, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            blob_client = container_client.get_blob_client(get_filename_from_url(u))
            blob_client.upload_blob(r.raw,overwrite=True)

def create_blob_from_path(storage_connection_string,container_name):
    # Instantiate a new BlobServiceClient and a new ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    for f in list_files():
        print(f"uploading local file: {f} to blob storage...")
        with open(f["local_path"], "rb") as data:
            blob_client = container_client.get_blob_client(f["file_name"])
            blob_client.upload_blob(data,overwrite=True)

def download_blob_from_file_name(storage_connection_string,container_name,file_name):
    # Instantiate a new BlobServiceClient and a new ContainerClient
    blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)

    # download file into data folder
    with open("./data/"+file_name, "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)

if __name__ == '__main__':

    # load en vars
    load_dotenv()
    # get storage account settings
    storage_connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    container_name = os.environ["STORAGE_CONTAINER"]

    # # if you want to copy from a public url
    # create_blob_from_url(storage_connection_string,container_name)
    
    # OR if you want to upload form your local drive
    #create_blob_from_path(storage_connection_string,container_name)

    # test sample with a sample data file to download blob storage
    download_blob_from_file_name(storage_connection_string,container_name,"stock-MSFT-2020-09-03.csv")

    print("done!")
