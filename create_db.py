import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Connect as postgres user to default postgres db
    # Host is empty string to imply unix domain socket
    # User is postgres, password none (peer auth if running as postgres user)
    conn = psycopg2.connect(dbname='postgres', user='postgres', host='/var/run/postgresql')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Check if DB exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'hrd_db'")
    if not cursor.fetchone():
        print("Creating hrd_db...")
        cursor.execute("CREATE DATABASE hrd_db;")
    else:
        print("hrd_db already exists.")
        
    # Create user if not exists
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname = 'hrd_user'")
    if not cursor.fetchone():
        print("Creating hrd_user...")
        cursor.execute("CREATE USER hrd_user WITH PASSWORD 'HRD_SuperSecure_2024!';")
    else:
        print("hrd_user already exists.")
        cursor.execute("ALTER USER hrd_user WITH PASSWORD 'HRD_SuperSecure_2024!';")

    # Grant privileges
    print("Granting privileges...")
    cursor.execute("GRANT ALL PRIVILEGES ON DATABASE hrd_db TO hrd_user;")
    # Also need to grant on schema public in the new DB? 
    # Usually easier to just make user owner or superuser for simplicity in this context?
    # No, stick to least privilege but make sure it works.
    
    cursor.close()
    conn.close()
    
    # Connect to hrd_db to grant schema usage
    conn = psycopg2.connect(dbname='hrd_db', user='postgres', host='/var/run/postgresql')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("GRANT ALL ON SCHEMA public TO hrd_user;")
    cursor.close()
    conn.close()

    print("Success provided.")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
