import os
import glob
import pandas as pd
from ml_module.data_loader import load_data
from ml_module.anomaly_detector import AnomalyDetector

def train_on_all_datasets(base_dir, model_output_dir="models"):
    if not os.path.exists(model_output_dir):
        os.makedirs(model_output_dir)

    # Find all CSV files recursively, but exclude non-training datasets
    csv_files = []
    exclude_dirs = ['MalwareBazaar', 'Phishing', 'download']
    
    for root, dirs, files in os.walk(base_dir):
        # Skip excluded directories
        if any(ex_dir in root for ex_dir in exclude_dirs):
            continue
            
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    
    if not csv_files:
        print("No CSV files found.")
        return

    print(f"Found {len(csv_files)} datasets.")

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        print(f"\nProcessing {filename}...")
        
        # Skip if model already exists
        model_name = f"rf_{filename.replace('.csv', '')}.pkl"
        save_path = os.path.join(model_output_dir, model_name)
        
        if os.path.exists(save_path):
             print(f"Model {model_name} already exists. Skipping.")
             continue

        df = load_data(filepath)
        if df is None:
            continue

        # Sample if too large (e.g., > 200k rows for speed)
        if len(df) > 200000:
            print("Dataset too large, sampling 200k rows...")
            df = df.sample(n=200000, random_state=42)

        # Train Random Forest
        detector = AnomalyDetector(model_type='rf')
        detector.train(df)
        # detector.evaluate(df) # Skip eval for batch training to save time/output
        detector.save_model(save_path)
        
        # Clear memory
        del df
        del detector

if __name__ == "__main__":
    data_dir = r"p:\CODE-X\ThreatFusion\data\datasets"
    train_on_all_datasets(data_dir)
