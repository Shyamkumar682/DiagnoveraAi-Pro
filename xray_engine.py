import os
import cv2
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from path import XRAY_MODEL_PATH, SYMPTOMS_JSON_PATH, FALLBACK_SYMPTOMS_JSON_PATH
IMG_SIZE = 150
LABELS = ['PNEUMONIA', 'NORMAL']
def load_symptoms():
    if not os.path.exists(SYMPTOMS_JSON_PATH):
        if os.path.exists(FALLBACK_SYMPTOMS_JSON_PATH):
            with open(FALLBACK_SYMPTOMS_JSON_PATH, 'r') as f:
                data = json.load(f)
            return data.get('symptoms', [])
        return []
    with open(SYMPTOMS_JSON_PATH, 'r') as f:
        data = json.load(f)
    return data.get('symptoms', [])
def predict_pneumonia(img_path):
    if not os.path.exists(XRAY_MODEL_PATH):
        return {"error": "Model not trained yet or model.h5 is missing."}
    try:
        model = load_model(XRAY_MODEL_PATH)
    except Exception as e:
        return {"error": f"Failed to load model: {str(e)}"}
    img_arr = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img_arr is None:
        return {"error": "Invalid image file. Could not read image."}
    resized_arr = cv2.resize(img_arr, (IMG_SIZE, IMG_SIZE))
    resized_arr = resized_arr / 255.0
    x_in = resized_arr.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    prediction = model.predict(x_in)
    prob = float(prediction[0][0])
    class_idx = 1 if prob > 0.5 else 0
    confidence = prob if class_idx == 1 else (1.0 - prob)
    predicted_label = LABELS[class_idx]
    result = {
        "prediction": predicted_label,
        "confidence": round(confidence * 100, 2)
    }
    if predicted_label == "PNEUMONIA":
        all_symptoms = load_symptoms()
        pneumonia_symptoms_list = [
            "Fever", "High Fever", "Chills", "Cough", "Shortness of Breath", "Fatigue",
            "Chest Pain", "Muscle Aches", "Nausea", "Vomiting", "Confusion", "Weakness", "Sweating"
        ]
        symptoms = [s for s in pneumonia_symptoms_list if s in all_symptoms]
        if not symptoms:
            symptoms = pneumonia_symptoms_list
        result["symptoms"] = symptoms
        result["message"] = "Seek medical evaluation. Your X-Ray indicates possible Pneumonia."
    else:
        result["symptoms"] = []
        result["message"] = "Your X-Ray looks normal. Maintain healthy habits."
    return result
