# 10. Appendices

## Appendix A: Technology Stack and Environment Setup

This section outlines the technology stack and the development environment setup required for DiagnoveraAI Pro. It describes the dependencies, frameworks, and libraries utilized throughout the project.

### A.1 Core Technologies Map
- **Programming Language**: Python 3.x
- **Web Framework**: Flask 3.1.3 (Serves as the backend for the application and API endpoints)
- **Frontend Technologies**: HTML5, CSS3, Vanilla JavaScript, Jinja2 (Flask Templating)
- **Data Persistence**: CSV-based storage (for Patient History mapping and System Database)

### A.2 Machine Learning & Data Science Libraries
- **scikit-learn (1.6.1)**: Used for traditional machine learning algorithms (Decision Trees, Random Forests) applied in symptom-based predictions.
- **pandas (2.2.3)**: Essential for robust data manipulation, structured data processing, CSV file operations, and creating DataFrame matrices for the dataset.
- **numpy (2.1.0)**: Used for numerical computations, multi-dimensional array operations, and mathematical parsing crucial to machine learning and deep learning algorithms.

### A.3 Deep Learning & Computer Vision Libraries
- **TensorFlow & Keras**: Frameworks used to design, train, and execute the Convolutional Neural Networks (CNN) for Chest X-Ray diagnostic models.
- **opencv-python**: Employed for medical image reading, conversion, normalization, and resizing, formatting raw X-Ray/CT scans before they are fed into the neural network classification models.

### A.4 Additional Dependencies
- **matplotlib (3.10.3)**: Utilized for plotting analytical data, graphing learning curves (Loss/Accuracy distributions), and visualizing prediction arrays.
- **Werkzeug**: Flask's underlying WSGI comprehensive web application library for HTTP utilities, request handling, and secure file uploads.

### A.5 Environment Setup Guide
To effectively establish a localized development environment:

1. **Prerequisites**: Ensure Python 3.x is globally accessible on your local system path.
2. **Virtual Environment Initialization**:
   Create a virtual environment to avoid global dependency footprinting.
   ```bash
   python -m venv venv
   ```
   *Activation on Windows:*
   ```bash
   venv\Scripts\activate
   ```
   *Activation on macOS/Linux:*
   ```bash
   source venv/bin/activate
   ```
3. **Core Dependency Installation**:
   Install required packages via the project's standard requirements document:
   ```bash
   pip install -r requirements.txt
   ```

---

## Appendix B: Deployment / Instructions to Run the Application

This unit encapsulates the execution procedure, operating prerequisites, and web startup for the diagnostic application.

### B.1 Project File Setup Structure
Prior to launch, verify that the project data models are correctly situated:
- Trained machine learning weights and models for predictive diagnostics must be available and accurately located per `path.py` configuration.
- Chest X-Ray image generation or classification weights must be reachable by the backend engine dependencies.
- Frontend structural directories (`/templates` and `/static`) must remain at the root alongside `app.py`.

### B.2 Execution Protocol
1. Launch your command-line interface (e.g., Terminal, PowerShell, or VS Code terminal).
2. Configure the working directory context to the project's root level where `app.py` is located.
3. Validate that your Python virtual environment (configured in B.1) is actively running.
4. Execute the web application script:
   ```bash
   python app.py
   ```

### B.3 Application Access
Once properly initialized without package loading failures, the Flask WSGI instance will bind and serve locally to the default port interface.
- Open a modern graphical web browser (e.g., Google Chrome, Firefox, Microsoft Edge).
- Navigate directly to the host loopback IP: [http://127.0.0.1:5000](http://127.0.0.1:5000) or [http://localhost:5000](http://localhost:5000)

### B.4 Basic Troubleshooting Steps
- **Address Already in Use / Port Conflicts**: If port 5000 is intercepted by native operating system services (e.g., Control Center on macOS), modifying the execution parameters in `app.py` to `app.run(port=5001)` or similar alternative port configurations will bypass the network overlap.
- **File Path Resolution / Model Loading Errors**: Examine console tracebacks if a `FileNotFoundError` emerges. Ensure that dataset directories, history CSV files, and ML model outputs precisely map via the defined routing in `path.py` pointing correctly to root machine pathways.
