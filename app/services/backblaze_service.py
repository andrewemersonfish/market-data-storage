import boto3
from b2sdk.v2 import InMemoryAccountInfo, B2Api
from b2sdk.v2.exception import FileNotPresent
from .utils import setup_logger

logger = setup_logger(__name__)

class BackblazeService:
    def __init__(self, key_id: str, application_key: str) -> None:
        """
        Initialize Backblaze B2 service
        Args:
            key_id: Backblaze key ID
            application_key: Backblaze application key
        """
        logger.info("Initializing BackblazeService")
        try:
            self.info = InMemoryAccountInfo()
            self.api = B2Api(self.info)
            self.api.authorize_account("production", key_id, application_key)
            
            self.bucket = self.api.get_bucket_by_name("polygon-market-data")
            logger.debug("Successfully connected to B2 bucket")
        except Exception as e:
            logger.error(f"Failed to initialize BackblazeService: {str(e)}")
            raise
            
    def file_exists(self, file_path: str) -> bool:
        """
        Check if a file exists in B2 bucket
        Args:
            file_path: Path to file in B2 bucket
        Returns:
            bool: True if file exists, False otherwise
        """
        logger.debug(f"Checking if file exists: {file_path}")
        try:
            self.bucket.get_file_info_by_name(file_path)
            logger.info(f"File exists: {file_path}")
            return True
        except FileNotPresent:
            logger.info(f"File does not exist: {file_path}")
            return False
        except Exception as e:
            logger.error(f"Error checking file existence: {str(e)}")
            raise
            
    def upload_file(self, local_path: str, destination_path: str) -> str:
        """
        Upload a file to B2 bucket
        Args:
            local_path: Path to local file to upload
            destination_path: Path where file should be stored in B2
        Returns:
            str: Path where file was uploaded
        """
        logger.info(f"Uploading {local_path} to {destination_path}")
        try:
            self.bucket.upload_local_file(
                local_file=local_path,
                file_name=destination_path,
            )
            logger.debug(f"Successfully uploaded to {destination_path}")
            return destination_path
        except Exception as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise
            
    def download_file(self, source_path: str, local_path: str) -> str:
        """
        Download a file from B2 bucket
        Args:
            source_path: Path to file in B2 bucket
            local_path: Local path where file should be downloaded
        Returns:
            str: Path where file was downloaded
        """
        logger.info(f"Downloading {source_path} to {local_path}")
        try:
            downloaded_file = self.bucket.download_file_by_name(source_path)
            downloaded_file.save_to(local_path)
            logger.debug(f"Successfully downloaded to {local_path}")
            return local_path
        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise