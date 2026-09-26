import json
import pickle
import numpy as np
class DiseaseModelEngine:
    def __init__(self, model_path='model.pkl', config_path='symptoms.json'):
        self.model_path = model_path
        self.config_path = config_path
        self.model = None
        self.symptoms_list = []
        self.classes = []
        self._load_model()
    def _load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.config_path, 'r') as f:
                config_data = json.load(f)
                self.symptoms_list = config_data.get('symptoms', [])
                self.classes = config_data.get('classes', [])
        except Exception as e:
            print(f"Engine Warning - Failed to load model or config: {e}")
            self.model = None
            self.symptoms_list = []
    def get_symptoms(self):
        return self.symptoms_list
    def is_ready(self):
        return self.model is not None and len(self.symptoms_list) > 0
    def predict(self, selected_symptoms):
        if not self.is_ready():
            return None, "N/A"
        input_data = []
        for s in self.symptoms_list:
            if s in selected_symptoms:
                input_data.append(1)
            else:
                input_data.append(0)
        input_array = np.array(input_data).reshape(1, -1)
        predicted_disease = self.model.predict(input_array)[0]
        try:
            probabilities = self.model.predict_proba(input_array)[0]
            max_prob = max(probabilities)
            confidence = round(max_prob * 100, 2)
        except AttributeError:
            confidence = "N/A"
        return predicted_disease, confidence
