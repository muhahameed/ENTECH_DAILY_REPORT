from django.contrib import admin
from .models import Report, Picture

class PictureInline(admin.TabularInline):
    model = Picture
    extra = 1

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('daily_report_no', 'date', 'page', 'created_at')
    inlines = [PictureInline]

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('description', 'location', 'report')
    list_filter = ('report',)
