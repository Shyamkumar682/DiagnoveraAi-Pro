# MediAI: Diseases and Symptoms Diagnoses 
### A Machine Learning powered Clinical Diagnostic System
**Date:** April 14, 2026

---

## 1. Executive Summary
The **MediAI: Diseases and Symptoms Diagnoses** project aims to predict an individual's underlying disease based on a provided set of symptoms using machine learning. The solution encompasses an end-to-end pipeline starting from the generation of a balanced, synthetic dataset representing various ailments (such as COVID-19, Influenza, Migraine, and Asthma) to the training and evaluation of robust classification models. The final model is serialized and decoupled via a dedicated model engine, integrating seamlessly into a modern Flask web application. This provides an interactive user interface for collecting patient demographics and symptoms, producing instant clinical predictions alongside confidence scores and tailored precautions.

---

## 2. Project Overview

### 2.1 Objectives
* **Dataset Generation:** Develop a comprehensive, balanced synthetic dataset mapping various common diseases to their definitive and noisy symptoms.
* **Model Training & Tuning:** Train and hyperparameter-tune Decision Tree and Random Forest classifiers to establish reliable predictive baselines.
* **Robust Evaluation:** Extensively evaluate model performance using cross-validation, confusion matrices, and macro-averaged Precision, Recall, and F1 metrics to prevent data leakage and bias.
* **Decoupled Architecture:** Isolate the model inference logic from the web application layer through a dedicated `DiseaseModelEngine` class.
* **Interactive Web Interface:** Build a responsive Flask-based web application to collect user demographics and symptoms, providing real-time predictions and medical precautions.

### 2.2 Project Components

| File Name | Description |
| :--- | :--- |
| `src/create_dataset.py` | Generates the synthetic dataset mapping diseases to symptomatic features, including random noise for model robustness. |
| `data/dataset.csv` | The generated dataset holding binary symptom indicators and the target disease class. |
| `src/train_model.py` | Main script for training, tuning (GridSearchCV), evaluating, and serializing the Scikit-Learn models. |
| `model_engine.py` | Contains the `DiseaseModelEngine` class responsible for loading the trained model/config and executing predictions. |
| `app.py` | The Flask web application handling frontend-backend routing, user requests, and precaution mapping. |
| `data/symptoms.json` | Configuration file storing the list of symptoms and target classes used during model training. |
| `models/model.pkl` | The serialized (Pickle) final chosen machine learning model. |

---

## 3. Dataset Description

### 3.1 Data Summary

| Attribute | Data Type | Description |
| :--- | :--- | :--- |
| `Symptom_*` (e.g., `Fever`, `Cough`) | Integer (Binary 0/1) | Input features representing the presence (1) or absence (0) of a specific symptom. |
| `Disease` | String (Categorical) | The target variable representing the predicted ailment (e.g., 'Common Cold', 'Diabetes'). |

### 3.2 Class Imbalance
The target variable distribution is **highly balanced**. Since the dataset is generated synthetically (`NUM_SAMPLES = 1000`), the `create_dataset.py` script uniformly samples from the distinct disease categories. This mitigates traditional class imbalance issues and prevents the model from developing a majority-class bias.

### 3.3 Data Cleaning
* **Missing Value Handling:** Cleaned by proactively dropping `NA` values (to ensure runtime stability, despite the synthetic nature being inherently clean).
* **Noise Injection:** A 5% chance of injecting "noise" (a random unrelated symptom) was added during data creation to make the learning algorithm more generalized and robust against isolated atypical symptom combinations.

---

## 4. Exploratory Data Analysis (EDA)
* **Direct Causal Correlations:** Distinct subsets of symptoms strongly correlate with specific diseases (e.g., 'Loss of Taste or Smell' has near-perfect correlation with 'COVID-19').
* **Symptom Overlap:** General symptoms like 'Fatigue', 'Weakness', and 'Fever' are highly prevalent across multiple target classes (e.g., common across Influenza, COVID-19, Pneumonia, and Anemia), introducing non-linear complexity.
* **Tree-based Feature Importance:** EDA via `RandomForest` feature importance reveals that highly specific symptoms acts as strong splits at the root nodes, dictating early classifications.

---

## 5. Data Preprocessing

### 5.1 Feature Engineering
* **Numeric:** None
* **Categorical (Target):** `Disease` (Categorical String, natively handled or implicitly encoded via `best_model.classes_`).
* **Categorical (Features):** All symptom inputs are formulated as **Binary** (0 or 1) features matching independent symptom states.

### 5.2 Preprocessing Pipeline
* **Encoding:** No numerical scaling pipeline (e.g., `StandardScaler`) is necessary since all feature variables are binary indicators representing one-hot encoded symptom presences.
* **Vector Formatting:** The `model_engine.py` dynamically builds a binary array structure correlating the end-user's selected string symptoms into the identical feature array shape expected by the model.

### 5.3 Train/Validation Split
The dataset employs an **80/20 splitting strategy** (80% Training, 20% Testing) orchestrated via `train_test_split` seeded with `random_state=42` to guarantee reproducibility. 

---

## 6. Model Training & Evaluation

### 6.1 Baseline Models

| Model | Hyperparameters Tuned | Key Characteristics |
| :--- | :--- | :--- |
| **Decision Tree** | `max_depth`, `min_samples_split` | Highly interpretable, creates hard binary splits based on key symptoms, but prone to slight overfitting on noisy features. |
| **Random Forest** | `n_estimators`, `max_depth` | Ensemble approach aggregating multiple decision trees; robust against overfitting and highly accurate under overlapping symptom sets. |

### 6.2 Specialized Techniques
* **Hyperparameter Tuning (GridSearchCV):** Employed 5-fold cross-validated grid search to find the optimal estimators (e.g., tuning tree depth and estimator count).
* **Learning Curves:** Programmatically analyzed to detect metrics for Overfitting vs. Underfitting by observing train/validation trajectory variations based on training set size.
* **Model Decoupling:** Model parameters (`classes_`) and feature structures are saved into an external `symptoms.json` configuration file to allow inference decoupled from the exact training environment.

### 6.3 Evaluation Metrics
* **Accuracy:** Initial assessment of overall correctly classified diagnoses.
* **Macro-Averaged Precision, Recall, and F1-Score:** Leveraged `macro` averaging (which weighs all classes equally regardless of instance count) to ensure the model exhibits uniformly high predictive confidence across every single disease category.
* **Confusion Matrix:** Discovers exact misclassifications between heavily overlapping ailments (e.g., Common Cold vs. Allergies). 

### 6.4 Final Model
* **Selection:** The evaluation suite automatically picks the best performing model based on the Test setup (typically the **Random Forest**).
* **Serialization:** The chosen pipeline is serialized unconditionally using **Pickle** directly to `models/model.pkl`, enabling lightweight and instantaneous loading downstream in the Flask app sequence.

---

## 7. Web Application

### 7.1 Architecture
The application runs on a **Flask (Python) Backend** communicating with a responsive **HTML/JS Frontend**. The architecture strictly isolates the AI logic via the `DiseaseModelEngine` class, ensuring that the web router (`app.py`) only receives strings and passes back visual components, while the backend engine safely manages the Scikit-Learn logic, state matrices, array reshaping, and deserialization. 

### 7.2 Prediction Flow
1. **User Input:** The user fills the HTML form on the index page, marking patient demographics and ticking observed symptom checkboxes.
2. **Form Submission:** A `POST` payload is routed to `/predict`. 
3. **Engine Evaluation:** The `DiseaseModelEngine` catches the raw array of symptom strings, checks them against the original `symptoms.json` master list, and marshals a 1xN NumPy binary array.
4. **Prediction & Confidence:** The serialized model receives the array, returning the absolute predicted class string and calculating the highest probability branch for a percentage Confidence Score.
5. **Precaution Mapping & Rendering:** Flask retrieves disease-tailored advice from the `PRECAUTIONS` dictionary and renders Jinja templates directly to the user detailing their complete diagnostic result.

### 7.3 Input Features Collected

| UI Field | HTML Input Type | Validation Ranges / Expected Output |
| :--- | :--- | :--- |
| **Patient Name** | `text` | Unrestricted string input (fallback to 'Unknown'). |
| **Patient Age** | `number` | Numeric ranges typically >0 (fallback to 'N/A'). |
| **Patient Gender** | `select` / `radio` | Fixed string categories (e.g., Male, Female, Other). |
| **Pregnancy Status** | `select` / `radio` | Fixed string categories (fallback to 'Not Applicable'). |
| **Symptom Duration** | `text` / `select` | Expected time range format (e.g., "3 days"). |
| **Symptoms** | `checkbox` | Multi-select boolean values directly aligning with the JSON master config. |

---

## 8. Technology Stack

| Category | Technology |
| :--- | :--- |
| **Programming Languages** | Python, HTML5, CSS3, JavaScript |
| **Data Manipulation** | Pandas, NumPy |
| **Machine Learning** | Scikit-Learn (Decision Tree, Random Forest, GridSearchCV) |
| **Web Framework** | Flask, Jinja2 Template Engine |
| **Serialization & Plotting** | Pickle, Matplotlib |

---

## 9. Conclusion & Future Work

### 9.1 Summary
The MediAI Disease Diagnosis project successfully integrates a robust machine learning pipeline into a decoupled web interface. By using a simulated, balanced symptom dataset coupled with an optimal Random Forest classifier, the application achieves a highly confident and deterministic end-user diagnostic experience that adheres to clinical interface guidelines.

### 9.2 Limitations
* **Synthetic Data Constraint:** The model trains on synthetically created data patterns. While logically sound within its closed system, the absence of real-world patient records means it cannot adapt completely to rare edge-case biological presentations.
* **Limited Scope:** The underlying JSON only supports a finite number of configured ailments and specific symptoms, restraining it from providing highly generic triage.

### 9.3 Future Improvements
* **Real-World EMR Data Integration:** Re-train Version 2.0 purely utilizing anonymized, real-world Electronic Medical Records to improve validity.
* **Advanced NLP Form Entry:** Allow users to describe symptoms in natural language, utilizing an LLM or traditional NLP chunking to parse strings to our defined vector inputs.
* **Automated Data Retraining Pipeline:** Setup chron-jobs or Airflow flows to automatically regenerate and retrain the Pickle models as new dynamic inputs are pushed to a relational SQL Database instead of a static CSV.
