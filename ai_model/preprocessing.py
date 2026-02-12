import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.efficientnet import preprocess_input


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction.
    
    Args:
        image_path: Path to the image file
        target_size: Target size tuple (height, width)
    
    Returns:
        Preprocessed image array
    """
    try:
        # Load and resize image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize(target_size, Image.LANCZOS)
        
        # Convert to array
        img_array = keras_image.img_to_array(img)
        
        # Expand dimensions for batch processing
        img_array = np.expand_dims(img_array, axis=0)
        
        # Apply model-specific preprocessing
        img_array = preprocess_input(img_array)
        
        return img_array
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        raise
