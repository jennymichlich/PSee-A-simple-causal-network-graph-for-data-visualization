import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
import pandas as pd
import numpy as np
from src.loaders import load_tuebingen_pair
# from src.causality import run_pc_algo_library as run_pc_algorithm
from src.causality import run_pc_algo_library
from src.causality import get_adjacency_matrix


class TestPCAlgoLib(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Runs ONCE for the entire class.
        """
        cls.alpha = 0.05
        cls.data_folder = os.path.join('data', 'pairs')
        cls.filename = 'pair0001.txt'
        
        # Load and Run once
        cls.df = load_tuebingen_pair(cls.data_folder, cls.filename)
        print(f"\n[Test Setup] Running PC Algorithm on {cls.filename} (This may take a moment)...")
        cls.dag = run_pc_algo_library(data=cls.df, alpha=cls.alpha)
        cls.matrix = get_adjacency_matrix(dag=cls.dag)

    def test_pc_finds_connection(self):
        """
        Checks if the PC algorithm finds a connection (edge) between A and B.
        """
        self.assertGreater(self.dag.number_of_edges(), 0, "Graph should have at least one edge.")

    def test_adjacency_matrix_format(self):
        """
        Ensures the output can be converted to a 2x2 numeric adjacency matrix.
        """
        self.assertIsNotNone(self.matrix, "Adjacency matrix should not be None.")
        self.assertEqual(self.matrix.shape, (2, 2), f"Expected (2,2) matrix, got {self.matrix.shape}")
        
        if isinstance(self.matrix, pd.DataFrame):
            has_nans = self.matrix.isnull().values.any()
        else:
            has_nans = np.isnan(self.matrix).any()
            
        self.assertFalse(has_nans, "Adjacency matrix contains NaN values.")


    # def test_direction_accuracy_maybe():
    #     """
    #     Okay, this is the tricky one.
        
    #     The Tuebingen data has a ground truth (like A causes B), but I've read 
    #     that standard PC might fail to orient the arrow if there are no V-structures 
    #     (which you can't have with only 2 vars).
        
    #     But let's write this test anyway? If it fails, we can mark it as 'expected failure'
    #     or maybe we need to implement that 'Additive Noise Model' thing later.
        
    #     For now:
    #     1. Load pair 1.
    #     2. Check if the result is specifically A -> B.
    #     """
    #     # TODO: Load data
    #     # TODO: Run algorithm
    #     # TODO: Check if edge is A->B specifically
    #     pass




if __name__ == '__main__':
    unittest.main()
