![image](https://github.com/user-attachments/assets/c34d243d-a646-40af-a1dc-2a059feb8e7a)


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
   docker run -p 8000:8000 -e POSTGRES_HOST=127.0.0.1 -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_PORT=5432 entech-report-generator
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
    - `report_app/images/` - Directory for storing images used in reports
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

## Using Images in Reports

The ENTECH Daily Inspection Report Generator allows you to include site documentation images in your reports. Follow these instructions to add images to your reports:

### Adding Images to the Application

1. **Image Location**: Place all your images in the `report_app/static/report_app/images/` directory.

2. **Supported Image Formats**: The application supports common image formats including:
   - JPEG (.jpg, .jpeg)
   - PNG (.png)
   - GIF (.gif)

3. **Image Naming**: Use descriptive filenames without spaces (use underscores or hyphens instead). For example:
   - `site_entrance.jpg`
   - `before_painting.jpg`
   - `after_repairs.png`

### Referencing Images in input.json

To include images in your report, reference them in the `input.json` file using the following format:

```json
{
  "date": "2024-10-29",
  "daily_report_no": "123",
  "page": "3 of 4",
  "pictures": [
    {
      "file_name": "Picture1.jpg",
      "location": "Staten Island, New York",
      "description": "Before the painting"
    },
    {
      "file_name": "Picture2.jpg",
      "location": "Staten Island, New York",
      "description": "After the painting"
    }
  ]
}
```

### Important Notes About Images

1. **File Name**: The `file_name` field should contain only the filename (e.g., `Picture1.jpg`), not the full path.

2. **Image Processing**: The application automatically resizes images to fit properly in the PDF report (800x600 pixels).

3. **Image Metadata**: Each image requires:
   - `file_name`: The name of the image file in the images directory
   - `location`: Where the picture was taken
   - `description`: A brief description of what the image shows

4. **Adding Multiple Images**: You can add as many images as needed by adding more objects to the `pictures` array in the JSON.

### Using the Web Interface

When using the web interface:

1. Place your images in the `report_app/static/report_app/images/` directory
2. Update the JSON in the text area on the home page to reference your images
3. Click "Generate Report" to create a report with your images

The application will automatically find the referenced images, resize them as needed, and include them in the generated PDF report.

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors like the following:

```
psycopg2.OperationalError: connection to server at "127.0.0.1", port 5432 failed: Connection refused
        Is the server running on that host and accepting TCP/IP connections?
```

This typically happens due to incorrect database connection settings. Here are some solutions:

#### When Using Docker Standalone

When running the application container separately from the database container, you need to ensure proper network connectivity:

1. **Network Configuration**: Make sure both containers are on the same Docker network:
   ```bash
   # Create a network
   docker network create entech-network
   
   # Run PostgreSQL with the network
   docker run --name postgres-db --network entech-network -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:14
   
   # Run the application with the network and correct host
   docker run --network entech-network -p 8000:8000 -e POSTGRES_HOST=postgres-db -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_PORT=5432 entech-report-generator
   ```

2. **Host Configuration**: When running containers separately, use the container name as the host, not 127.0.0.1:
   - Incorrect: `-e POSTGRES_HOST=127.0.0.1`
   - Correct: `-e POSTGRES_HOST=postgres-db`

#### When Using Docker Compose

With Docker Compose, the service name defined in `docker-compose.yml` should be used as the host:

1. **Check Environment Variables**: In the `docker-compose.yml` file, ensure the web service has:
   ```yaml
   environment:
     - POSTGRES_HOST=db  # 'db' is the service name of the database
   ```

2. **Verify Dependencies**: Make sure the web service depends on the database service:
   ```yaml
   depends_on:
     db:
       condition: service_healthy
   ```

#### When Running Locally

If running the application outside of Docker:

1. **Ensure PostgreSQL is Running**: Check if PostgreSQL is running on your machine:
   ```bash
   # Windows
   sc query postgresql
   
   # Or check if port 5432 is listening
   netstat -an | findstr 5432
   ```

2. **Correct Environment Variables**: Set the correct environment variables:
   ```bash
   set POSTGRES_HOST=localhost
   # or
   set POSTGRES_HOST=127.0.0.1
   ```

3. **PostgreSQL Configuration**: Ensure PostgreSQL is configured to accept connections:
   - Check `pg_hba.conf` for proper client authentication settings
   - Verify PostgreSQL is listening on the correct interfaces in `postgresql.conf`

