import pandas as pd
import numpy as np

def analyze_data():
    # 1. load clean data
    csv_file = "data/cleaned_trends.csv"
    if not pd.io.common.file_exists(csv_file):
        print(f"Error: {csv_file} does not exist. Run Task 2 first.")
        return

    df = pd.read_csv(csv_file)

    # group Analysis using Pandas
    category_summary = df.groupby("category").agg(
        total_posts=("post_id", "count"),
        total_score=("score", "sum"),
        avg_score=("score", "mean"),
        avg_comments=("num_comments", "mean")
    ).reset_index()

    
    scores = df["score"].to_numpy()
    comments = df["num_comments"].to_numpy()

    # avoid division by zero with np
    engagement_ratio = np.where(scores > 0, comments / scores, 0)
    df["engagement_ratio"] = np.round(engagement_ratio, 2)

    # Top author
    top_author = df["author"].mode()[0] if not df["author"].empty else "None"

    # display analysed Output
    print("================ TRENDPULSE DATA SUMMARY ================")
    print(f"Total Stories Analyzed : {len(df)}")
    print(f"Most Frequent Author   : {top_author}")
    print("\n--- Summary By Category ---")
    print(category_summary.to_string(index=False))
    print("========================================================")

if __name__ == "__main__":
    analyze_data()
