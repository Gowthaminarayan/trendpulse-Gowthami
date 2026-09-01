import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_visualizations():
    csv_file = "data/cleaned_trends.csv"
    if not os.path.exists(csv_file):
        print("Error: Cleaned CSV file not found.")
        return

    df = pd.read_csv(csv_file)

    # Set up matplotlib figure with 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Average Score per Category
    avg_scores = df.groupby("category")["score"].mean()
    avg_scores.plot(kind="bar", ax=axes[0], color="skyblue", edgecolor="black")
    axes[0].set_title("Average Score by Category")
    axes[0].set_xlabel("Category")
    axes[0].set_ylabel("Average Score (Upvotes)")
    axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Score vs Number of Comments Scatter Plot
    axes[1].scatter(df["score"], df["num_comments"], alpha=0.6, color="coral")
    axes[1].set_title("Score vs. Number of Comments")
    axes[1].set_xlabel("Score (Upvotes)")
    axes[1].set_ylabel("Number of Comments")

    plt.tight_layout()

    # Save chart image to data/ folder
    output_image = "data/trends_plot.png"
    plt.savefig(output_image)
    print(f"Visualizations saved successfully to {output_image}")

if __name__ == "__main__":
    generate_visualizations()