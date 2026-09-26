# DiagnoveraAI Pro - Project Directory Structure

```text
mini_project(orignal)/
|-- app.py                     # Main Flask Web routing Controller
|-- history_manager.py         # CSV Logging and Session History Manager
|-- model_engine.py            # Machine Learning Backend (Symptom-Based Disease Prediction)
|-- xray_engine.py             # Deep Learning Backend (Chest X-Ray Pneumonia Prediction)
|-- path.py                    # Centralized File Path Configurations
|-- symptoms.json              # Master Dictionary Mapping Symptoms to Medical Precautions
|-- diagnostic_history.csv     # Persistent Session Records / Clinical Ledger
|-- CT_Scan.ipynb              # Jupyter Notebook Exploratory Data Analysis & Prototyping
|
|-- Chapter_*.md               # Project Documentation Chapters (Architecture, Conclusion, etc.)
|
+-- chest_xray/                # Radiographic / CNN Pipeline Context
|   |-- chest_xray_model.keras # Pre-trained Convolutional Neural Network Target Model
|   |-- chest_xray/            # Massive Image Dataset Root (train/, test/, val/ distributions)
|   |-- app.py                 # (Sandbox/Test API for isolated X-Ray debugging)
|   +-- model_engine/          # Deep Learning Model Scripts (config.py, predict.py, train.py)
|
+-- data/                      # Textual Datasets
|   +-- dataset.csv            # Procedurally Generated Symptom Vector Data (1,000 samples)
|
+-- models/                    # Serialized Machine Learning Output
|   +-- model.pkl              # Pickled Random Forest Classifier (Symptom Predictions)
|
+-- src/                       # Data Processing Automation
|   |-- create_dataset.py      # Script generating the random 11-disease binary database
|   +-- train_model.py         # Script training Random Forest Classifier against dataset.csv
|
+-- static/                    # Frontend Public Assets & Outputs
|   |-- style.css              # Application Theme System (Animations, Print Media Queries, Dark Mode)
|   |-- main.js / pdf_export.js# Client-side form validations and print handling
|   +-- graphs/                # Analysis Visualizations (Learning Curves, Confusion Matrix)
|   +-- uploads/               # Target localized cache for patient-uploaded Medical Images
|
+-- templates/                 # Decoupled Jinja UI Views
|   |-- index.html             # Main View: Interactive Symptom Input Form
|   |-- xray.html              # Main View: Chest X-Ray Image Upload Portal
|   |-- result.html            # Output View: Returns Symptom Predictions, Scored Confidence, Precautions
|   |-- xray_result.html       # Output View: Returns Pneumonia Classification and Warning Modals
|   |-- history.html           # Output View: Tabular representation of diagnostic_history.csv
|   |-- about.html             # Information View: X-Ray Labs / Hospital Google Map Integrations
|   |-- resources.html         # Information View: Public Medical References 
|   +-- report_template.html   # Report View: Dedicated interface rendering printable diagnostic outputs
|
+-- reports/                   # Miscellaneous
    |-- chapter1_introduction.txt
    +-- metrics_report.txt
```
