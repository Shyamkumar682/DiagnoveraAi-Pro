import os
import csv
from datetime import datetime
from path import HISTORY_CSV_PATH
def init_csv():
    os.makedirs(os.path.dirname(HISTORY_CSV_PATH), exist_ok=True)
    if not os.path.exists(HISTORY_CSV_PATH):
        with open(HISTORY_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Type', 'Patient Name', 'Result', 'Confidence'])
def log_history(diagnostic_type, patient_name, result, confidence):
    init_csv()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, diagnostic_type, patient_name, result, confidence])
def get_history():
    init_csv()
    history = []
    with open(HISTORY_CSV_PATH, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            history.append(row)
    return history[::-1]  
def clear_history():
    init_csv()
    with open(HISTORY_CSV_PATH, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Type', 'Patient Name', 'Result', 'Confidence'])
