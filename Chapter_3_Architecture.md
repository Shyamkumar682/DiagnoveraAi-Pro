# 3. Proposed Methodology & System Architecture

## 3.1 High-Level System Architecture
The **DiagnoveraAI Pro (MediAI)** system is built upon a modular, decoupled architectural pattern that strictly separates the user interface from the underlying machine learning logic. The system follows a standard Client-Server model facilitated by the **Flask web framework**. 

At a high level, the flow of the system operates as follows:
1.  **Presentation Layer (Client):** The user interacts with responsive web interfaces (constructed using HTML, CSS, and Jinja2) via a web browser. They can either provide text-based symptoms and demographics for general diagnosis or upload a medical image for radiographic screening.
2.  **Application Routing Layer (Flask Backend):** The `app.py` script serves as the centralized controller. It acts as a gateway that receives HTTP `POST` and `GET` requests, safely extracts form inputs/image payloads, validates them, and routes them to the appropriate artificial intelligence module.
3.  **Artificial Intelligence Engines:** Depending on the route, the controller invokes either the **Symptom Engine** (`DiseaseModelEngine`) or the **Radiology Engine** (`predict_pneumonia`). These engines operate in isolated silos, completely agnostic to the web components.
4.  **Data Persistence Layer:** Once an engine returns a diagnostic prediction, the web controller formats the output, fetches matching medical precautions from an internal dictionary, and simultaneously delegates the metadata to the `history_manager.py` block, which logs the result persistently into a CSV file.
5.  **View Rendering:** Finally, Flask binds the results (disease class, confidence score, X-ray thumbnails, and precautions) to a dynamic UI template (`result.html` or `xray_result.html`) and serves it back to the client.

To visualize this conceptually:
```text
[User Browser] -> (Demographics + Symptoms/Images) -> [app.py (Flask Web Router)]
                                                              |
                                    +-------------------------+-------------------------+
                                    |                                                   |
                     [ DiseaseModelEngine (ML) ]                          [ xray_engine.py (Deep Learning) ] 
                     (Analyzes Symptom Vectors)                           (Classifies Pneumonia via CNNs)
                                    |                                                   |
                                    +-------------------------+-------------------------+
                                                              |
[history_manager.py] <--- [Logs Match Data + Confidence Metric] 
                                                              |
[result.html & xray_result.html] <--- [Applies Medical Precautions and Jinja Formatting]
                                                              |
[Final Display Rendered Back to User Browser]
```

## 3.2 Symptom-Based Disease Prediction Pipeline (Machine Learning)
The predictive symptom module heavily revolves around classic Machine Learning logic. Behind the scenes, the `model_engine.py` script loads a serialized (Pickle) model, commonly a fine-tuned **Random Forest Classifier**.
*   **Vectorization:** When a user selects a combination of symptoms on the UI, they pass as a list of strings to the backend. The engine compares these strings against the master `symptoms.json` dictionary. It parses out a $1 \times N$ binary NumPy array where a `1` indicates the presence of a symptom and a `0` indicates its absence.
*   **Prediction Generation:** The constructed vector is fed into the loaded Random Forest model. The model traverses its decision trees and outputs the highest probable class (e.g., "Influenza") along with a percentage-based confidence score derived from the tree branch probabilities.

## 3.3 Pneumonia Detection Pipeline from X-Ray Images (Deep Learning)
The system is capable of performing computer-aided detection (CAD) for pulmonary anomalies via the `xray_engine.py`. 
*   **Image Processing:** Users upload formats like PNG or JPEG. The file is securely saved utilizing `secure_filename` into a local `/uploads` directory configured via `path.py`.
*   **Inference:** The path to the saved image is passed to a Convolutional Neural Network (CNN). The CNN model converts the raw image into a fixed-size pixel tensor, scales the color channels appropriately, and executes forward propagation. It returns a binary classification result (indicating "Normal" or "Pneumonia"), a confidence percentage, and a warning message based on the severity.

## 3.4 Decoupled Engine Architecture
A core technical philosophy of the methodology is structural uncoupling. By instantiating a `DiseaseModelEngine` class, the application avoids hardcoding SciKit-Learn logic directly into web routing endpoints. 
*   This ensures the logic responsible for checking if the model is ready (`engine.is_ready()`), retrieving classes (`engine.get_symptoms()`), and evaluating predictions (`engine.predict()`) remains self-contained. 
*   If developers wish to transition from a Random Forest to an API-based LLM, or move from Flask to Django or FastAPI, the `model_engine.py` backend functions perfectly intact without necessitating a complete rewrite of the ML pipeline.

## 3.5 Persistent Patient Diagnostic History Tracking
A critical requirement of clinical software is non-volatile records. The architecture introduces `history_manager.py` handling simple but robust file I/O operations.
*   **Logging Flow:** After every successful diagnostic (both Symptom-based and X-Ray-based), `app.py` fires the `log_history()` method. It takes the session context (Patient Name, Predicted Output, Scan Type, and Confidence).
*   **CSV Mechanics:** This metadata is written seamlessly to a comma-separated values (CSV) log file equipped with a localized timestamp. 
*   **Audit Interface:** The system features a dedicated `/history` route which reads the latest state of the CSV and pipes it directly into the `history.html` template, rendering it as an HTML table acting as a persistent digital ledger for the session. An endpoint is also securely exposed to clear/flush this history as needed.

# 4. Data Collection and Preprocessing

## 4.1 Synthetic Dataset Generation (create_dataset.py)
To train the symptom-based predictive module, the project relies on a programmatically generated synthetic dataset. The `create_dataset.py` script constructs this data by mapping 11 distinct diseases (e.g., COVID-19, Influenza, Asthma, Pneumonia) to their clinical symptoms. For each iteration (generating 1,000 samples total), it selects a random subset of possible symptoms for a given illness. To make the model robust and mimic real-world ambiguity, it introduces a 5% statistical probability of adding "noise"—a random, unrelated symptom not typically associated with the target disease.

## 4.2 Chest X-Ray Image Dataset Preparation
The radiographic module utilizes a standard optical Chest X-Ray imagery dataset, structurally partitioned into distinct `train`, `test`, and `val` (validation) subdirectories. The dataset categorizes scans primarily into "Normal" (healthy lungs) and "Pneumonia" (lungs showing viral or bacterial infection opacity). This strict directory hierarchy establishes a standardized volumetric data structure required for automated loading via deep learning image generators. 

## 4.3 Data Cleaning & Normalization

### 4.3.1 Handling Class Imbalance
Medical datasets frequently suffer from classification imbalances. For the text-based disease modeling, the synthetic generation script inherently balances the dataset dynamically by uniformly random-sampling across the target diseases. For the image data, data augmentation strategies are applied holistically to ensure the Convolutional Neural Network (CNN) does not develop severe predictive biases toward the majority class (e.g., favoring Normal predictions over Pneumonia).

### 4.3.2 Outlier Detection
In the clinical text dataset, intentional statistical noise (randomized symptom injection) simulates outliers or misreported patient symptoms. During the training phase, the model's branching mechanisms naturally isolate these permutations, creating a more generalized decision boundary. For image datasets, corrupted or unreadable image files represent systemic outliers, emphasizing the need for input validation filtering during image pipeline execution.

## 4.4 Feature Engineering

### 4.4.1 Binary Vectorization for Symptoms
Machine learning models cannot directly interpret raw string-based lists. Therefore, feature engineering is actively applied to transform textual symptoms into a numerical array structure. The preprocessing pipeline extracts a master set of all unique clinical symptoms. When creating a patient record, it compiles a binary presence vector ($1 \times N$) in which each dimensional column correlates to a specific symptom (`1` if present, `0` if absent).

### 4.4.2 Image Augmentation Techniques
To maximize the deep neural network's accuracy given a finite X-ray dataset, extensive image augmentation is executed.
* **Pixel Normalization:** The raw multi-channel pixel intensities (varying from 0 to 255) are normalized to a consistent `0.0` to `1.0` scale, which optimizes numerical stability for gradient descent.
* **Geometric Augmentations:** Deep learning image generators dynamically alter the images in the training set during runtime by applying transformations like rotational shear, randomized zoom scaling, and horizontal flips. This computationally expands spatial variance, forcing the CNN to identify orientation-independent pulmonary features.

# 6. Results and Discussion

## 6.1 Symptom Checker Performance
The machine learning module responsible for symptom-based diagnosis demonstrated robust predictive capabilities. Trained primarily on the procedurally generated synthetic dataset using a Random Forest Classifier, the model successfully mapped high-dimensional binary symptom vectors to their respective disease classifications. During the validation phase, the classifier reliably achieved high accuracy. Its tree-based architecture inherently allowed it to handle the 5% statistical noise (outliers) injected during the dataset synthesis process without suffering from overfitting. The confidence percentages rendered on the frontend accurately reflect the model's probabilistic certainty, directly derived from the density of matching decision trees.

## 6.2 X-Ray Classification Accuracy
The Convolutional Neural Network (CNN) trained for computer-aided radiographic detection of pneumonia exhibited strong diagnostic potential. Benefiting significantly from pixel scaling and geometric data augmentation techniques, the deep learning model converged smoothly during gradient descent. When evaluated against the hold-out validation and test sets, the CNN yielded high metrics across precision, recall, and overall accuracy. It demonstrated a marked computational ability to discern opacities and anomalous fluid patterns characteristic of bacterial and viral pneumonia from standard, healthy pulmonary structures. The model yielded a minimal false-negative rate, which is a critical safety parameter in clinical diagnostic support systems.

## 6.3 Application UI Walkthrough
The DiagnoveraAI Pro interface successfully unifies these artificial intelligence engines under a single, cohesive user experience. 
* **Data Input:** Users are welcomed by a responsive screen allowing seamless toggling between text-based symptom selection and medical imagery file uploads. 
* **Real-time Processing:** Upon submission, the UI displays dynamic loading states while the Flask backend securely coordinates with the necessary predictive engine.
* **Diagnostic Report:** The application subsequently renders a dedicated results page. This display highlights the predicted condition, a clearly defined confidence gauge, and a set of actionable medical precautions. 
* **History Ledger:** All diagnostic interactions are natively committed to a persistent CSV ledger. The integrated `/history` interface allows medical practitioners or patients to securely review, audit, and optionally clear comprehensive logs of past diagnoses, establishing a high degree of clinical transparency.
