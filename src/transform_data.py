import pandas as pd

def transform_data(true_df: pd.DataFrame, fake_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and transform the raw true and fake news DataFrames.
    - Adds a 'target' column to distinguish True vs. Fake articles.
    - Standardizes the 'subject' column into two categories: 'political' or 'non-political'.
    - Concatenates the two DataFrames into one complete dataset.

    Parameters
    ----------
    true_df : pd.DataFrame
        DataFrame containing true news articles.
    fake_df : pd.DataFrame
        DataFrame containing fake news articles.

    Returns
    -------
    pd.DataFrame
        Combined and transformed DataFrame.
        
    Raises
    ------
    TypeError
        If the inputs are not pandas Dataframes,
    ValueError
        If 'subject' is not a column in the input Dataframes or if the
        resulting Dataframe is empty    
    """
    # Check that inputs are Dataframes
    if not isinstance(true_df, pd.DataFrame):
        raise TypeError("true_df must be a pandas Dataframe")
    if not isinstance(fake_df, pd.DataFrame):
        raise TypeError("fake_df must be a pandas Dataframe")
    
    # Check that true_df and fake_df have the 'subject' column
    if "subject" not in set(true_df.columns):
        raise ValueError("true_df is missing the 'subject' column")
    if "subject" not in set(fake_df.columns):
        raise ValueError("fake_df is missing the 'subject' column")
    
    try:
        # Create new 'target' columns true_df and fake_df
        true_df['target'] = 'True'
        fake_df['target'] = 'Fake'
    
        # Transform 'subject' columns so that they are consistenly in one of two categories: political or non-political
        true_df['subject'] = true_df['subject'].replace('politicsNews', 'political')
        true_df['subject'] = true_df['subject'].replace('worldnews', 'non-political')
        fake_df['subject'] = fake_df['subject'].replace('politics', 'political')
        fake_df['subject'] = fake_df['subject'].replace('left-news', 'political')
        fake_df['subject'] = fake_df['subject'].replace('Government News', 'political')
        fake_df['subject'] = fake_df['subject'].replace('News', 'non-political')
        fake_df['subject'] = fake_df['subject'].replace('US_News', 'non-political')
        fake_df['subject'] = fake_df['subject'].replace('Middle-east', 'non-political')
    
        # Combine true_df and fake_df into a complete dataset
        complete_df = pd.concat([true_df, fake_df])
        
    except Exception as e:
        print(f"Error during data transformation: {e}")
    
    if complete_df.empty:
        raise ValueError("Combined dataset is empty after transformations")
    
    return complete_df