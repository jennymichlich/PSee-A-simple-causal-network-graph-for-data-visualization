import pandas as pd
import os
import glob


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
        df = pd.read_csv(full_path, sep=r'\s+', header=None, names=['A', 'B'])
                
        return df
        
    except Exception as e:
        print(f"ERROR reading file {file_name}: {e}")
        return None


def get_ground_truth(data_folder, pair_filename):
    """
    Parses the description file to extract the ground truth direction.
    Returns: 'A --> B', 'B --> A', or 'Unknown'
    """
    base_name = pair_filename.split('.')[0]
    des_filename = f"{base_name}_des.txt"
    file_path = os.path.join(data_folder, des_filename)
    
    if not os.path.exists(file_path):
        return "Unknown"

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if "x --> y" in content or "x -> y" in content:
            return "A --> B"
        elif "y --> x" in content or "y -> x" in content:
            return "B --> A"
        elif "x --- y" in content:
            return "Ind/Confounder"
        else:
            return "Unknown"
            
    except Exception:
        return "Error"


def get_all_ground_truths(data_folder):
    """
    Scans the folder and extracts ground truth for all pair files.
    Returns a dictionary: {'pair0001.txt': 'A --> B', ...}
    """
    ground_truths = {}
    search_path = os.path.join(data_folder, 'pair*.txt')
    files = glob.glob(search_path)
    
    for file_path in files:
        filename = os.path.basename(file_path)
        
        if '_des.txt' in filename:
            continue
            
        truth = get_ground_truth(data_folder, filename)
        ground_truths[filename] = truth
        
    return ground_truths


def load_causal_data(folder_path, filename):
    """
    INTENT: Robustly loads causal data by automatically detecting separators and headers.
    Current data sets have file extension .csv and .txt. This function is file extension agnostic.
    This function is an evolution of the function 'load_tuebingen_pair'. The original function remains
    because we wish to keep the history of this project.
    """

    file_path = os.path.join(folder_path, filename)

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None

    try:
        # We use the try except construct to avoid code crashes.
        # The logic for testing the different formats that data might be in goes in the try section
        # As far as we can determine upfront the logic should prevent crashes.

        # Use sep=None with engine='python' to automatically detect the delimiter.
        # We first read just the column names to check if a header row exists.
        sample = pd.read_csv(file_path, sep=None, engine='python', nrows=0)

        # Check if the 'header' columns are actually numeric data.
        # If all column labels can be converted to numbers, the file likely lacks a header.
        is_numeric_header = pd.to_numeric(sample.columns, errors='coerce').notnull().all()

        # Intent: We avoid hard coding the 'header' parameter so the loader can dynamically
        # transition between benchmark datasets (no headers) and synthetic CSV exports (with headers).
        if is_numeric_header:
            df = pd.read_csv(file_path, sep=None, engine='python', header=None)
        else:
            df = pd.read_csv(file_path, sep=None, engine='python')

        # Standardize column names to A, B, C...
        # Intent: This ensures that downstream causal algorithms can reference nodes consistently,
        # regardless of whether the source file used 'X,Y' or 'V1,V2'.
        df.columns = [chr(65 + i) for i in range(df.shape[1])]

        # Ensure all data is numeric and remove rows with missing values to prevent statistical test failures.
        return df.apply(pd.to_numeric, errors='coerce').dropna()

    except Exception as e:
        print(f"An error occurred while loading {filename}: {e}")
        return None
