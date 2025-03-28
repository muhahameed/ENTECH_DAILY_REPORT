from django.db import models
import json

class Report(models.Model):
    date = models.DateField()
    daily_report_no = models.CharField(max_length=50)
    page = models.CharField(max_length=20)
    json_content = models.TextField(null=True, blank=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report #{self.daily_report_no} - {self.date}"

class Picture(models.Model):
    report = models.ForeignKey(Report, related_name='pictures', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.file_name} - {self.location}"

class ReportPDF(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='pdf')
    pdf_file = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"PDF for Report #{self.report.daily_report_no}"
