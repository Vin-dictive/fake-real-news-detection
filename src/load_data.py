import pandas as pd
import os

def load_data(path: str):
    """
    Load data from a CSV file into a pandas DataFrame.

    Parameters
    ----------
    path : str
        Path to the CSV file to load.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the loaded data.
        
    Raises
    ------
    ValueError
        If the data filename does not end with '.csv', the CSV file is empty
        or the output dataframe has zero rows.
    FileNotFoundError
        If the file does not exist at the given path.
    """
    if not path.endswith(".csv"):
        raise ValueError("Data must be in CSV format")
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No file found at {path}")
    
    # Load the data from the .csv files
    try:
        data_df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError("CSV file is empty")
    except Exception as e:
        print(f"Unexpected error reading CSV: {e}")
    
    if data_df.empty:
        raise ValueError("CSV file contains no rows")
        
    return data_df