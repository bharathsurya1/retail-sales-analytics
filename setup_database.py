from pathlib import Path
import sqlite3

import pandas as pd


# Locate files relative to this script
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "superstore.csv"
DB_PATH = BASE_DIR / "data" / "superstore.db"


def main():
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}\n"
            "Download the dataset using the instructions in README.md."
        )

    # Load the source dataset
    df = pd.read_csv(CSV_PATH)

    # Recreate the database table from the source CSV
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("orders", conn, if_exists="replace", index=False)

    print("Database setup completed successfully!")
    print(f"Rows imported: {len(df):,}")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    main()