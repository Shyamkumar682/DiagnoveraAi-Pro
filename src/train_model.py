import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, precision_score, recall_score, f1_score, classification_report
import pickle
import os
import json
def check_overfitting(train_acc, test_acc, threshold=0.05):
    diff = train_acc - test_acc
    if diff > threshold:
        return "Overfitting"
    elif train_acc < 0.70 and test_acc < 0.70:
        return "Underfitting"
    else:
        return "Good Fit"
def main():
    print("=== Disease Diagnosis System Training ===")
    print("Loading dataset...")
    df = pd.read_csv('data/dataset.csv')
    df.dropna(inplace=True)
    X = df.drop(columns=['Disease'])
    y = df['Disease']
    symptoms = X.columns.tolist()
    print("Splitting data into 80% training and 20% testing...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print("\n--- Training Decision Tree ---")
    dt_params = {'max_depth': [None, 5, 10, 15], 'min_samples_split': [2, 5, 10]}
    dt_grid = GridSearchCV(DecisionTreeClassifier(random_state=42), dt_params, cv=5)
    dt_grid.fit(X_train, y_train)
    best_dt = dt_grid.best_estimator_
    dt_train_pred = best_dt.predict(X_train)
    dt_test_pred = best_dt.predict(X_test)
    dt_train_acc = accuracy_score(y_train, dt_train_pred)
    dt_test_acc = accuracy_score(y_test, dt_test_pred)
    print(f"Decision Tree Train Accuracy: {dt_train_acc:.3f}")
    print(f"Decision Tree Test Accuracy: {dt_test_acc:.3f}")
    print(f"Status: {check_overfitting(dt_train_acc, dt_test_acc)}")
    print("\n--- Training Random Forest ---")
    rf_params = {'n_estimators': [50, 100], 'max_depth': [None, 10, 20]}
    rf_grid = GridSearchCV(RandomForestClassifier(random_state=42), rf_params, cv=5)
    rf_grid.fit(X_train, y_train)
    best_rf = rf_grid.best_estimator_
    rf_train_pred = best_rf.predict(X_train)
    rf_test_pred = best_rf.predict(X_test)
    rf_train_acc = accuracy_score(y_train, rf_train_pred)
    rf_test_acc = accuracy_score(y_test, rf_test_pred)
    print(f"Random Forest Train Accuracy: {rf_train_acc:.3f}")
    print(f"Random Forest Test Accuracy: {rf_test_acc:.3f}")
    print(f"Status: {check_overfitting(rf_train_acc, rf_test_acc)}")
    print("\n--- Selecting Best Model ---")
    if rf_test_acc >= dt_test_acc:
        best_model = best_rf
        best_name = "Random Forest"
        best_test_acc = rf_test_acc
    else:
        best_model = best_dt
        best_name = "Decision Tree"
        best_test_acc = dt_test_acc
    print(f"Best Model Selected: {best_name} with Accuracy {best_test_acc:.3f}")
    print("\n--- Saving Model ---")
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(best_model, f)
    print("Saved to models/model.pkl")
    print("\n--- Saving Configuration ---")
    config_data = {
        'symptoms': symptoms,
        'classes': best_model.classes_.tolist()
    }
    with open('data/symptoms.json', 'w') as f:
        json.dump(config_data, f, indent=4)
    print("Saved to data/symptoms.json")
    log_data = pd.DataFrame([{
        'Model': 'Decision Tree', 'Train_Accuracy': dt_train_acc, 'Test_Accuracy': dt_test_acc, 'Fit_Status': check_overfitting(dt_train_acc, dt_test_acc)
    }, {
        'Model': 'Random Forest', 'Train_Accuracy': rf_train_acc, 'Test_Accuracy': rf_test_acc, 'Fit_Status': check_overfitting(rf_train_acc, rf_test_acc)
    }])
    log_data.to_csv('logs/training_logs.csv', index=False)
    print("Saved training logs to logs/training_logs.csv")
    print("\n--- Saving Advanced Metrics Report ---")
    y_pred_best = best_model.predict(X_test)
    precision = precision_score(y_test, y_pred_best, average='macro', zero_division=0)
    recall = recall_score(y_test, y_pred_best, average='macro', zero_division=0)
    f1 = f1_score(y_test, y_pred_best, average='macro', zero_division=0)
    report = classification_report(y_test, y_pred_best, zero_division=0)
    with open('reports/metrics_report.txt', 'w') as f:
        f.write(f"=== Advanced Metrics for {best_name} ===\n")
        f.write(f"Precision Score: {precision:.4f}\n")
        f.write(f"Recall Score: {recall:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n")
        f.write(f"\n=== Classification Report ===\n")
        f.write(report)
    print("Saved advanced metrics to reports/metrics_report.txt")
    print("\n--- Generating Visualizations ---")
    os.makedirs('static/graphs', exist_ok=True)
    plt.figure(figsize=(8, 5))
    models = ['Decision Tree', 'Random Forest']
    test_accs = [dt_test_acc, rf_test_acc]
    plt.bar(models, test_accs, color=['#4CAF50', '#2196F3'])
    plt.title('Model Accuracy Comparison')
    plt.ylabel('Test Accuracy')
    plt.ylim([0, 1.1])
    for i, v in enumerate(test_accs):
        plt.text(i, v + 0.02, f"{v:.3f}", ha='center')
    plt.savefig('static/graphs/accuracy_comparison.png')
    plt.close()
    plt.figure(figsize=(8, 5))
    x = np.arange(2)
    width = 0.35
    train_accs = [dt_train_acc, rf_train_acc]
    plt.bar(x - width/2, train_accs, width, label='Train', color='#FF9800')
    plt.bar(x + width/2, test_accs, width, label='Test', color='#9C27B0')
    plt.xticks(x, models)
    plt.title('Training vs Testing Accuracy')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.ylim([0, 1.1])
    plt.savefig('static/graphs/train_test_accuracy.png')
    plt.close()
    plt.figure(figsize=(12, 10))
    y_pred_best = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best, labels=best_model.classes_)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=best_model.classes_)
    fig, ax = plt.subplots(figsize=(10,10))
    disp.plot(cmap='Blues', xticks_rotation='vertical', ax=ax)
    plt.title(f'Confusion Matrix - {best_name}')
    plt.tight_layout()
    plt.savefig('static/graphs/confusion_matrix.png')
    plt.close('all')
    plt.figure(figsize=(8, 5))
    cv_scores = cross_val_score(best_model, X_train, y_train, cv=5)
    plt.plot(range(1, 6), cv_scores, marker='o', linestyle='--', color='#E91E63')
    plt.title(f'5-Fold Cross Validation Scores - {best_name}')
    plt.xlabel('Fold Number')
    plt.ylabel('Accuracy')
    plt.ylim([0, 1.1])
    plt.xticks(range(1, 6))
    plt.savefig('static/graphs/cv_scores.png')
    plt.close()
    plt.figure(figsize=(8, 5))
    train_sizes, train_scores, validation_scores = learning_curve(
        estimator=best_model,
        X=X_train, y=y_train, train_sizes=np.linspace(0.1, 1.0, 5), cv=5,
        scoring='accuracy'
    )
    train_scores_mean = train_scores.mean(axis=1)
    validation_scores_mean = validation_scores.mean(axis=1)
    plt.plot(train_sizes, train_scores_mean, label='Training score', color='#FF9800', marker='o')
    plt.plot(train_sizes, validation_scores_mean, label='Cross-validation score', color='#4CAF50', marker='o')
    plt.ylabel('Accuracy')
    plt.xlabel('Training Set Size')
    plt.title(f'Learning Curve - {best_name}')
    plt.legend(loc='lower right')
    plt.ylim([0, 1.1])
    plt.savefig('static/graphs/learning_curve.png')
    plt.close()
    plt.figure(figsize=(10, 6))
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1][:10]
        top_symptoms = [symptoms[i] for i in indices]
        top_importances = importances[indices]
        plt.barh(top_symptoms[::-1], top_importances[::-1], color='#2ed573')
        plt.xlabel('Relative Importance')
        plt.title(f'Top 10 Key Symptoms - {best_name}')
        plt.tight_layout()
        plt.savefig('static/graphs/feature_importance.png')
    plt.close()
    print("Visualizations saved in static/graphs/ :")
    print(" - accuracy_comparison.png")
    print(" - train_test_accuracy.png")
    print(" - confusion_matrix.png")
    print(" - cv_scores.png")
    print(" - learning_curve.png")
    print(" - feature_importance.png")
    print("\nTraining Phase Complete! Run 'python app.py' to start the web app.")
if __name__ == "__main__":
    main()
