from google.cloud import storage
from dotenv import load_dotenv
import os
from datetime import timedelta

# load environment variables for Google Cloud Storage
load_dotenv()

class GoogleStorageService:
    """
    Service class for Google Cloud Storage related operations
    """


    @staticmethod
    def upload_blob(source_file_name, destination_blob_name) -> str:
        """
        Uploads a file to the bucket.
        
        Parameters
        ----------
        source_file_name : str
            Path to the file to upload
        destination_blob_name : str
            Destination blob name

        Returns
        -------
        str
        """
        
        # get the bucket name from the environment variables 
        bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET")
        # create a storage client
        storage_client = storage.Client()
        # get the bucket
        bucket = storage_client.bucket(bucket_name)
        # create a blob
        blob = bucket.blob(destination_blob_name)

        # upload the file
        with open(source_file_name, "r") as f:
            blob.upload_from_file(f)

        # get the public url
        public_url = blob.generate_signed_url(
            version="v4",
            # This URL will expire in 7 days.
            expiration=timedelta(hours=168),
            # Allow GET requests using this URL.
            method="GET")

        # return the public url
        return public_url

    @staticmethod
    def create_and_upload_file(destination_blob_name, content) -> str:
        """
        Create a file and upload it to the bucket.
        
        Parameters
        ----------
        destination_blob_name : str
            Destination blob name
        content : str
            Content of the file

        Returns
        -------
        str

        """

        file_name = f"{destination_blob_name}.txt"
        with open(file_name, 'w') as f:
            f.write(content)
        url = GoogleStorageService.upload_blob(file_name, destination_blob_name)
        os.remove(file_name)
        return url