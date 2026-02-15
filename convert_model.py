import tensorflow as tf
import os

def convert_h5_to_tflite(h5_path, tflite_path):
    print(f"Loading .h5 model from {h5_path}...")
    model = tf.keras.models.load_model(h5_path)
    
    print("Converting to TFLite format...")
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimization (Optional but recommended for mobile/web)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    print(f"Saving TFLite model to {tflite_path}...")
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    
    print("Conversion complete! ✅")

if __name__ == "__main__":
    h5_file = os.path.join('models', 'sports_classifier.h5')
    tflite_file = os.path.join('models', 'sports_classifier.tflite')
    
    if os.path.exists(h5_file):
        convert_h5_to_tflite(h5_file, tflite_file)
    else:
        print(f"Error: {h5_file} not found. Please place your .h5 file in the models/ folder.")
