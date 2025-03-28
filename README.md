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

### Option 1: Using Docker (Recommended)

Docker provides the easiest setup experience by handling all dependencies automatically.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/ENTECH_DAILY_REPORT.git
   cd ENTECH_DAILY_REPORT
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```
5. Access the application at http://localhost:8000

### Using Docker

1. Build the Docker image:
   ```
   docker build -t entech-report-generator .
   ```
2. Run the container:
   ```
   docker run -p 8000:8000 -e POSTGRES_HOST=localhost -e POSTGRES_DB=entech_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_PORT=5432 entech-report-generator
   ```
3. Access the application at http://localhost:8000

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
- `entech_project/` - Django project settings
- `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
- `Dockerfile` - Docker configuration
- `requirements.txt` - Python dependencies
