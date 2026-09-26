# 🚀 Project Run Instructions

This document provides a comprehensive, step-by-step guide to setting up and running the DiagnoveraAI Pro application (Symptom Analyzer & X-Ray Diagnostics) on your local machine.

---

## 🛠️ Step 1: Prerequisites

Before running the application, ensure you have the following installed:
- **Python 3.8+**: Ensure Python is added to your system PATH.
- **Git** (Optional, for version control).

---

## 📦 Step 2: Environment Setup & Installation

It is highly recommended to use a virtual environment to avoid dependency conflicts.

### 1. Open your terminal (PowerShell or Command Prompt)
Navigate to the root directory of the project:
```bash
# Example:
cd "d:\books\mini_project(orignal)"
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# This creates an isolated Python environment named 'venv'
python -m venv venv

# Activate the virtual environment (Windows)
.\venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries listed in the `requirements.txt` file:
```bash
# This will install Flask, pandas, tensorflow, scikit-learn, etc.
pip install -r requirements.txt

# Note: If you want to run the outlier graph script, also install seaborn
pip install seaborn
```

---

## 🏃 Step 3: Running the Application

### Running the Main Web App (Flask)
The core of the project is a web application built with Flask. To start the server:

```bash
# Run the main Flask application script
python app.py
```
**What happens next?**
- The terminal will display a local address, usually: `http://127.0.0.1:5000/`
- Open your web browser (Chrome, Edge, Safari) and navigate to that URL.
- You can now interact with the Symptom Analyzer and X-Ray Diagnosis tools!

---

## 📊 Step 4: Running Additional Scripts

There are other utility scripts in this folder that you can run independently of the web app.

### 1. Generating Outlier Graphs
If you want to analyze your dataset and generate visualizations for symptom outliers:
```bash
# Run the outlier generation script
python generate_outliers.py
```
- **Result:** This will read `data/dataset.csv` and save boxplots and histograms into the `static/graphs/` directory.

### 2. Training the Model (If Applicable)
If you need to retrain the underlying machine learning models, scripts are located in the `src/` directory.
```bash
# Example: Running the training script
python src/train_model.py
```

---

## 📁 Directory Structure Overview

Here is a quick guide to what each folder does, so you know where to look:

- **`/data`**: Contains the datasets (`dataset.csv`, `symptoms.json`) used by the app.
- **`/models`**: Stores the trained machine learning models used for prediction.
- **`/static`**: Contains static web assets like CSS styles, JavaScript, generated graphs, and uploaded X-rays.
- **`/templates`**: Contains the HTML files (`index.html`, `xray.html`, etc.) for the web interface.
- **`app.py`**: The main entry point for the Flask web application.
- **`model_engine.py` / `xray_engine.py`**: The logic that handles symptom and X-ray predictions.
- **`history_manager.py`**: Manages the logging and retrieval of patient diagnostic history.
