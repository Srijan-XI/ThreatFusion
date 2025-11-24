# ML Module

This module implements Machine Learning based anomaly detection for ThreatFusion.

## Components

- `data_loader.py`: Handles loading and inspecting CSV datasets (specifically CICIDS2017 format).
- `anomaly_detector.py`: Contains the `AnomalyDetector` class which supports:
    - **Random Forest (rf)**: Supervised classification.
    - **Isolation Forest (if)**: Unsupervised anomaly detection.

## Usage

### Training a Model

```python
from ml_module.data_loader import load_data
from ml_module.anomaly_detector import AnomalyDetector

# Load data
df = load_data("path/to/dataset.csv")

# Train Random Forest
detector = AnomalyDetector(model_type='rf')
detector.train(df)
detector.save_model("rf_model.pkl")
```

### Loading and Predicting

```python
detector = AnomalyDetector()
detector.load_model("rf_model.pkl")

# Predict on new data (df)
detector.evaluate(new_df)
```

## Datasets

The module is designed to work with the following datasets located in `data/datasets`:

- **CICIDS2017**: Network traffic analysis (in `MachineLearningCSV`).
- **KDD Cup 1999**: Intrusion detection dataset (in `Network Intrusion`).
- **PhishTank / OpenPhish**: Phishing URLs (in `Phishing`).
- **URLHaus / ThreatFox**: Malware URLs and IOCs (in `MalwareBazaar`).

You can download/update these datasets using:
```bash
python ml_module/dataset_downloader.py
```
