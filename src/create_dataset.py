import pandas as pd
import numpy as np
import random
np.random.seed(42)
random.seed(42)
DISEASES = {
    'Common Cold': ['Sneezing', 'Stuffy Nose', 'Sore Throat', 'Cough', 'Fever', 'Fatigue'],
    'Influenza (Flu)': ['High Fever', 'Chills', 'Muscle Aches', 'Fatigue', 'Cough', 'Headache', 'Sore Throat', 'Weakness'],
    'COVID-19': ['High Fever', 'Cough', 'Fatigue', 'Loss of Taste or Smell', 'Shortness of Breath', 'Muscle Aches'],
    'Allergies': ['Sneezing', 'Runny Nose', 'Itchy Eyes', 'Watery Eyes', 'Cough', 'Stuffy Nose'],
    'Migraine': ['Severe Headache', 'Nausea', 'Vomiting', 'Sensitivity to Light', 'Sensitivity to Sound', 'Visual Disturbances'],
    'Gastroenteritis (Stomach Flu)': ['Diarrhea', 'Nausea', 'Vomiting', 'Stomach Pain', 'Fever', 'Muscle Aches', 'Weakness'],
    'Asthma': ['Shortness of Breath', 'Chest Tightness', 'Wheezing', 'Cough'],
    'Pneumonia': ['High Fever', 'Chills', 'Difficulty Breathing', 'Chest Pain', 'Cough', 'Confusion', 'Fatigue'],
    'Anemia': ['Fatigue', 'Weakness', 'Pale Skin', 'Shortness of Breath', 'Dizziness', 'Cold Hands and Feet'],
    'Diabetes': ['Increased Thirst', 'Frequent Urination', 'Extreme Hunger', 'Unexplained Weight Loss', 'Fatigue', 'Blurred Vision', 'Weakness'],
    'Pregnancy': ['Missed Period', 'Nausea', 'Breast Tenderness', 'Frequent Urination', 'Fatigue', 'Mood Swings', 'Food Cravings', 'Vomiting', 'Weakness']
}
all_symptoms = set()
for symptoms in DISEASES.values():
    all_symptoms.update(symptoms)
all_symptoms = sorted(list(all_symptoms))
data = []
NUM_SAMPLES = 1000
for _ in range(NUM_SAMPLES):
    disease = random.choice(list(DISEASES.keys()))
    possible_symptoms = DISEASES[disease]
    num_symptoms = random.randint(2, len(possible_symptoms))
    selected_symptoms = set(random.sample(possible_symptoms, num_symptoms))
    if random.random() < 0.05:
        noise = random.choice(all_symptoms)
        selected_symptoms.add(noise)
    row = {}
    for symptom in all_symptoms:
        row[symptom] = 1 if symptom in selected_symptoms else 0
    row['Disease'] = disease
    data.append(row)
df = pd.DataFrame(data)
cols = [c for c in df.columns if c != 'Disease'] + ['Disease']
df = df[cols]
df.to_csv('data/dataset.csv', index=False)
print(f"Generated data/dataset.csv with {df.shape[0]} rows and {df.shape[1]} columns.")
