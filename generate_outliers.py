"""
=============================================================================
Outlier Detection and Visualization Script
=============================================================================

Instructions for use:
1. Ensure your dataset is located at: `data/dataset.csv`
2. Run this script from the terminal using: `python generate_outliers.py`
3. The script will automatically create a `static/graphs/` directory.
4. Check the `static/graphs/` directory for the generated visualizations.

Dependencies:
- pandas (for data manipulation)
- matplotlib (for plotting)
- seaborn (for advanced plotting)
Install them via: `pip install pandas matplotlib seaborn` if not already installed.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_outlier_graphs():
    """
    Main function to read the dataset, calculate outlier metrics, and save visualizations.
    """
    # Define the directory where the output graphs will be saved
    graphs_dir = os.path.join('static', 'graphs')
    
    # Create the directory if it doesn't already exist (exist_ok=True prevents errors if it does)
    os.makedirs(graphs_dir, exist_ok=True)
    
    # Define the path to the dataset
    data_path = os.path.join('data', 'dataset.csv')
    
    # Check if the dataset exists before proceeding
    if not os.path.exists(data_path):
        print(f"Error: Dataset not found at {data_path}. Please ensure the file exists.")
        return
        
    # Read the dataset into a pandas DataFrame
    df = pd.read_csv(data_path)
    
    # -------------------------------------------------------------------------
    # DATA PREPARATION
    # -------------------------------------------------------------------------
    # Since the dataset consists of binary symptom flags (0 = No, 1 = Yes), 
    # traditional outlier detection on individual columns isn't meaningful. 
    # Instead, we detect outliers based on aggregate metrics.
    
    # Remove the 'Disease' target column if it exists so we only analyze symptoms
    if 'Disease' in df.columns:
        features = df.drop('Disease', axis=1)
    else:
        features = df
        
    # -------------------------------------------------------------------------
    # METRIC 1: Outliers in Number of Symptoms per Patient
    # -------------------------------------------------------------------------
    # Calculate the total number of symptoms reported by each individual patient (row-wise sum)
    symptoms_per_record = features.sum(axis=1)
    
    # Create a boxplot to identify patients with an abnormally high or low number of symptoms
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=symptoms_per_record, color='skyblue')
    plt.title('Outliers Detection: Number of Symptoms per Patient')
    plt.xlabel('Total Symptoms Reported')
    plt.tight_layout() # Adjusts layout to prevent clipping of titles/labels
    # Save the plot to the graphs directory
    plt.savefig(os.path.join(graphs_dir, 'outliers_symptoms_per_patient_boxplot.png'))
    plt.close() # Close the figure to free up memory
    
    # Create a histogram to show the overall distribution of symptoms per patient
    plt.figure(figsize=(10, 6))
    sns.histplot(symptoms_per_record, bins=15, kde=True, color='coral')
    plt.title('Distribution of Number of Symptoms per Patient')
    plt.xlabel('Total Symptoms Reported')
    plt.ylabel('Number of Patients')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'distribution_symptoms_per_patient.png'))
    plt.close()
    
    # -------------------------------------------------------------------------
    # METRIC 2: Outliers in Symptom Frequencies
    # -------------------------------------------------------------------------
    # Calculate how many times each specific symptom appears across the entire dataset (column-wise sum)
    symptom_freq = features.sum(axis=0)
    
    # Create a boxplot to identify symptoms that are abnormally common or rare
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=symptom_freq, color='lightgreen')
    plt.title('Outliers Detection: Frequency of Individual Symptoms')
    plt.xlabel('Frequency across all records')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'outliers_symptom_frequencies_boxplot.png'))
    plt.close()
    
    # Create a horizontal bar chart showing the top 15 most frequently reported symptoms
    plt.figure(figsize=(12, 8))
    # Sort values in ascending order and take the last 15 to get the top 15
    symptom_freq.sort_values().tail(15).plot(kind='barh', color='teal')
    plt.title('Top 15 Most Common Symptoms')
    plt.xlabel('Frequency')
    plt.tight_layout()
    plt.savefig(os.path.join(graphs_dir, 'top_15_symptoms.png'))
    plt.close()

    # Print success message to terminal
    print(f"Success! Outlier graphs have been generated and saved in the '{graphs_dir}' directory.")

# Standard Python boilerplate to ensure the main code only runs when executed directly
if __name__ == "__main__":
    create_outlier_graphs()
