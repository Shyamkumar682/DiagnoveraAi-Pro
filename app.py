import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from model_engine import DiseaseModelEngine
from xray_engine import predict_pneumonia
from path import DISEASE_MODEL_PATH, SYMPTOMS_JSON_PATH, UPLOAD_FOLDER
from history_manager import log_history, get_history, clear_history
app = Flask(__name__)
app.secret_key = "diagnovera_secret_key"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
engine = DiseaseModelEngine(DISEASE_MODEL_PATH, SYMPTOMS_JSON_PATH)
PRECAUTIONS = {
    'Common Cold': "Rest, stay hydrated, and consider over-the-counter cold medicines.",
    'Influenza (Flu)': "Get plenty of rest, drink fluids, and monitor your fever. Consult a doctor if symptoms worsen.",
    'COVID-19': "Isolate yourself, wear a mask around others, and monitor your oxygen levels. Seek medical help if you experience breathing difficulties.",
    'Allergies': "Avoid known allergens, keep windows closed during high pollen counts, and use antihistamines if necessary.",
    'Migraine': "Rest in a quiet, dark room. Stay hydrated and try hot or cold compresses. Consult your doctor for severe migraines.",
    'Gastroenteritis (Stomach Flu)': "Stay hydrated with clear fluids or oral rehydration solutions. Eat bland foods cautiously.",
    'Asthma': "Avoid asthma triggers, use your prescribed inhaler as directed, and seek emergency care if you cannot catch your breath.",
    'Pneumonia': "Consult a doctor immediately for proper diagnosis and potential antibiotics or tailored treatment. Rest extensively.",
    'Anemia': "Incorporate iron-rich foods into your diet like spinach and red meat. Speak to a doctor about iron supplements.",
    'Diabetes': "Monitor blood sugar levels closely, maintain a balanced diet, and consult your endocrinologist for a precise care plan."
}
@app.route('/')
def home():
    return render_template('index.html', symptoms=engine.get_symptoms())
@app.route('/predict', methods=['POST'])
def predict():
    if not engine.is_ready():
        return "Model or Config not found. Please ask the administrator to train the model.", 500
    selected_symptoms = request.form.getlist('symptoms')
    patient_name = request.form.get('patient_name', 'Unknown')
    patient_age = request.form.get('patient_age', 'N/A')
    patient_gender = request.form.get('patient_gender', 'N/A')
    pregnancy_status = request.form.get('pregnancy_status', 'Not Applicable')
    symptom_duration = request.form.get('symptom_duration', 'N/A')
    if not selected_symptoms:
        return render_template('index.html', symptoms=engine.get_symptoms(), error="Please select at least one symptom.")
    predicted_disease, confidence = engine.predict(selected_symptoms)
    precaution = PRECAUTIONS.get(predicted_disease, "Consult a medical professional for personalized advice.")
    log_history("Symptom Analysis", patient_name, predicted_disease, f"{confidence}%")
    return render_template('result.html', 
                           disease=predicted_disease, 
                           symptoms=selected_symptoms, 
                           confidence=f"{confidence}%", 
                           precaution=precaution,
                           patient_name=patient_name,
                           patient_age=patient_age,
                           patient_gender=patient_gender,
                           pregnancy_status=pregnancy_status,
                           symptom_duration=symptom_duration)
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/resources')
def resources():
    return render_template('resources.html')
@app.route('/xray', methods=['GET'])
def xray_index():
    patient_name = request.args.get('patient_name', '')
    patient_age = request.args.get('patient_age', '')
    patient_gender = request.args.get('patient_gender', '')
    return render_template('xray.html', 
                           patient_name=patient_name, 
                           patient_age=patient_age, 
                           patient_gender=patient_gender)
@app.route('/predict_xray', methods=['POST'])
def predict_xray():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('xray_index', error="No selected file"))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        patient_name = request.form.get('patient_name', 'Unknown Patient')
        patient_age = request.form.get('patient_age', 'N/A')
        patient_gender = request.form.get('patient_gender', 'N/A')
        result = predict_pneumonia(filepath)
        if "error" in result:
            return render_template('xray.html', error=result["error"])
        log_history("X-Ray Diagnostics", patient_name, result['prediction'], f"{result['confidence']}%")
        return render_template('xray_result.html', 
                               image_file=filename,
                               prediction=result['prediction'],
                               confidence=result['confidence'],
                               symptoms=result['symptoms'],
                               message=result['message'],
                               patient_name=patient_name,
                               patient_age=patient_age,
                               patient_gender=patient_gender)
    return render_template('xray.html', error="Invalid file extension. Please upload PNG, JPG, or JPEG.")
@app.route('/history')
def history():
    log_data = get_history()
    return render_template('history.html', history_records=log_data)
@app.route('/clear_history', methods=['POST'])
def clear_history_route():
    clear_history()
    return redirect(url_for('history'))
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
