import pandas as pd
import os

def load_data(filepath):
    """
    Load data from a CSV file.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None
    
    print(f"Loading data from {filepath}...")
    try:
        # Try reading with comment support for ThreatFox/URLHaus
        df = pd.read_csv(filepath, comment='#', on_bad_lines='skip')
        
        # Post-processing for KDD Cup 99 (sklearn fetch returns bytes)
        # Or if read_csv read them as strings looking like "b'val'"
        # Actually, if we saved it from sklearn df directly to CSV, it might have saved "b'normal.'" as the string.
        # Let's clean that up.
        
        def clean_bytes(x):
            if isinstance(x, str) and x.startswith("b'") and x.endswith("'"):
                return x[2:-1]
            return x

        # Apply to object columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(clean_bytes)

        print("Data loaded successfully.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def inspect_data(df):
    """
    Inspect the dataframe structure, columns, and basic stats.
    """
    if df is None:
        return

    print("\n--- Data Inspection ---")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nMissing Values:")
    print(df.isnull().sum().sum())

    if ' Label' in df.columns: # Note: CICIDS often has a space before Label
        print("\nLabel Distribution:")
        print(df[' Label'].value_counts())
    elif 'Label' in df.columns:
        print("\nLabel Distribution:")
        print(df['Label'].value_counts())
    else:
        print("\n'Label' column not found.")

if __name__ == "__main__":
    # Test with Monday dataset (usually normal traffic)
    filepath = r"p:\CODE-X\ThreatFusion\data\datasets\MachineLearningCSV\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"
    df = load_data(filepath)
    inspect_data(df)
