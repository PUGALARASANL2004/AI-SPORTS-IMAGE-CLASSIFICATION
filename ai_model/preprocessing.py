
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
        import numpy as np
        from PIL import Image

        # Load and resize image
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize(target_size, Image.LANCZOS)
        
        # Convert to array (Equivalent to keras_image.img_to_array)
        img_array = np.array(img, dtype=np.float32)
        
        # Expand dimensions for batch processing
        img_array = np.expand_dims(img_array, axis=0)
        
        # NOTE: EfficientNet in tf.keras has a Rescaling layer built-in,
        # so preprocess_input is an identity function. We can skip the TF import.
        
        return img_array
    
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        raise
