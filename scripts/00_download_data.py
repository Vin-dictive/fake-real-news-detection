# 00_download_data.py
# author: Vinay Valson
# date: 2025-12-02

import click
import os

import requests
from pathlib import Path


def download_csv(url, write_to):
    """Download CSV file from URL to specified directory."""
    response = requests.get(url)
    response.raise_for_status()
    
    # Extract filename from URL or use default
    filename = url.split('/')[-1]
    if not filename.endswith('.csv'):
        filename = 'data.csv'
    
    # Write CSV file
    csv_path = os.path.join(write_to, filename)
    with open(csv_path, 'wb') as f:
        f.write(response.content)


@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write_to', type=str, help="Path to directory where raw data will be written to")
def main(url, write_to):
    """Downloads CSV data from the web to a local filepath."""
    # Create directory if it doesn't exist
    Path(write_to).mkdir(parents=True, exist_ok=True)
    
    try:
        download_csv(url, write_to)
        print(f"Successfully downloaded CSV to {write_to}")
    except Exception as e:
        print(f"Error downloading data: {e}")

if __name__ == '__main__':
    main()