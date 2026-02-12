import uuid
from django.db import models
from django.utils import timezone


class UploadedImage(models.Model):
    """Model to store uploaded images and their predictions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    predicted_class = models.CharField(max_length=100, blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.predicted_class or 'Pending'} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
