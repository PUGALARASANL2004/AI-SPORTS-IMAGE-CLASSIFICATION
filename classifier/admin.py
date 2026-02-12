from django.contrib import admin
from .models import UploadedImage


@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    """Admin interface for uploaded images."""
    
    list_display = ['id', 'predicted_class', 'confidence_score', 'uploaded_at']
    list_filter = ['uploaded_at', 'predicted_class']
    search_fields = ['id', 'predicted_class']
    readonly_fields = ['id', 'uploaded_at']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('id', 'image', 'uploaded_at')
        }),
        ('Prediction Results', {
            'fields': ('predicted_class', 'confidence_score')
        }),
    )
