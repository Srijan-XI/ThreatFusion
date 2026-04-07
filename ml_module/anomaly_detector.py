import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os
from pathlib import Path

class AnomalyDetector:
    def __init__(self, model_type='rf'):
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.encoders = {} # Dictionary to store LabelEncoders for each categorical column
        self.feature_columns = None

    def preprocess(self, df, is_training=True):
        """
        Preprocess the dataframe: clean columns, handle NaNs, encode categoricals, scale features.
        """
        # Clean column names
        df.columns = df.columns.str.strip()
        
        # Drop rows with infinite or missing values
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)

        # Identify Target Column
        target_col = None
        if 'Label' in df.columns:
            target_col = 'Label'
        elif 'labels' in df.columns:
            target_col = 'labels'

        # Separate features and target
        if target_col:
            X = df.drop(target_col, axis=1)
            y = df[target_col]
        else:
            print(f"Warning: Target column 'Label' or 'labels' not found. Available columns: {df.columns.tolist()}")
            X = df
            y = None

        # Handle Categorical Columns
        # We need to encode string columns to numbers
        object_cols = X.select_dtypes(include=['object']).columns.tolist()
        
        if is_training:
            self.feature_columns = X.columns.tolist()
            for col in object_cols:
                le = LabelEncoder()
                # Convert to string to ensure uniformity
                X[col] = le.fit_transform(X[col].astype(str))
                self.encoders[col] = le
        else:
            # Ensure columns match training
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0 
            X = X[self.feature_columns]
            
            # Encode using saved encoders
            for col in object_cols:
                if col in self.encoders:
                    le = self.encoders[col]
                    # Handle unseen labels by mapping them to a default or -1
                    # Simple approach: map known, fill unknown with -1
                    X[col] = X[col].astype(str).map(lambda s: le.transform([s])[0] if s in le.classes_ else -1)
                else:
                    # If we didn't see this column in training but it's here now (shouldn't happen due to feature_columns check)
                    X[col] = 0

        # Scale features
        # Ensure all data is numeric now
        X = X.apply(pd.to_numeric, errors='coerce').fillna(0)
        
        if is_training:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)

        return X_scaled, y

    def train(self, df):
        print(f"Training {self.model_type} model...")
        X, y = self.preprocess(df, is_training=True)

        if self.model_type == 'rf':
            # Random Forest (Supervised)
            self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
            self.model.fit(X, y)
            print("Random Forest training complete.")
            
        elif self.model_type == 'if':
            # Isolation Forest (Unsupervised)
            self.model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42, n_jobs=-1)
            self.model.fit(X)
            print("Isolation Forest training complete.")

    def evaluate(self, df):
        print("Evaluating model...")
        X, y = self.preprocess(df, is_training=False)
        
        if self.model_type == 'rf':
            y_pred = self.model.predict(X)
            print("\nClassification Report:")
            # Use unique labels present in y and y_pred to avoid errors
            print(classification_report(y, y_pred))
            
        elif self.model_type == 'if':
            y_pred = self.model.predict(X)
            print("Predictions (1=Normal, -1=Anomaly):")
            print(pd.Series(y_pred).value_counts())
            
            if y is not None:
                # Heuristic to determine "Normal" label from dataset
                # CICIDS: 'BENIGN'
                # KDD: 'normal.'
                
                y_true_binary = []
                for label in y:
                    label_str = str(label).lower()
                    if 'benign' in label_str or 'normal' in label_str:
                        y_true_binary.append(1)
                    else:
                        y_true_binary.append(-1)
                
                print("\nAccuracy (assuming Normal/Benign=1, Others=-1):")
                print(accuracy_score(y_true_binary, y_pred))

    def save_model(self, filepath):
        if self.model:
            joblib.dump({
                'model': self.model, 
                'scaler': self.scaler, 
                'encoders': self.encoders,
                'features': self.feature_columns, 
                'type': self.model_type
            }, filepath)
            print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        if os.path.exists(filepath):
            data = joblib.load(filepath)
            self.model = data['model']
            self.scaler = data['scaler']
            self.encoders = data.get('encoders', {})
            self.feature_columns = data['features']
            self.model_type = data['type']
            print(f"Model loaded from {filepath}")
        else:
            print(f"Model file not found: {filepath}")

if __name__ == "__main__":
    # Example usage
    from data_loader import load_data
    
    # Test with KDD Cup 99
    repo_root = Path(__file__).resolve().parents[1]
    filepath = str(repo_root / "data" / "datasets" / "Network Intrusion" / "kddcup99_10_percent.csv")
    df = load_data(filepath)
    
    if df is not None:
        # Sample for speed
        df_sample = df.sample(frac=0.1, random_state=42) 
        
        # Train Random Forest
        detector_rf = AnomalyDetector(model_type='rf')
        detector_rf.train(df_sample)
        detector_rf.evaluate(df_sample)
        detector_rf.save_model("rf_kdd_model.pkl")
