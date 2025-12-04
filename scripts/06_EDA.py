# 06_EDA.py
# author: Jessie Liang
# date: 2025-12-03

import click
import os
import pandas as pd
from io import StringIO

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

        # train_df information
        buffer = StringIO()
        train_df.info(buf=buffer)
        os.makedirs("data/text", exist_ok=True)
        with open("data/text/train_df_info.txt", "w") as f:
            f.write(buffer.getvalue())
        print("Successfully saved train_df info to data/text as a text file")

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()