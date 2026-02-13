import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
import pandas as pd
import numpy as np
from src.loaders import load_tuebingen_pair, get_all_ground_truths
# from src.causality import run_pc_algo_library as run_pc_algorithm
from src.causality import run_pc_algo_library, get_adjacency_matrix, check_causal_direction_anm
import warnings
import networkx as nx
# from sklearn.exceptions import ConvergenceWarning
# warnings.filterwarnings("ignore", category=ConvergenceWarning)


class TestPCAlgorithm(unittest.TestCase):
    """
    Specific unit tests for the run_pc_algo_library.
    """

    def test_pc_perfect_correlation(self):
        """
        If A and B are identical the PC algorithm must find an edge.
        """
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5] * 20,
                           'B': [1, 2, 3, 4, 5] * 20})
        
        dag = run_pc_algo_library(df, alpha=0.05)
        
        self.assertCountEqual(dag.nodes(), ['A', 'B'])
        self.assertEqual(dag.number_of_edges(), 1, "PC algorithm failed to find an edge.")

    def test_pc_alpha_parameter(self):
        """
        Test that changing alpha actually changes the result.
        """
        np.random.seed(42)
        A = np.random.rand(100)
        B = A + np.random.normal(0, 2.0, 100) 
        df = pd.DataFrame({'A': A, 'B': B})

        dag_strict = run_pc_algo_library(df, alpha=0.00)
        self.assertEqual(dag_strict.number_of_edges(), 0, "Alpha=0.0 should result in no edges.")

        dag_loose = run_pc_algo_library(df, alpha=1.00)
        self.assertEqual(dag_loose.number_of_edges(), 1, "Alpha=1.0 should force an edge.")
        

class TestCausalityStructure(unittest.TestCase):
    """
    Tests the structural integrity of helper functions without statistical data.
    """

    def test_matrix_empty_graph(self):
        """
        Ensure an empty graph returns a 2x2 matrix of zeros not an empty DF.
        """
        dag = nx.DiGraph()
        dag.add_nodes_from(['A', 'B'])
        
        matrix = get_adjacency_matrix(dag)
        
        self.assertEqual(matrix.shape, (2, 2))
        self.assertEqual(matrix.sum().sum(), 0, "Matrix should be all zeros for empty graph")

    def test_matrix_none_input(self):
        """
        Ensure passing None returns a safe default (2x2 zeros) instead of crashing.
        """
        matrix = get_adjacency_matrix(None)
        
        self.assertIsNotNone(matrix)
        self.assertEqual(matrix.shape, (2, 2))
        self.assertEqual(matrix.sum().sum(), 0)

    def test_matrix_reverse_edge(self):
        """
        Ensure B->A is mapped to row B, col A.
        """
        dag = nx.DiGraph()
        dag.add_edge('B', 'A') 
        
        matrix = get_adjacency_matrix(dag)
        1
        self.assertEqual(matrix.loc['B', 'A'], 1, "Failed to map B->A edge")
        self.assertEqual(matrix.loc['A', 'B'], 0, "Incorrectly mapped B->A as A->B")


class TestKnownEdgeCases(unittest.TestCase):
    """
    Focused tests for real-world pairs that are known to be difficult
    or have failed in previous benchmark runs.
    """
    @classmethod
    def setUpClass(cls):
        cls.data_folder = os.path.join('data', 'pairs')
        cls.alpha = 0.05

    def test_specific_pair(self):
        """
        Test a specific pair. Useful because some pairs are known to be difficult.
        """
        filename = 'pair0004.txt'
        df = load_tuebingen_pair(self.data_folder, filename)
        
        prediction, p_fwd, p_bwd = check_causal_direction_anm(df, alpha=self.alpha)
        
        print(f"\n--- Debugging {filename} ---")
        print(f"P(A->B): {p_fwd:.4f} | P(B->A): {p_bwd:.4f}")
        print(f"Result: {prediction}")
        
        self.assertEqual(prediction.split(" (")[0], "A --> B")


class TestCausalBenchmark(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.data_folder = os.path.join('data', 'pairs')
        cls.ground_truths = get_all_ground_truths(cls.data_folder)
        cls.alpha = 0.05
        
        print(f"\n[Setup] Found {len(cls.ground_truths)} pairs with ground truth.")        

    def test_all_pairs_anm(self):
        """
        Test every file in the data folder and checks if ANM correctly identifies the direction.
        """
        passed = 0
        total = 0
        
        sorted_files = sorted(self.ground_truths.keys())

        print(f"\n{'='*60}")
        print(f"{'File':<15} | {'Ground Truth':<15} | {'ANM Prediction':<15} | {'Result'}")
        print(f"{'-'*60}")

        for filename in sorted_files:
            expected_truth = self.ground_truths[filename]
            
            if expected_truth not in ['A --> B', 'B --> A']:
                continue

            with self.subTest(file=filename):
                df = load_tuebingen_pair(self.data_folder, filename)
                if df is None:
                    self.fail(f"Could not load {filename}")

                prediction_full, _, _ = check_causal_direction_anm(df, alpha=self.alpha)
                
                prediction_core = prediction_full.split(" (")[0]
                
                is_correct = (prediction_core == expected_truth)
                
                status = "PASS" if is_correct else "FAIL"
                print(f"{filename:<15} | {expected_truth:<15} | {prediction_core:<15} | {status}")
                
                if is_correct:
                    passed += 1
                total += 1
                
                self.assertEqual(prediction_core, expected_truth, 
                                 f"Failed on {filename}: Expected {expected_truth}, got {prediction_full}")

        print(f"{'='*60}")
        accuracy = (passed / total) * 100 if total > 0 else 0
        print(f"Final Accuracy: {passed}/{total} ({accuracy:.1f}%)")


if __name__ == '__main__':
    unittest.main()