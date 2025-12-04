# 06_EDA.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

# terminal command to run script:
# python scripts/06_EDA.py \
#     --train_data_path=data/processed/train_data.csv

def load_data(path):
    return pd.read_csv(path)

@click.command()
@click.option('--train_data_path', type=str, required=True, help="Path to training data CSV")
def main(train_data_path):
    try:
        # Load train dataset
        train_df = load_data(train_data_path)

        # train_df.info() as text file
        buffer = StringIO()
        train_df.info(buf=buffer)
        os.makedirs("data/text", exist_ok=True)
        with open("data/text/train_df_info.txt", "w") as f:
            f.write(buffer.getvalue())
        print("Successfully saved train_df info to data/text as a text file")

        # plot: Count of Fake vs. Real News Articles
        counts = train_df['target'].value_counts().sort_index()
        plt.figure(figsize=(6, 1.5)) 
        plt.barh(counts.index, counts.values)
        plt.xlabel('Count')
        plt.ylabel('Label')
        plt.title('Count of true and fake news articles in training data')
        fig_path_1 = "img/fake_real_count.png"
        plt.tight_layout()
        plt.savefig(fig_path_1, dpi=300, bbox_inches="tight")
        print("Successfully saved fake_real_count.png to img/ folder")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()