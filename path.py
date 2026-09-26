import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DISEASE_MODEL_PATH = os.path.join(ROOT_DIR, 'models', 'model.pkl')
SYMPTOMS_JSON_PATH = os.path.join(ROOT_DIR, 'data', 'symptoms.json')
FALLBACK_SYMPTOMS_JSON_PATH = r'd:\Learning\jupitor\symptoms.json'
XRAY_MODEL_PATH = os.path.join(ROOT_DIR, 'major_project', 'model_engine', 'model.h5')
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'static', 'uploads')
HISTORY_CSV_PATH = os.path.join(ROOT_DIR, 'data', 'history.csv')
