import json
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import get_template, render_to_string
from .models import Report, Picture, ReportPDF
from weasyprint import HTML
from PIL import Image
from datetime import datetime  # Add this import
from django.template.loader import render_to_string
import tempfile
from django.core.files.base import ContentFile

def index(request):
    """Home page view with button to generate report"""
    return render(request, 'report_app/index.html')

def generate_report(request):
    """Generate report from JSON data and save to database"""
    # Clear existing data (for demo purposes)
    Report.objects.all().delete()
    
    # Read JSON data
    json_path = os.path.join(settings.BASE_DIR, 'input.json')
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    # Create report
    report = Report.objects.create(
        date=data['date'],
        daily_report_no=data['daily_report_no'],
        page=data['page']
    )
    
    # Create pictures and resize them
    for pic_data in data['pictures']:
        file_name = pic_data['file_name']
        if file_name.startswith('/'):
            file_name = file_name[1:]
        
        image_path = os.path.join(settings.BASE_DIR, 'report_app', 'static', 'report_app', 'images', file_name)
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Adjusted size for A4 page (approximately 700px height to ensure fit)
                fixed_size = (800, 600)  # Reduced height to fit A4 page with text
                resized_img = img.resize(fixed_size, Image.Resampling.LANCZOS)
                
                new_filename = f"resized_{os.path.splitext(file_name)[0]}_{fixed_size[0]}x{fixed_size[1]}.jpg"
                new_path = os.path.join(os.path.dirname(image_path), new_filename)
                resized_img.save(new_path, 'JPEG', quality=100, optimize=True)
                file_name = new_filename
        
        Picture.objects.create(
            report=report,
            file_name=file_name,
            location=pic_data['location'],
            description=pic_data['description']
        )
    
    return redirect('view_report')

def view_report(request):
    """View the generated report"""
    try:
        report = Report.objects.latest('created_at')
        pictures = report.pictures.all()
        
        context = {
            'report': report,
            'pictures': pictures,
            # Remove the replace operation since we're now storing the correct path format
            'base_url': request.build_absolute_uri('/').rstrip('/')
        }
        
        return render(request, 'report_app/report.html', context)
    except Report.DoesNotExist:
        return redirect('index')

def download_pdf(request):
    """Generate and download PDF report"""
    try:
        report = Report.objects.latest('created_at')
        
        # Check if we have JSON content
        if hasattr(report, 'json_content') and report.json_content:
            # Use JSON content if available
            data = json.loads(report.json_content)
            context = {
                'report': data,
                'pictures': data.get('pictures', [])
            }
            template_string = render_to_string('report_app/report.html', context)
        else:
            # Use the old method with pictures from the database
            pictures = report.pictures.all()
            context = {
                'report': report,
                'pictures': pictures,
                'static_url': settings.STATIC_URL,
                'base_url': request.build_absolute_uri('/')
            }
            template = get_template('report_app/report.html')
            template_string = template.render(context)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{report.daily_report_no}.pdf"'
        
        # Convert HTML to PDF using WeasyPrint with proper base URL
        html = HTML(string=template_string, base_url=request.build_absolute_uri('/'))
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            html.write_pdf(target=tmp.name)
            tmp_file_path = tmp.name
        
        # Read the PDF file
        with open(tmp_file_path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        
        # Save PDF to database - check if report already has a PDF
        try:
            if hasattr(report, 'pdf'):
                # Update existing PDF
                report.pdf.pdf_file.delete(save=False)  # Delete old file
                report.pdf.pdf_file.save(f"report_{report.daily_report_no}_{report.date}.pdf", ContentFile(pdf_content))
            else:
                # Create new PDF record
                report_pdf = ReportPDF(report=report)
                report_pdf.pdf_file.save(f"report_{report.daily_report_no}_{report.date}.pdf", ContentFile(pdf_content))
        except Exception as e:
            print(f"Error saving PDF: {e}")
        
        # Clean up the temporary file
        os.unlink(tmp_file_path)
        
        # Write PDF to response
        response.write(pdf_content)
        
        return response
    
    except Report.DoesNotExist:
        return redirect('index')


def generate_report_json(request):
    """Generate report from JSON data submitted via form"""
    if request.method == 'POST':
        try:
            json_data = request.POST.get('json_data')
            data = json.loads(json_data)
            
            # Save report to database
            report_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            report = Report(
                date=report_date,
                daily_report_no=data['daily_report_no'],
                page=data['page'],
                json_content=json_data
            )
            report.save()
            
            # Pass to template
            context = {
                'report': data,
                'pictures': data.get('pictures', [])
            }
            
            return render(request, 'report_app/report.html', context)
        except json.JSONDecodeError:
            # Handle invalid JSON
            return render(request, 'report_app/index.html', {'error': 'Invalid JSON format'})
    
    return render(request, 'report_app/index.html')
