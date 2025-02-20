import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from django.conf import settings


db_dir = os.path.join(settings.BASE_DIR, 'db')
if not os.path.exists(db_dir):
    print("exist")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
MODEL_PATH = os.path.join(BASE_DIR, "ML", "distraction.h5") 



def predict_distraction(target_size=(256, 256),username="arjunbiju322@gmail.com"):
    """Loads a fixed model, processes an image, and makes a prediction."""
    folder_name = username
    folder_path = os.path.join(db_dir, folder_name)
    image_path = os.path.join(folder_path,'', ".tmp.jpg") 
    try:
        # Load the model
        model = tf.keras.models.load_model(MODEL_PATH)
        print("Model loaded successfully!")
        print("Expected input shape:", model.input_shape)
        
        # Load and preprocess the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Error: Image not found or unable to read.")
        
        image_resized = cv2.resize(image, target_size)
        image_array = np.expand_dims(image_resized, axis=0)  # Add batch dimension
        image_array = image_array / 255.0  # Normalize pixel values
        
        # Make prediction
        predictions = model.predict(image_array)
        prediction_label = 'not engaged' if predictions[0] > 0.5 else 'engaged'
        
        return prediction_label, predictions
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# image_path = r"ML\WIN_20250217_12_06_05_Pro.jpg"  
    
# prediction, scores = predict_distraction(image_path)
# if prediction is not None:
#     print(f"Prediction: {prediction}, Scores: {scores}")
