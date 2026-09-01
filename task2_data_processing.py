import os
import glob
import json
import pandas as pd

def clean_data():
    # locate the JSON file in directory
    json_files = glob.glob("data/trends_*.json")
    if not json_files:
        print("Error: No JSON file found in data/ directory.")
        return

    input_file = json_files[0]
    print(f"Loading data from {input_file}...")

    # read json into Pandas dataframe
    df = pd.read_json(input_file)

    
    # Drop duplicates by post_id
    df = df.drop_duplicates(subset=["post_id"])

    # Clean missing values or null values
    df["title"] = df["title"].fillna("Untitled").astype(str).str.strip()
    df["author"] = df["author"].fillna("anonymous").astype(str)
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # ensure score and comments are not negative
    df["score"] = df["score"].apply(lambda x: max(0, x))
    df["num_comments"] = df["num_comments"].apply(lambda x: max(0, x))

    # export to CSV
    output_file = "data/cleaned_trends.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Data successfully cleaned and saved {len(df)} rows to {output_file}.")

if __name__ == "__main__":
    clean_data()
