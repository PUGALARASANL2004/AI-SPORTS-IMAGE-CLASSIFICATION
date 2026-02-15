from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from .forms import ImageUploadForm
from .models import UploadedImage
from ai_model.predictor import predictor
from ai_model.model_loader import model_loader
import os
from django.conf import settings


import base64
from io import BytesIO

def upload_image(request):
    """View for handling image uploads and predictions in-memory."""
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Get the uploaded file from memory
                image_file = request.FILES['image']
                
                # Manual garbage collection to free up RAM
                import gc
                gc.collect()
                
                # Make prediction directly using the file-like object
                # PIL.Image.open (used in our preprocessing) handles this perfectly
                predicted_class, confidence_score = predictor.predict_top(image_file)
                
                # Convert image to Base64 so we can display it without saving to disk
                image_file.seek(0)
                image_bytes = image_file.read()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                mime_type = image_file.content_type
                
                context = {
                    'predicted_class': predicted_class,
                    'confidence': confidence_score,
                    'confidence_percentage': round(confidence_score * 100, 2),
                    'base64_image': f"data:{mime_type};base64,{base64_image}",
                }
                
                # Render result directly (No redirect/DB save)
                return render(request, 'classifier/result.html', context)
            
            except Exception as e:
                import traceback
                print(f"CRITICAL ERROR: {str(e)}")
                print(traceback.format_exc())
                messages.error(request, f'Processing error: {str(e)}')
                return redirect('upload')
    else:
        form = ImageUploadForm()
    
    return render(request, 'classifier/upload.html', {'form': form})


# Removed result_view because results are now rendered directly to prevent storage issues.


def dashboard(request):
    """View for the Analytics Dashboard."""
    
    # Total Uploads
    total_images = UploadedImage.objects.count()
    
    # Average Confidence
    avg_confidence = UploadedImage.objects.aggregate(Avg('confidence_score'))['confidence_score__avg'] or 0
    avg_confidence = round(avg_confidence * 100, 1)
    
    # Most Popular Sports (Top 5)
    top_sports = UploadedImage.objects.values('predicted_class').annotate(count=Count('predicted_class')).order_by('-count')[:5]
    
    # Prepare data for Chart.js
    labels = [item['predicted_class'] for item in top_sports if item['predicted_class']]
    data = [item['count'] for item in top_sports if item['predicted_class']]
    
    # Recent Uploads
    recent_uploads = UploadedImage.objects.all()[:10]
    
    context = {
        'total_images': total_images,
        'avg_confidence': avg_confidence,
        'chart_labels': labels,
        'chart_data': data,
        'recent_uploads': recent_uploads
    }
    
    return render(request, 'classifier/dashboard.html', context)


def home(request):
    """Home page view (redirects to upload)."""
    return redirect('upload')


def health_check(request):
    """Simple health check endpoint for Render."""
    from django.http import HttpResponse
    return HttpResponse("OK", status=200)
