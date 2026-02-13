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
        df = pd.read_csv(full_path, sep='\s+', header=None, names=['A', 'B'])
                
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