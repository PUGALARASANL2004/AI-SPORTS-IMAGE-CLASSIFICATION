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
        """Load the model (TFLite or H5) with robust error handling and fallbacks."""
        if self._model is not None:
            return

        from django.conf import settings
        import pathlib
        
        # Use absolute paths using Pathlib for better cross-platform support
        base_path = pathlib.Path(settings.BASE_DIR)
        models_dir = base_path / 'models'
        tflite_model_path = models_dir / 'sports_classifier.tflite'
        h5_model_path = models_dir / 'sports_classifier.h5'

        print(f"--- AI Model Loading Debug ---")
        print(f"BASE_DIR: {settings.BASE_DIR}")
        print(f"Models Directory: {models_dir}")
        
        if models_dir.exists():
            print(f"Files in models dir: {[f.name for f in models_dir.iterdir()]}")
        else:
            print(f"❌ ERROR: Models directory DOES NOT EXIST at {models_dir}")
            self._model = None
            return

        # Strategy 1: Try tflite_runtime (Production/Render - most memory efficient)
        try:
            import tflite_runtime.interpreter as tflite
            print("✓ tflite_runtime successfully imported.")
            
            if tflite_model_path.exists():
                print(f"→ Attempting to load TFLite model from {tflite_model_path}")
                try:
                    interpreter = tflite.Interpreter(model_path=str(tflite_model_path))
                    interpreter.allocate_tensors()
                    self._model = interpreter
                    print("✅ SUCCESS: TFLite model loaded via tflite_runtime!")
                    return
                except Exception as tflite_err:
                    print(f"⚠️ TFLite allocation failed: {tflite_err}")
            else:
                print(f"⚠️ TFLite file NOT found at {tflite_model_path}")
        except ImportError:
            print("ℹ️ tflite_runtime not available (expected in local dev)")

        # Strategy 2: Try TensorFlow with TFLite (Fallback 1)
        try:
            import tensorflow as tf
            print("✓ tensorflow successfully imported.")
            
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
            
            # Strategy 3: Try H5 model (Fallback 2 - works locally, but memory intensive)
            if h5_model_path.exists():
                print(f"→ Attempting H5 model from {h5_model_path}")
                try:
                    self._model = tf.keras.models.load_model(str(h5_model_path), compile=False)
                    print("✅ SUCCESS: H5 model loaded via tensorflow!")
                    return
                except Exception as h5_err:
                    print(f"❌ H5 model loading failed: {h5_err}")
            else:
                print(f"⚠️ H5 file NOT found at {h5_model_path}")
                
        except ImportError:
            print("❌ tensorflow not installed/found.")
        except Exception as tf_err:
            print(f"❌ TensorFlow error: {tf_err}")
            import traceback
            traceback.print_exc()

        # If we reach here, all strategies failed
        print("❌ CRITICAL: Failed to load model with any strategy!")
        print("   - TFLite via tflite_runtime: Failed or not available")
        print("   - TFLite via tensorflow: Failed or not available")  
        print("   - H5 via tensorflow: Failed or not available")
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
    
    def generate_demo_sports_labels(self):
        """Generate sample sports labels for demo purposes."""
        sports = [
            'air hockey', 'ampute football', 'archery', 'arm wrestling', 'axe throwing',
            'balance beam', 'barell racing', 'baseball', 'basketball', 'baton twirling',
            'bike polo', 'billiards', 'bmx', 'bobsled', 'bowling',
            'boxing', 'bull riding', 'bungee jumping', 'canoe slamon', 'cheerleading',
            'chuckwagon racing', 'cricket', 'croquet', 'curling', 'disc golf',
            'fencing', 'field hockey', 'figure skating men', 'figure skating pairs', 'figure skating women',
            'fly fishing', 'football', 'formula 1 racing', 'frisbee', 'gaga',
            'giant slalom', 'golf', 'hammer throw', 'hang gliding', 'harness racing',
            'high jump', 'hockey', 'horse jumping', 'horse racing', 'horseshoe pitching',
            'hurdles', 'hydroplane racing', 'ice climbing', 'ice yachting', 'jai alai',
            'javelin', 'jousting', 'judo', 'lacrosse', 'log rolling',
            'luge', 'motorcycle racing', 'mushing', 'nascar racing', 'olympic wrestling',
            'parallel bar', 'pole climbing', 'pole dancing', 'pole vault', 'polo',
            'pommel horse', 'rings', 'rock climbing', 'roller derby', 'rollerblade racing',
            'rowing', 'rugby', 'sailboat racing', 'shot put', 'shuffleboard',
            'sidecar racing', 'ski jumping', 'sky surfing', 'skydiving', 'snow boarding',
            'snowmobile racing', 'speed skating', 'steer wrestling', 'sumo wrestling', 'surfing',
            'swimming', 'table tennis', 'tennis', 'track bicycle', 'trapeze',
            'tug of war', 'ultimate', 'uneven bars', 'volleyball', 'water cycling',
            'water polo', 'weightlifting', 'wheelchair basketball', 'wheelchair racing', 'wingsuit flying'
        ]
        return sports[:100]  # Ensure we have exactly 100 labels
    
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
