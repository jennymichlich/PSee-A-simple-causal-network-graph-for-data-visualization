import pandas as pd
import os

def load_tuebingen_pair(folder_path, file_name):
    """
    Grabs one of those specific pair files from the Tuebingen folder.
    
    This handles Issue #2. We are focused on just getting a two-variable 
    system loaded up so the algorithm has something to chew on.
    """
    # TODO: Find the specific text file in the folder
    # TODO: Load the two columns of data (Variable A and Variable B)
    # TODO: Return the data table

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
