import pandas as pd
from pathlib import Path


def resolve_kdd_path() -> Path:
    repo_root = Path(__file__).resolve().parent
    default_path = repo_root / "data" / "datasets" / "Network Intrusion" / "kddcup99_10_percent.csv"
    return default_path


def main() -> None:
    csv_path = resolve_kdd_path()

    if not csv_path.exists():
        print("Dataset file not found.")
        print(f"Expected path: {csv_path}")
        print("Update the path in this script or place the CSV at the expected location.")
        return

    try:
        df = pd.read_csv(csv_path)
        print("Columns:", df.columns.tolist())
        print("First 5 rows:\n", df.head())
        print("Shape:", df.shape)
    except Exception as e:
        print(f"Error reading CSV: {e}")


if __name__ == "__main__":
    main()
