# scripts/test_transfer.py

import asyncio
import httpx
import time
from datetime import datetime

async def main():
    async with httpx.AsyncClient(timeout=300.0) as client:  # 5 minute timeout
        # Get list of files for just one day
        today = datetime.now().strftime("%Y/%m/%d")
        prefix = f"us_options_opra/trades_v1/{today}"
        
        print(f"Listing files for {prefix}...")
        response = await client.get(
            "http://localhost:8000/polygon/files",
            params={"prefix": prefix}
        )
        files = response.json()
        print(f"Found {len(files)} files")

        # Try to transfer first 3 files
        for file_path in files[:3]:
            print(f"\nStarting transfer: {file_path}")
            start_time = time.time()
            
            try:
                response = await client.post(
                    "http://localhost:8000/transfer",
                    params={"file_path": file_path}
                )
                
                if response.status_code == 200:
                    elapsed = time.time() - start_time
                    print(f"Success: {response.json()}")
                    print(f"Transfer took {elapsed:.1f} seconds")
                else:
                    print(f"Failed with status {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"Failed: {str(e)}")
            
            # Add a small delay between transfers
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())