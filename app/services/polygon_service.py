# Example
import boto3
from botocore.config import Config
from .utils import setup_logger

logger = setup_logger(__name__)
class PolygonService:
    def __init__(self, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        """
        Initialize Polygon.io S3 service
        Args:
            aws_access_key_id: AWS access key for Polygon.io
            aws_secret_access_key: AWS secret key for Polygon.io
        """
        logger.info("Initializing PolygonService")
        try:
            self.session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            
            self.s3_client = self.session.client(
                's3',
                endpoint_url='https://files.polygon.io',
                config=Config(signature_version='s3v4'),
            )
            logger.debug("Successfully initialized S3 client")
        except Exception as e:
            logger.error(f"Failed to initialize PolygonService: {str(e)}")
            raise


    def list_files(self, prefix: str = 'us_options_opra') -> list[str]:
        """
        List all files under a specific prefix in Polygon.io S3
        Args:
            prefix: S3 prefix to list files from
        Returns:
            list[str]: List of file paths
        """
        logger.info(f"Listing files with prefix: {prefix}")
        try:
            paginator = self.s3_client.get_paginator('list_objects_v2')
            files = []
            
            for page in paginator.paginate(Bucket='flatfiles', Prefix=prefix):
                for obj in page['Contents']:
                    files.append(obj['Key'])
                    
            logger.debug(f"Found {len(files)} files")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            raise


    def download_file(self, file_path: str, dest_path: str) -> str:
        """
        Download a file from Polygon.io S3
        Args:
            file_path: Full path of file in S3 (e.g., 'us_options_opra/trades_v1/2024/03/2024-03-19.csv.gz')
            dest_path: Local path where the file should be saved
        Returns:
            str: Path where the file was downloaded
        """
        logger.info(f"Downloading {file_path} to {dest_path}")
        try:
            self.s3_client.download_file('flatfiles', file_path, dest_path)
            logger.debug(f"Successfully downloaded {file_path}")
            return dest_path
        except Exception as e:
            logger.error(f"Error downloading file {file_path}: {str(e)}")
            raise





