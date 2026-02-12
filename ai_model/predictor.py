import numpy as np
from .model_loader import model_loader
from .preprocessing import preprocess_image


class SportsPredictor:
    """Class to handle sports image classification predictions."""
    
    def __init__(self):
        self.model = model_loader.get_model()
        self.class_labels = model_loader.get_class_labels()
    
    def predict(self, image_path, top_k=1):
        """
        Predict the sport in the given image.
        
        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return
        
        Returns:
            List of tuples (class_name, confidence_score)
        """
        try:
            # Preprocess the image
            processed_image = preprocess_image(image_path)
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get top K predictions
            top_indices = np.argsort(predictions[0])[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                # Map ImageNet classes to demo sports labels using modulo
                # This ensures we always get a result even in demo mode
                label_idx = idx % len(self.class_labels) if idx >= len(self.class_labels) else idx
                class_name = self.class_labels[label_idx]
                confidence = float(predictions[0][idx])
                results.append((class_name, confidence))
            
            return results
        
        except Exception as e:
            print(f"Error during prediction: {e}")
            raise
    
    def predict_top(self, image_path):
        """
        Get the top prediction for an image.
        
        Args:
            image_path: Path to the image file
        
        Returns:
            Tuple of (class_name, confidence_score)
        """
        results = self.predict(image_path, top_k=1)
        return results[0] if results else ("Unknown", 0.0)


# Create a global predictor instance
predictor = SportsPredictor()
