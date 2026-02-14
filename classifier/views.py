from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from .forms import ImageUploadForm
from .models import UploadedImage
from ai_model.predictor import predictor
from ai_model.model_loader import model_loader
import os
from django.conf import settings


def upload_image(request):
    """View for handling image uploads, predictions, and Grad-CAM."""
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Save the uploaded image
                uploaded_image = form.save()
                
                # Get the image file path
                image_path = uploaded_image.image.path
                
                # Make prediction
                predicted_class, confidence_score = predictor.predict_top(image_path)
                
                # Update the model with prediction results
                uploaded_image.predicted_class = predicted_class
                uploaded_image.confidence_score = confidence_score
                
                uploaded_image.save()
                
                uploaded_image.save()
                
                # Redirect to result page
                return redirect('result', pk=uploaded_image.pk)
            
            except Exception as e:
                import traceback
                error_traceback = traceback.format_exc()
                print(f"CRITICAL ERROR DURING PREDICTION: {str(e)}")
                print(error_traceback)
                messages.error(request, f'Internal processing error: {str(e)}')
                # If we are in DEBUG mode, re-raise to see the Django error page
                if settings.DEBUG:
                    raise e
                return redirect('upload')
    else:
        form = ImageUploadForm()
    
    return render(request, 'classifier/upload.html', {'form': form})


def result_view(request, pk):
    """View for displaying prediction results."""
    
    uploaded_image = get_object_or_404(UploadedImage, pk=pk)
    
    context = {
        'image': uploaded_image,
        'predicted_class': uploaded_image.predicted_class,
        'confidence': uploaded_image.confidence_score,
        'confidence_percentage': round(uploaded_image.confidence_score * 100, 2) if uploaded_image.confidence_score else 0
    }
    
    return render(request, 'classifier/result.html', context)


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
