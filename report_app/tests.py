from django.test import TestCase, Client
from django.urls import reverse
import json
import os
from django.conf import settings
from .models import Report, Picture

class ReportModelTests(TestCase):
    def test_report_creation(self):
        report = Report.objects.create(
            date='2024-10-29',
            daily_report_no='123',
            page='3 of 4'
        )
        self.assertEqual(report.daily_report_no, '123')
        self.assertEqual(str(report), 'Report #123 - 2024-10-29')

class PictureModelTests(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            date='2024-10-29',
            daily_report_no='123',
            page='3 of 4'
        )
    
    def test_picture_creation(self):
        picture = Picture.objects.create(
            report=self.report,
            file_name='/images/Picture1.jpg',
            location='Staten Island, New York',
            description='Before the painting'
        )
        self.assertEqual(picture.location, 'Staten Island, New York')
        self.assertEqual(str(picture), 'Before the painting at Staten Island, New York')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Ensure the input.json file is accessible for testing
        self.json_path = os.path.join(settings.BASE_DIR, 'input.json')
        self.assertTrue(os.path.exists(self.json_path), 'Test JSON file not found')
    
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_app/index.html')
    
    def test_generate_report_view(self):
        response = self.client.get(reverse('generate_report'))
        self.assertEqual(response.status_code, 302)  # Redirect after generation
        
        # Verify data was saved to database
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.daily_report_no, '123')
        
        # Verify pictures were created
        self.assertEqual(Picture.objects.count(), 4)
    
    def test_view_report_view(self):
        # First generate a report
        self.client.get(reverse('generate_report'))
        
        # Then view it
        response = self.client.get(reverse('view_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report_app/report.html')
        
        # Check context data
        self.assertIn('report', response.context)
        self.assertIn('pictures', response.context)
        self.assertEqual(len(response.context['pictures']), 4)
    
    def test_download_pdf_view(self):
        # First generate a report
        self.client.get(reverse('generate_report'))
        
        # Then download PDF
        response = self.client.get(reverse('download_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue('attachment; filename="report_123.pdf"' in response['Content-Disposition'])
