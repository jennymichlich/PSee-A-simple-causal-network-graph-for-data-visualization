import pandas as pd
import os

def load_tuebingen_pair(folder_path, file_name):
    """
    Loads a specific variable pair file from the Tuebingen dataset directory.
    
    Returns:
        pd.DataFrame: A two-column DataFrame ('A', 'B') containing the 
                      variable pair, or None if the file is missing.
    """

    full_path = os.path.join(folder_path, file_name)

    if not os.path.exists(full_path):
        print(f"ERROR: File not found at {full_path}")
        return None
        
    try:
        df = pd.read_csv(full_path, sep='\s+', header=None, names=['A', 'B'])
                
        return df
        
    except Exception as e:
        print(f"ERROR reading file {file_name}: {e}")
        return None
