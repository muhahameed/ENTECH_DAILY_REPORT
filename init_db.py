import os
import django
import time
import psycopg2
import socket

# Check if we're running in Docker or locally
def is_docker_host_available():
    try:
        # Try to resolve the Docker host name
        socket.gethostbyname('db')
        return True
    except socket.gaierror:
        return False

# Set the appropriate host based on environment
db_host = 'db' if is_docker_host_available() else '127.0.0.1'
print(f"Using database host: {db_host}")

# Wait for PostgreSQL to be ready
max_retries = 10
retry_count = 0
while retry_count < max_retries:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'entech_db'),
            user=os.environ.get('POSTGRES_USER', 'postgres'),
            password=os.environ.get('POSTGRES_PASSWORD', 'postgres'),
            host=os.environ.get('POSTGRES_HOST', db_host),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        conn.close()
        print("PostgreSQL is ready!")
        break
    except psycopg2.OperationalError as e:
        retry_count += 1
        print(f"PostgreSQL not ready yet (attempt {retry_count}/{max_retries}). Error: {e}")
        print("Waiting 5 seconds before retry...")
        time.sleep(5)

if retry_count == max_retries:
    print("Could not connect to PostgreSQL. Exiting.")
    exit(1)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entech_project.settings')

# Update Django's database settings to use the correct host
os.environ['POSTGRES_HOST'] = db_host

django.setup()

# Run migrations
from django.core.management import call_command
call_command('migrate')
print("Migrations applied successfully!")
