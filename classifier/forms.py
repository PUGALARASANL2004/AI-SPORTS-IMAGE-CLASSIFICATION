from django import forms
from .models import UploadedImage


class ImageUploadForm(forms.ModelForm):
    """Form for uploading images with validation."""
    
    class Meta:
        model = UploadedImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/jpeg,image/jpg,image/png',
                'id': 'imageInput'
            })
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Validate file size (max 10MB)
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be less than 10MB.')
            
            # Validate file extension
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError('Only JPG, JPEG, and PNG images are allowed.')
        
        return image
