# Azure Storage
A sample project showing how to upload files to Azure Storage using 2 methods
- **Directly from a local folder on your machine**  
I've included a sample "data" folder containing 10 csv files conatining the MSFT stock price history for a specific date.

- **Copied from a web-accessible URL**  
(this is useful if you're trying to transfer files between a web location and Azure storage - you don't need to download the files and then upload to Azure - Azure Storage can get the file directly from the source)  
For the web-accessible url's, I've included a helper function that gets 10 random images from http://loremflickr.com

## Run the project

I used Python 3.6.8 for this, but it should be fine on other 3.x versions as well.

1. Create a virtual environment  
`python -m venv .venv`

2. Rename the `.env.sample.txt` file to `.env`  
This contains the environment variables that you need to set for your Azure Storage account

3. Set each of the variables in the .env file:  
`STORAGE_ACCOUNT_NAME`  
`STORAGE_KEY`  
`STORAGE_CONTAINER`

4. Install the dependencies  
`pip install -r requirements.txt`

5. Comment/uncomment the call to the function that you want to test:
```
# if you want to copy from a public url
create_blob_from_url(block_blob_service)

# OR if you want to upload form your local drive
#create_blob_from_path(block_blob_service)
```

6. Run the project!



