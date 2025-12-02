# 00_download_data.py
# author: Vinay Valson
# date: 2025-12-02

import click
import os
import zipfile
import requests


@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write_to', type=str, help="Path to directory where raw data will be written to")
def main(url, write_to):
    """Downloads data zip data from the web to a local filepath and extracts it."""
    try:
        read_zip(url, write_to)
    except:
        os.makedirs(write_to)
        read_zip(url, write_to)

if __name__ == '__main__':
    main()