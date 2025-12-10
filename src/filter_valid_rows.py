import pandas as pd

def filter_valid_rows(train_data: pd.DataFrame) -> pd.DataFrame:
    """
    Filter out invalid rows from the training dataset based on the following conditions:
    - Rows where the 'text' length is less than 20 characters should be removed
    - Rows with invalid or missing 'date' values should be removed

    Parameters
    ----------
    train_data : pd.DataFrame
        The training dataset.

    Returns
    -------
    pd.DataFrame
        Filtered dataset containing only valid rows.
    
    Raises
    ------
    TypeError
        If input is not a pandas DataFrame.
    ValueError
        If required columns 'text' and 'date' are missing or if no valid rows remain.
    """
    # Check if input is a Dataframe
    if not isinstance(train_data, pd.DataFrame):
        raise TypeError("Input must be a pandas Dataframe")
    
    # Check that Dataframe has required columns
    if "text" not in set(train_data.columns):
        raise ValueError("Missing required 'text' column in input data")
    if "date" not in set(train_data.columns):
        raise ValueError("Missing required 'date' column in input data")
    
    try:
        train_data = train_data[train_data['text'].str.len() >= 20]
        train_data = train_data[pd.to_datetime(train_data['date'],
                                               format='mixed',
                                               errors='coerce').notna()]
    except Exception as e:
        print(f"Error filtering rows: {e}")
        
    if train_data.empty:
        raise ValueError("No valid rows remaining")
    
    return train_data
