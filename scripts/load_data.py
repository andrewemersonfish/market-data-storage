import psycopg2
import gzip
import csv
import glob
import os

# Database connection settings
DB_NAME = "options_flow"
DB_USER = "andrewfish"
DB_HOST = "localhost"
DB_PORT = "5432"

def create_tables(cursor):
    """Create the tables if they don't exist"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            ticker TEXT,
            conditions FLOAT,
            correction INTEGER,
            exchange INTEGER,
            price FLOAT,
            sip_timestamp BIGINT,
            size INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS minute_aggs (
            ticker TEXT,
            volume INTEGER,
            open FLOAT,
            close FLOAT,
            high FLOAT,
            low FLOAT,
            window_start BIGINT,
            transactions INTEGER
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS day_aggs (
            ticker TEXT,
            volume INTEGER,
            open FLOAT,
            close FLOAT,
            high FLOAT,
            low FLOAT,
            window_start BIGINT,
            transactions INTEGER
        )
    """)

def load_gz_file(cursor, file_path, table_name):
    """Load a gzipped CSV file directly into PostgreSQL"""
    with gzip.open(file_path, 'rt') as f:
        # Read and skip header
        header = next(csv.reader([f.readline()]))
        columns = ','.join(header)
        
        # Use COPY command for fast loading
        cursor.copy_expert(f"""
            COPY {table_name} ({columns})
            FROM STDIN WITH (FORMAT CSV)
        """, f)

def main():
    # Connect to database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = False
    cursor = conn.cursor()

    try:
        # Create tables
        create_tables(cursor)
        conn.commit()
        
        # Process each data type
        data_types = {
            'trades': 'data/downloads/trades/*.csv.gz',
            'minute_aggs': 'data/downloads/minute_aggs/*.csv.gz',
            'day_aggs': 'data/downloads/day_aggs/*.csv.gz'
        }
        
        for table_name, glob_pattern in data_types.items():
            files = glob.glob(glob_pattern)
            total_files = len(files)
            print(f"\nProcessing {table_name}: {total_files} files")
            
            for idx, file_path in enumerate(files, 1):
                try:
                    print(f"Loading {table_name} file {idx}/{total_files}: {os.path.basename(file_path)}")
                    load_gz_file(cursor, file_path, table_name)
                    conn.commit()  # Commit after each file
                    
                    # Print progress after each file
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"Current {table_name} count: {count:,} rows")
                    
                except Exception as e:
                    print(f"Error loading {file_path}: {str(e)}")
                    conn.rollback()
            
            # Print final count for this table
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"\nFinished {table_name}: {count:,} total rows")

    except Exception as e:
        print(f"Error: {str(e)}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()