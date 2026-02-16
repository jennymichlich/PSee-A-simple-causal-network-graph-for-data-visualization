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
        current_test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_test_dir)
        self.data_folder = os.path.join(project_root, 'data', 'pairs')

    # Individaul data file tests
    def test_dimensions_are_correct(self):
        # Load single data file
        filename = 'pair0001.txt'
        df = load_tuebingen_pair(self.data_folder, filename)
        # Access data file shape
        rows, cols = df.shape
        # Assert that number of columns (from shape) is 2 otherwise emmit error message
        self.assertEqual(cols,2,  f"Expected 2 columns, got {cols}")
        # Assert that number of rows (from shape) is greater than 0 otherwise emit error
        self.assertGreater(rows,0, f"Expected 0 rows, got {rows}")
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
        Test all Tuebingen pair files and report only the failures.
        """
        search_path = os.path.join(self.data_folder, 'pair*.txt')
        all_files = glob.glob(search_path)
        data_files = [f for f in all_files if '_des.txt' not in f]

        failed_files = []

        for file_path in data_files:
            filename = os.path.basename(file_path)

            try:
                df = load_tuebingen_pair(self.data_folder, filename)

                # Validation Logic
                if df is None:
                    failed_files.append(f"{filename} (Returned None)")
                elif df.empty:
                    failed_files.append(f"{filename} (Empty DataFrame)")
                elif df.shape[1] < 2:
                    failed_files.append(f"{filename} (Less than 2 columns)")

            except Exception as e:
                failed_files.append(f"{filename} (Raised Exception: {str(e)})")

        if failed_files:
            print(f"\n\n{'!' * 20} LOADING FAILURES {'!' * 20}")
            for failure in failed_files:
                print(f"  - {failure}")
            print(f"{'!' * 58}\n")

        self.assertEqual(len(failed_files), 0, f"Failed to load {len(failed_files)} files out of {len(data_files)}.")


if __name__ == '__main__':
    unittest.main()


