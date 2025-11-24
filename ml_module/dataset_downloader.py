import os
import requests
import pandas as pd
from sklearn.datasets import fetch_kddcup99
import gzip
import shutil

DATASETS_DIR = r"p:\CODE-X\ThreatFusion\data\datasets"

def download_file(url, filepath):
    """Downloads a file from a URL to the specified path."""
    print(f"Downloading from {url}...")
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved to {filepath}")
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def fetch_kdd_cup_99():
    """Fetches KDD Cup 1999 dataset using sklearn."""
    print("\n--- Fetching KDD Cup 1999 Dataset ---")
    target_dir = os.path.join(DATASETS_DIR, "Network Intrusion")
    os.makedirs(target_dir, exist_ok=True)
    
    try:
        # fetch_kddcup99 downloads to scikit_learn_data by default, we can load it then save to CSV
        print("Fetching data via sklearn (this may take a moment)...")
        data = fetch_kddcup99(as_frame=True, percent10=True) # Download 10% version for speed
        df = data.frame
        
        output_path = os.path.join(target_dir, "kddcup99_10_percent.csv")
        df.to_csv(output_path, index=False)
        print(f"KDD Cup 1999 (10%) saved to {output_path}")
        print(f"Rows: {len(df)}")
    except Exception as e:
        print(f"Error fetching KDD Cup 99: {e}")

def fetch_phishing_data():
    """Fetches Phishing URLs from OpenPhish and PhishTank."""
    print("\n--- Fetching Phishing Datasets ---")
    target_dir = os.path.join(DATASETS_DIR, "Phishing")
    os.makedirs(target_dir, exist_ok=True)

    # 1. OpenPhish (Free Feed)
    openphish_url = "https://openphish.com/feed.txt"
    download_file(openphish_url, os.path.join(target_dir, "openphish_feed.txt"))

    # 2. PhishTank (might require user agent or API key, trying generic access)
    # Note: PhishTank CSV often requires a valid API key or session. 
    # We will try a public mirror or the direct link with a User-Agent.
    phishtank_url = "http://data.phishtank.com/data/online-valid.csv"
    # Sometimes this fails without an API key, but let's try.
    try:
        headers = {'User-Agent': 'ThreatFusion-Downloader/1.0'}
        response = requests.get(phishtank_url, headers=headers, stream=True, timeout=30)
        if response.status_code == 200:
            with open(os.path.join(target_dir, "phishtank_online_valid.csv"), 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("PhishTank data downloaded.")
        else:
            print(f"PhishTank download failed with status: {response.status_code} (API key might be required)")
    except Exception as e:
        print(f"PhishTank download error: {e}")

def fetch_threat_intel_data():
    """Fetches recent threat indicators from URLHaus."""
    print("\n--- Fetching Threat Intelligence Data ---")
    target_dir = os.path.join(DATASETS_DIR, "MalwareBazaar") # Reusing this dir for general malware intel
    os.makedirs(target_dir, exist_ok=True)

    # URLHaus Recent CSV
    urlhaus_url = "https://urlhaus.abuse.ch/downloads/csv_recent/"
    download_file(urlhaus_url, os.path.join(target_dir, "urlhaus_recent.csv"))

    # ThreatFox Recent IOCs
    threatfox_url = "https://threatfox.abuse.ch/export/csv/recent/"
    download_file(threatfox_url, os.path.join(target_dir, "threatfox_recent.csv"))

if __name__ == "__main__":
    print("Starting dataset downloads...")
    
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: 'requests' library is missing. Please run 'pip install requests'")
        exit(1)

    fetch_kdd_cup_99()
    fetch_phishing_data()
    fetch_threat_intel_data()
    
    print("\nDownload process completed.")
