# app/main.py

import os
from typing import List, Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.services.polygon_service import PolygonService
from app.services.backblaze_service import BackblazeService
from app.services.utils import setup_logger

logger = setup_logger(__name__)
load_dotenv()

app = FastAPI(
    title="Polygon Data Collector",
    description="API for transferring data between Polygon.io and Backblaze B2",
    version="1.0.0"
)

# Initialize services
polygon = PolygonService(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

b2 = BackblazeService(
    key_id=os.getenv('B2_KEY_ID'),
    application_key=os.getenv('B2_APPLICATION_KEY')
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/polygon/files", response_model=List[str])
async def list_polygon_files(prefix: str = "us_options_opra") -> List[str]:
    """
    List available files in Polygon.io S3 bucket
    Args:
        prefix: S3 prefix to list files from (default: "us_options_opra")
    Returns:
        List[str]: List of file paths in the S3 bucket
    """
    try:
        return polygon.list_files(prefix=prefix)
    except Exception as e:
        logger.error(f"Failed to list Polygon files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/polygon/download")
async def download_polygon_file(file_path: str) -> Dict[str, str]:
    """
    Download a file from Polygon.io S3
    Args:
        file_path: Full path of file (e.g., 'us_options_opra/trades_v1/2024/03/2024-03-19.csv.gz')
    Returns:
        Dict[str, str]: Dictionary containing the downloaded file path
    """
    try:
        return {"file": polygon.download_file(file_path)}
    except Exception as e:
        logger.error(f"Failed to download Polygon file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/backblaze/check")
async def check_file_exists(file_path: str) -> Dict[str, bool]:
    """
    Check if a file exists in Backblaze B2
    Args:
        file_path: Full path of file (e.g., 'us_options_opra/trades_v1/2024/03/2024-03-19.csv.gz')
    Returns:
        Dict[str, bool]: Dictionary indicating if file exists
    """
    try:
        exists = b2.file_exists(file_path)
        return {"exists": exists}
    except Exception as e:
        logger.error(f"Failed to check B2 file existence: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/backblaze/upload")
async def upload_to_backblaze(file_path: str) -> Dict[str, str]:
    """
    Upload a file to Backblaze B2
    Args:
        file_path: Full path of file (e.g., 'us_options_opra/trades_v1/2024/03/2024-03-19.csv.gz')
    Returns:
        Dict[str, str]: Dictionary containing the uploaded file path
    """
    try:
        uploaded_path = b2.upload_file(file_path)
        return {"uploaded_to": uploaded_path}
    except Exception as e:
        logger.error(f"Failed to upload to B2: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transfer")
async def transfer_file(file_path: str = Query(..., description="Full path of file to transfer")) -> Dict[str, str]:
    """
    Download from Polygon and upload to Backblaze in one operation
    Args:
        file_path: Full path of file (e.g., 'us_options_opra/trades_v1/2024/03/2024-03-19.csv.gz')
    Returns:
        Dict[str, str]: Dictionary containing source and destination paths (same path)
    """
    logger.info(f"Starting transfer for {file_path}")
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_path = os.path.join(temp_dir, os.path.basename(file_path))
    
    try:
        # Download from Polygon to temp directory
        downloaded_path = polygon.download_file(file_path, temp_path)
        logger.debug(f"Successfully downloaded to {downloaded_path}")
        
        # Upload from temp directory to Backblaze
        uploaded_path = b2.upload_file(downloaded_path, file_path)
        logger.debug(f"Successfully uploaded to {uploaded_path}")
        
        # Clean up
        if os.path.exists(downloaded_path):
            os.remove(downloaded_path)
            logger.debug(f"Cleaned up temp file: {downloaded_path}")
            
        return {
            "downloaded_from": file_path,
            "uploaded_to": file_path
        }
    except Exception as e:
        logger.error(f"Transfer failed: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
            logger.debug(f"Cleaned up temp file after error: {temp_path}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)