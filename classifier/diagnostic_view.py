"""
DIAGNOSTIC SCRIPT FOR RENDER DEPLOYMENT
Add this to your Django views to see what's happening on Render
"""

from django.http import HttpResponse
from django.conf import settings
import pathlib
import os


def render_diagnostic(request):
    """Diagnostic view to check Render environment"""
    
    output = []
    output.append("=" * 70)
    output.append("RENDER DEPLOYMENT DIAGNOSTIC")
    output.append("=" * 70)
    
    # Check BASE_DIR
    output.append(f"\n1. BASE_DIR: {settings.BASE_DIR}")
    
    # Check models directory
    models_dir = pathlib.Path(settings.BASE_DIR) / 'models'
    output.append(f"\n2. Models Directory: {models_dir}")
    output.append(f"   - Exists: {models_dir.exists()}")
    
    if models_dir.exists():
        output.append(f"\n3. Files in models directory:")
        for f in models_dir.iterdir():
            size_mb = f.stat().st_size / (1024 * 1024) if f.is_file() else 0
            output.append(f"   - {f.name}: {size_mb:.2f} MB")
    else:
        output.append(f"\n3. ❌ Models directory does NOT exist!")
        
    # Test model loading
    output.append(f"\n4. Testing Model Loading:")
    
    try:
        from ai_model.model_loader import model_loader
        output.append("   ✓ model_loader imported")
        
        # Try to load model
        model = model_loader.get_model()
        
        if model is None:
            output.append("   ❌ Model is None after loading!")
        else:
            output.append(f"   ✅ Model loaded: {type(model)}")
            
        # Try to load labels  
        labels = model_loader.get_class_labels()
        if labels:
            output.append(f"   ✅ Labels loaded: {len(labels)} labels")
        else:
            output.append(f"   ❌ No labels loaded!")
            
    except Exception as e:
        output.append(f"   ❌ ERROR: {str(e)}")
        import traceback
        output.append(f"\n   Traceback:\n{traceback.format_exc()}")
    
    # Check tflite_runtime
    output.append(f"\n5. Checking tflite_runtime:")
    try:
        import tflite_runtime
        output.append(f"   ✓ tflite_runtime version: {tflite_runtime.__version__}")
    except ImportError as e:
        output.append(f"   ❌ tflite_runtime not found: {e}")
    
    # Check tensorflow
    output.append(f"\n6. Checking tensorflow:")
    try:
        import tensorflow as tf
        output.append(f"   ✓ tensorflow version: {tf.__version__}")
    except ImportError as e:
        output.append(f"   ❌ tensorflow not found: {e}")
    
    # Environment variables
    output.append(f"\n7. Environment Variables:")
    for key in ['TF_CPP_MIN_LOG_LEVEL', 'PYTHON_VERSION', 'PORT', 'RENDER']:
        value = os.environ.get(key, 'NOT SET')
        output.append(f"   - {key}: {value}")
    
    output.append("\n" + "=" * 70)
    
    return HttpResponse("<pre>" + "\n".join(output) + "</pre>", content_type="text/html")
