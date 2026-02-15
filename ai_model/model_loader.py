import os

# Set memory options before importing tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
from PIL import Image


class ModelLoader:
    """Singleton class to load and cache the AI model."""
    
    _instance = None
    _model = None
    _class_labels = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Do not load model in init to save memory during startup
        pass
    
    def load_model(self):
        """Load the model (TFLite or H5) with comprehensive error logging."""
        if self._model is not None:
            return

        from django.conf import settings
        import pathlib
        import traceback
        
        # Use absolute paths using Pathlib for better cross-platform support
        base_path = pathlib.Path(settings.BASE_DIR)
        models_dir = base_path / 'models'
        tflite_model_path = models_dir / 'sports_classifier.tflite'
        h5_model_path = models_dir / 'sports_classifier.h5'

        print("=" * 70)
        print("AI MODEL LOADING - DETAILED DEBUG")
        print("=" * 70)
        print(f"BASE_DIR: {settings.BASE_DIR}")
        print(f"Models Directory: {models_dir}")
        print(f"Models Directory Exists: {models_dir.exists()}")
        
        if models_dir.exists():
            print(f"\nFiles in models directory:")
            for f in models_dir.iterdir():
                size_mb = f.stat().st_size / (1024 * 1024) if f.is_file() else 0
                print(f"  - {f.name}: {size_mb:.2f} MB")
        else:
            print(f"❌ ERROR: Models directory DOES NOT EXIST!")
            self._model = None
            return

        # Strategy 1: Try tflite_runtime (Production/Render)
        print("\n" + "=" * 70)
        print("STRATEGY 1: TFLite via tflite_runtime")
        print("=" * 70)
        try:
            import tflite_runtime.interpreter as tflite
            print("✓ tflite_runtime successfully imported")
            
            if tflite_model_path.exists():
                file_size = tflite_model_path.stat().st_size / (1024*1024)
                print(f"✓ TFLite file found: {tflite_model_path}")
                print(f"✓ File size: {file_size:.2f} MB")
                
                try:
                    print("\n→ Step 1: Creating Interpreter...")
                    interpreter = tflite.Interpreter(model_path=str(tflite_model_path))
                    print("  ✓ Interpreter created successfully")
                    
                    print("\n→ Step 2: Allocating tensors...")
                    interpreter.allocate_tensors()
                    print("  ✓ Tensors allocated successfully")
                    
                    print("\n→ Step 3: Getting input/output details...")
                    input_details = interpreter.get_input_details()
                    output_details = interpreter.get_output_details()
                    print(f"  ✓ Input shape: {input_details[0]['shape']}")
                    print(f"  ✓ Output shape: {output_details[0]['shape']}")
                    
                    self._model = interpreter
                    print("\n" + "=" * 70)
                    print("✅ SUCCESS: TFLite model loaded via tflite_runtime!")
                    print("=" * 70)
                    return
                    
                except Exception as tflite_err:
                    print("\n" + "=" * 70)
                    print("❌ CRITICAL ERROR: TFLite loading FAILED!")
                    print("=" * 70)
                    print(f"Error Type: {type(tflite_err).__name__}")
                    print(f"Error Message: {str(tflite_err)}")
                    print(f"\nFull Traceback:")
                    print(traceback.format_exc())
                    print("=" * 70)
            else:
                print(f"⚠️ TFLite file NOT found at {tflite_model_path}")
                
        except ImportError as e:
            print(f"ℹ️ tflite_runtime not available: {e}")

        # Strategy 2: Try TensorFlow with TFLite (Fallback)
        print("\n" + "=" * 70)
        print("STRATEGY 2: TFLite via tensorflow")
        print("=" * 70)
        try:
            import tensorflow as tf
            print("✓ tensorflow successfully imported")
            
            if tflite_model_path.exists():
                print(f"→ Attempting TFLite via tensorflow from {tflite_model_path}")
                try:
                    interpreter = tf.lite.Interpreter(model_path=str(tflite_model_path))
                    interpreter.allocate_tensors()
                    self._model = interpreter
                    print("✅ SUCCESS: TFLite model loaded via tensorflow!")
                    return
                except Exception as tf_tflite_err:
                    print(f"⚠️ TFLite via TensorFlow failed: {tf_tflite_err}")
            
            # Strategy 3: Try H5 model
            if h5_model_path.exists():
                print(f"→ Attempting H5 model from {h5_model_path}")
                try:
                    self._model = tf.keras.models.load_model(str(h5_model_path), compile=False)
                    print("✅ SUCCESS: H5 model loaded!")
                    return
                except Exception as h5_err:
                    print(f"❌ H5 model loading failed: {h5_err}")
            else:
                print(f"ℹ️ H5 file not found (expected after removal)")
                
        except ImportError as e:
            print(f"ℹ️ tensorflow not available: {e}")
        except Exception as tf_err:
            print(f"❌ TensorFlow error: {tf_err}")
            print(traceback.format_exc())

        # If we reach here, all strategies failed
        print("\n" + "=" * 70)
        print("❌ CRITICAL: ALL MODEL LOADING STRATEGIES FAILED!")
        print("=" * 70)
        self._model = None
    
    def load_class_labels(self):
        """Load class labels from the text file with error handling."""
        if self._class_labels is not None:
            return

        from django.conf import settings
        import pathlib
        
        labels_path = pathlib.Path(settings.BASE_DIR) / 'models' / 'class_labels.txt'
        
        try:
            if labels_path.exists():
                with open(labels_path, 'r') as f:
                    self._class_labels = [line.strip() for line in f.readlines() if line.strip()]
                print(f"✅ Successfully loaded {len(self._class_labels)} class labels.")
            else:
                print(f"❌ ERROR: Class labels file NOT found at {labels_path}")
                self._class_labels = [] 
        except Exception as e:
            print(f"❌ ERROR loading class labels: {e}")
            self._class_labels = []
    
    def get_model(self):
        """Get the loaded model, loading it if necessary."""
        if self._model is None:
            self.load_model()
        return self._model
    
    def get_class_labels(self):
        """Get class labels, loading them if necessary."""
        if self._class_labels is None:
            self.load_class_labels()
        return self._class_labels


# Create a global instance
model_loader = ModelLoader()
