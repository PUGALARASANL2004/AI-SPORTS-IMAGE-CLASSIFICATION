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
        """Load the model (TFLite or H5) based on available libraries."""
        if self._model is not None:
            return

        # Use absolute paths to avoid issues on Render
        from django.conf import settings
        tflite_model_path = os.path.join(settings.BASE_DIR, 'models', 'sports_classifier.tflite')
        h5_model_path = os.path.join(settings.BASE_DIR, 'models', 'sports_classifier.h5')

        print(f"Checking for model at: {tflite_model_path}")

        # Try TFLite first (Highly optimized for memory)
        try:
            interpreter = None
            
            # 1. Try tflite_runtime (Production/Render)
            try:
                import tflite_runtime.interpreter as tflite
                if os.path.exists(tflite_model_path):
                    print(f"Loading TFLite model via tflite_runtime from {tflite_model_path}")
                    interpreter = tflite.Interpreter(model_path=tflite_model_path)
                else:
                    print(f"TFLite file NOT found at {tflite_model_path}")
            except ImportError as e:
                print(f"tflite_runtime import failed: {e}. Trying full tensorflow fallback...")

            # 2. Try full tensorflow (Local Development)
            if interpreter is None:
                try:
                    import tensorflow as tf
                    if os.path.exists(tflite_model_path):
                        print(f"Loading TFLite model via tensorflow.lite from {tflite_model_path}")
                        interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
                    elif os.path.exists(h5_model_path):
                        print(f"Loading H5 model from {h5_model_path}")
                        self._model = tf.keras.models.load_model(h5_model_path, compile=False)
                        print("H5 Model loaded successfully!")
                        return
                    else:
                        print(f"No model files found in {os.path.join(settings.BASE_DIR, 'models')}")
                except ImportError:
                    print("tensorflow not found in this environment")

            if interpreter:
                interpreter.allocate_tensors()
                self._model = interpreter
                print("TFLite Interpreter initialized successfully!")
            else:
                print("❌ CRITICAL: No model found or libraries missing. Application will fail to predict.")
                self._model = None
                
        except Exception as e:
            print(f"Error initializing model: {e}")
            self._model = None
    
    def load_class_labels(self):
        """Load class labels if not already loaded."""
        if self._class_labels is not None:
            return

        labels_path = os.path.join('models', 'class_labels.txt')
        
        if os.path.exists(labels_path):
            with open(labels_path, 'r') as f:
                self._class_labels = [line.strip() for line in f.readlines()]
        else:
            # Demo labels for ImageNet (will be replaced with actual sports labels)
            print("Warning: class_labels.txt not found. Using demo mode.")
            self._class_labels = self.generate_demo_sports_labels()
    
    def generate_demo_sports_labels(self):
        """Generate sample sports labels for demo purposes."""
        # ... (same as before) ...
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
