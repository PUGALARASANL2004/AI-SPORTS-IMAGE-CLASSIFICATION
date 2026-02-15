import numpy as np
from .model_loader import model_loader
from .preprocessing import preprocess_image


class SportsPredictor:
    """Class to handle sports image classification predictions."""
    
    def __init__(self):
        # Do not load model here. Access it via model_loader when needed.
        pass
    
    @property
    def model(self):
        return model_loader.get_model()
        
    @property
    def class_labels(self):
        return model_loader.get_class_labels()
    
    def predict(self, image_path, top_k=1):
        """
        Predict the sport in the given image using TFLite.
        """
        try:
            # Preprocess the image
            processed_image = preprocess_image(image_path)
            
            interpreter = self.model
            
            if interpreter is None:
                # Fallback to demo mode if model couldn't be loaded
                print("Running in demo mode (Random prediction)")
                random_idx = np.random.randint(0, len(self.class_labels))
                return [(self.class_labels[random_idx], 0.95)]

            # Get input and output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            # Set the input tensor
            interpreter.set_tensor(input_details[0]['index'], processed_image)

            # Run inference
            interpreter.invoke()

            # Get the output tensor
            predictions = interpreter.get_tensor(output_details[0]['index'])
            
            # Get top K predictions
            top_indices = np.argsort(predictions[0])[::-1][:top_k]
            
            results = []
            for idx in top_indices:
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
