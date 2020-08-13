# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: azure_storage_async.py
DESCRIPTION:
    This sample demos basic blob operations like getting a blob client from container, uploading and downloading
    a blob using the blob_client.
USAGE: python azure_storage_async.py
    Set the environment variables with your own values before running the sample:
    1) AZURE_STORAGE_CONNECTION_STRING - the connection string to your storage account
"""

import os
import asyncio
from dotenv import load_dotenv

# set up
DEST_FILE = 'BlockDestination.txt'
SOURCE_FILE = 'SampleSource.txt'

class BlobSamplesAsync(object):

    # load en vars
    load_dotenv()    
    # load connection string
    connection_string = os.environ["STORAGE_CONNECTION_STRING"]

    #--Begin Blob Samples-----------------------------------------------------------------

    async def create_container_sample_async(self):
        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob.aio import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            # Instantiate a new ContainerClient
            container_client = blob_service_client.get_container_client("mycontainerasync")

            try:
                # Create new container in the service
                await container_client.create_container()
                print('container is created')
                
                # List containers in the storage account
                my_containers = []
                async for container in blob_service_client.list_containers():
                    my_containers.append(container)

            finally:
                # Delete the container
                await container_client.delete_container()
                print('container is deleted')

    async def block_blob_sample_async(self):
        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob.aio import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            # Instantiate a new ContainerClient
            container_client = blob_service_client.get_container_client("myblockcontainerasync")

            try:
                # Create new Container in the service
                await container_client.create_container()
                print('container is created')

                # Instantiate a new BlobClient
                blob_client = container_client.get_blob_client("myblockblob")

                # [START upload_a_blob]
                # Upload content to block blob
                with open(SOURCE_FILE, "rb") as data:
                    await blob_client.upload_blob(data, blob_type="BlockBlob")
                    print('done! blob is uploaded')
                # [END upload_a_blob]

                # [START download_a_blob]
                with open(DEST_FILE, "wb") as my_blob:
                    stream = await blob_client.download_blob()
                    data = await stream.readall()
                    my_blob.write(data)
                    print('done! blob is downloaded')
                # [END download_a_blob]

                # [START delete_blob]
                await blob_client.delete_blob()
                # [END delete_blob]

            finally:
                # Delete the container
                await container_client.delete_container()
                print('container is deleted')

    async def page_blob_sample_async(self):
        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob.aio import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            # Instantiate a new ContainerClient
            container_client = blob_service_client.get_container_client("mypagecontainerasync")

            try:
                # Create new Container in the Service
                await container_client.create_container()
                print('container is created')

                # Instantiate a new BlobClient
                blob_client = container_client.get_blob_client("mypageblob")

                # Upload content to the Page Blob
                data = b'abcd'*128
                await blob_client.upload_blob(data, blob_type="PageBlob")

                # Download Page Blob
                with open(DEST_FILE, "wb") as my_blob:
                    stream = await blob_client.download_blob()
                    data = await stream.readall()
                    my_blob.write(data)

                # Delete Page Blob
                await blob_client.delete_blob()
                print('done! blob is deleted')

            finally:
                # Delete container
                await container_client.delete_container()
                print('container is deleted')

    async def append_blob_sample_async(self):
        # Instantiate a new BlobServiceClient using a connection string
        from azure.storage.blob.aio import BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)

        async with blob_service_client:
            # Instantiate a new ContainerClient
            container_client = blob_service_client.get_container_client("myappendcontainerasync")

            try:
                # Create new Container in the Service
                await container_client.create_container()
                print('container is created')

                # Get the BlobClient
                blob_client = container_client.get_blob_client("myappendblob")

                # Upload content to the append blob
                with open(SOURCE_FILE, "rb") as data:
                    await blob_client.upload_blob(data, blob_type="AppendBlob")
                    print('done! blob is appended')

                # Download append blob
                with open(DEST_FILE, "wb") as my_blob:
                    stream = await blob_client.download_blob()
                    data = await stream.readall()
                    my_blob.write(data)

                # Delete append blob
                await blob_client.delete_blob()
                print('done! blob is deleted')

            finally:
                # Delete container
                await container_client.delete_container()
                print('container is deleted')

async def main():
    sample = BlobSamplesAsync()
    await sample.create_container_sample_async()
    await sample.block_blob_sample_async()
    await sample.append_blob_sample_async()
    await sample.page_blob_sample_async()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())