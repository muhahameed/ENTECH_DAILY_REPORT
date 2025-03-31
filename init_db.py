import os
import django
import psycopg2

# Set fixed database connection parameters
db_name = 'entech_db'
db_user = 'postgres'
db_password = 'postgres'
db_host = '127.0.0.1'  # localhost
db_port = '5432'

# Simple connection check
print("Connecting to PostgreSQL database...")
try:
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.close()
    print("PostgreSQL connection successful!")
except psycopg2.OperationalError as e:
    print(f"Could not connect to PostgreSQL. Error: {e}")
    print("Please make sure PostgreSQL is running on localhost:5432")
    exit(1)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entech_project.settings')

# Set database environment variables
os.environ['POSTGRES_DB'] = db_name
os.environ['POSTGRES_USER'] = db_user
os.environ['POSTGRES_PASSWORD'] = db_password
os.environ['POSTGRES_HOST'] = db_host
os.environ['POSTGRES_PORT'] = db_port

django.setup()

# Run migrations
from django.core.management import call_command
call_command('migrate')
print("Migrations applied successfully!")
