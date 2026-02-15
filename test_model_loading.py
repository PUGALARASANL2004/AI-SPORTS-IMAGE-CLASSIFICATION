import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from ai_model.predictor import predictor
from ai_model.model_loader import model_loader

def test_prediction():
    print("Checking model loading...")
    try:
        model = model_loader.get_model()
        if model is None:
            print("❌ FAILED: Model is None")
            return
        print("✅ SUCCESS: Model loaded")
        
        labels = model_loader.get_class_labels()
        print(f"Number of labels: {len(labels)}")
        
        # Test with a dummy image if possible, or just print details
        print(f"Model type: {type(model)}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction()
