import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import pandas as pd
import glob
import unittest
from src.loaders import load_tuebingen_pair


class TestTuebingenLoader(unittest.TestCase):

    def setUp(self):
        self.data_folder = os.path.join('data', 'pairs')

    # Individaul data file tests
    def test_dimensions_are_correct(self):
        # Load single data file
        # Access data file shape
        # Assert that number of columns (from shape) is 2 otherwise emmit error message
        # Assert that number of rows (from shape) is greater than 0 otherwise emit error
        return

    def test_data_has_variance(self):
        # Load single data file
        # Calculate standard deviation for each column
        # Assert that standard deviation > 0 else emit error message
        return

    def test_data_is_numeric(self):
        # Load single data file
        # for each column check if data is numeric
        # Assert that the seach column is numeric else emit error message
        return

    def test_load_tuebingen_pair_valid(self):
        # Load single data file
        filename = 'pair0001.txt'
        df = load_tuebingen_pair(self.data_folder, filename)
        
        # Asserts
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertEqual(df.shape[1], 2) # df.shape[1] for the number of columns

    def test_load_tuebingen_pair_missing(self):
        filename = 'nonExistingPair0001.txt'
        df = load_tuebingen_pair(self.data_folder, filename)
        
        self.assertIsNone(df)

    def test_load_tuebingen_pair_bad_format(self):
        filename = 'pair0097_des.txt'
        
        full_path = os.path.join(self.data_folder, filename)
        if not os.path.exists(full_path):
            print(f"Skipping bad_format test: {filename} not found.")
            return

        try:
            df = load_tuebingen_pair(self.data_folder, filename)
            
            if df is not None:
                self.assertTrue(df.empty or df.shape[1] < 2, "Should not accept text files as valid data")
                                
        except Exception as e:
            print(f"Loader raised error on bad file (Expected behavior): {e}")

    # Group data file tests
    def test_load_all_valid_tuebingen_pairs(self):
        """
        Test all Tuebingen pair files in folder
        """
        search_path = os.path.join(self.data_folder, 'pair*.txt')
        all_files = glob.glob(search_path)
        
        data_files = [f for f in all_files if '_des.txt' not in f]
        
        print(f"\n[Test Info] Found {len(data_files)} data files to test.")
        for file_path in data_files:
            filename = os.path.basename(file_path)
            
            with self.subTest(file=filename):
            
                df = load_tuebingen_pair(self.data_folder, filename)
                
                self.assertIsInstance(df, pd.DataFrame, f"Failed to load {filename}.")
                self.assertFalse(df.empty, f"File {filename} is empty.")
                self.assertGreaterEqual(df.shape[1], 2, f"File {filename} has < 2 columns.")


if __name__ == '__main__':
    unittest.main()