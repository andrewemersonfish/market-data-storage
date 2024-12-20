import asyncio
import httpx
from datetime import datetime, timedelta

# Configuration
START_DATE = "2024-01-06"  # YYYY-MM-DD
END_DATE = "2024-01-09"    # YYYY-MM-DD
BASE_PREFIX = "us_options_opra/trades_v1"
API_URL = "http://localhost:8000"

async def get_files_for_date(client: httpx.AsyncClient, date_str: str) -> list[str]:
    """Get all trade files for a specific date"""
    prefix = f"{BASE_PREFIX}/{date_str[:4]}/{date_str[5:7]}/{date_str}"
    try:
        response = await client.get(
            f"{API_URL}/polygon/files",
            params={"prefix": prefix}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"✗ Error listing files for {date_str}: {str(e)}")
        return []

async def check_file_exists(client: httpx.AsyncClient, file_path: str) -> bool:
    """Check if file already exists in Backblaze"""
    try:
        response = await client.get(
            f"{API_URL}/backblaze/check",
            params={"file_path": file_path}
        )
        response.raise_for_status()
        return response.json()["exists"]
    except Exception as e:
        print(f"✗ Error checking file existence: {str(e)}")
        return False

async def transfer_file(client: httpx.AsyncClient, file_path: str):
    """Transfer a single file"""
    try:
        # Check if file already exists
        if await check_file_exists(client, file_path):
            print(f"⏭ Skipping (already exists): {file_path}")
            return

        response = await client.post(
            f"{API_URL}/transfer",
            params={"file_path": file_path}
        )
        response.raise_for_status()
        print(f"✓ Transferred: {file_path}")
    except httpx.HTTPStatusError as e:
        print(f"✗ Failed to transfer {file_path}: HTTP {e.response.status_code}")
        print(f"  Error details: {e.response.text}")
    except Exception as e:
        print(f"✗ Error transferring {file_path}: {str(e)}")

async def main():
    # Convert dates to datetime objects
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")
    end_date = datetime.strptime(END_DATE, "%Y-%m-%d")
    
    print(f"Starting transfer of trade data from {START_DATE} to {END_DATE}")
    
    async with httpx.AsyncClient(timeout=300.0) as client:
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            print(f"\nProcessing date: {date_str}")
            
            # Get files for current date
            files = await get_files_for_date(client, date_str)
            if not files:
                print(f"No files found for {date_str}")
                current_date += timedelta(days=1)
                continue
                
            print(f"Found {len(files)} files")
            
            # Process files sequentially
            for file_path in files:
                await transfer_file(client, file_path)
            
            current_date += timedelta(days=1)

if __name__ == "__main__":
    asyncio.run(main())