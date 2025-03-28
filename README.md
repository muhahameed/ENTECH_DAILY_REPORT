# ENTECH Daily Inspection Report Generator

A professional web application for generating daily inspection reports with image documentation for engineering projects. This application uses Django with PostgreSQL for data storage and WeasyPrint for PDF generation.

## Features

- Generate professional PDF reports from JSON data
- Include site documentation with images and descriptions
- Store report data in PostgreSQL database
- Save generated PDF files for future reference
- Customizable report formatting with modern styling
- Easy-to-use web interface
- Containerized with Docker for easy deployment

## Comprehensive Installation Guide

### Prerequisites

- Git
- Python 3.9+
- Docker and Docker Compose (recommended)
- PostgreSQL (if not using Docker)
- WeasyPrint dependencies (if not using Docker)

### Option 1: Local Setup

This option is for setting up the application locally without Docker.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muhahameed/ENTECH_DAILY_REPORT.git
   cd ENTECH_DAILY_REPORT
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database:
   ```bash
   # Ensure PostgreSQL is running locally
   # Set environment variables if needed (defaults shown)
   # Windows
   set POSTGRES_DB=entech_db
   set POSTGRES_USER=postgres
   set POSTGRES_PASSWORD=postgres
   set POSTGRES_HOST=127.0.0.1
   set POSTGRES_PORT=5432
   
   # Run the database initialization script
   python init_db.py
   ```
   
   Alternatively, you can run migrations manually:
   ```bash
   python manage.py migrate
   ```
4. Start the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the application at http://localhost:8000

### Option 2: Using Docker

1. Pull the PostgreSQL image:
   ```bash
   docker pull postgres:14
   ```

2. Run the PostgreSQL container:
   ```bash
   docker run --name postgres-db -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14
   ```

3. Build the application Docker image:
   ```bash
   docker build -t entech-report-generator .
   ```

4. Run the application container:
   ```bash
   docker run -p 8000:8000 -e POSTGRES_HOST=host.docker.internal -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_PORT=5432 entech-report-generator
   ```

5. Access the application at http://localhost:8000

### Option 3: Using Docker Compose (Recommended for Development)

Docker Compose provides the easiest way to set up both the web application and PostgreSQL database together. The configuration uses PostgreSQL 14 and automatically handles migrations.

1. **Start the application stack**:
   ```bash
   docker-compose up
   ```
   This command builds the images if they don't exist and starts the containers in the foreground with logs visible.

2. **Start the application in detached mode** (run in background):
   ```bash
   docker-compose up -d
   ```

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

4. **Stop the application and remove volumes** (will delete database data):
   ```bash
   docker-compose down -v
   ```

5. **View logs of running containers**:
   ```bash
   docker-compose logs
   ```
   To follow logs in real-time:
   ```bash
   docker-compose logs -f
   ```

6. **Rebuild the application after code changes**:
   ```bash
   docker-compose build
   docker-compose up
   ```

7. **Execute commands in the running container**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

8. **Access the application** at http://localhost:8000

## Database Initialization

The application includes an `init_db.py` script that handles PostgreSQL database initialization. This script automatically:

- Detects whether you're running in Docker or locally
- Waits for the PostgreSQL server to be ready
- Sets up the appropriate database connection
- Applies Django migrations

### Option 1: Using the Initialization Script

1. Ensure PostgreSQL is running (either locally or via Docker)

2. Set environment variables (optional, defaults shown):
   ```bash
   # Windows
   set POSTGRES_DB=entech_db
   set POSTGRES_USER=postgres
   set POSTGRES_PASSWORD=postgres
   set POSTGRES_HOST=127.0.0.1
   set POSTGRES_PORT=5432
   
   # Linux/macOS
   export POSTGRES_DB=entech_db
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export POSTGRES_HOST=127.0.0.1
   export POSTGRES_PORT=5432
   ```

3. Run the initialization script:
   ```bash
   python init_db.py
   ```

### Option 2: Manual Database Setup

1. Create a PostgreSQL database:
   ```bash
   createdb entech_db
   # Or using psql
   psql -U postgres -c "CREATE DATABASE entech_db;"
   ```

2. Apply migrations manually:
   ```bash
   python manage.py migrate
   ```

## Running Tests

To run the test suite:

```
python manage.py test
```

## Project Structure

- `report_app/` - Django application for report generation
  - `models.py` - Database models for report data
  - `views.py` - Views for processing JSON and rendering templates
  - `templates/` - HTML templates for the application
  - `tests.py` - Unit tests
  - `management/` - Custom management commands
  - `migrations/` - Database migrations
  - `static/` - Static files specific to the report app
  - `urls.py` - URL routing for the report app
  - `admin.py` - Admin interface configuration
- `entech_project/` - Django project settings
  - `settings.py` - Project configuration settings
  - `urls.py` - Main URL routing
  - `wsgi.py` and `asgi.py` - Web server interfaces
- `media/` - User-uploaded files
  - `reports/` - Generated report files
- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `requirements.txt` - Python dependencies
- `init_db.py` - Database initialization script
- `manage.py` - Django management script
- `input.json` - Sample input data

