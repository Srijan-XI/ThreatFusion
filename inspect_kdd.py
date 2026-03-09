import pandas as pd
import os

filepath = r"p:\CODE-X\ThreatFusion\data\datasets\Network Intrusion\kddcup99_10_percent.csv"
try:
    df = pd.read_csv(filepath)
    print("Columns:", df.columns.tolist())
    print("First 5 rows:\n", df.head())
    print("Shape:", df.shape)
except Exception as e:
    print(f"Error: {e}")
