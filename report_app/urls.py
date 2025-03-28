from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate_report, name='generate_report'),
    path('generate-json/', views.generate_report_json, name='generate_report_json'),
    path('view/', views.view_report, name='view_report'),
    path('download/', views.download_pdf, name='download_pdf'),
]
