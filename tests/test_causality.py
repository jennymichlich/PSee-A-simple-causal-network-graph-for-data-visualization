import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import unittest
import pandas as pd
import numpy as np
import networkx as nx
from contextlib import redirect_stdout, redirect_stderr
from src.loaders import load_tuebingen_pair, get_all_ground_truths
# from src.causality import run_pc_algo_library as run_pc_algorithm
from src.causality import run_pc_algo_library, get_adjacency_matrix, check_causal_direction_anm
import warnings
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class TestPCAlgorithm(unittest.TestCase):
    def test_pc_perfect_correlation(self):
        df = pd.DataFrame({'A': [1, 2, 3, 4, 5] * 20, 'B': [1, 2, 3, 4, 5] * 20})
        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull), redirect_stderr(fnull):
                dag = run_pc_algo_library(df, alpha=0.05)
        
        self.assertEqual(dag.number_of_edges(), 1)

    def test_pc_alpha_parameter(self):
        np.random.seed(42)
        A = np.random.rand(100)
        B = A + np.random.normal(0, 2.0, 100) 
        df = pd.DataFrame({'A': A, 'B': B})

        with open(os.devnull, 'w') as fnull:
            with redirect_stdout(fnull):
                dag_strict = run_pc_algo_library(df, alpha=0.00)
                dag_loose = run_pc_algo_library(df, alpha=1.00)

        self.assertEqual(dag_strict.number_of_edges(), 0)
        self.assertEqual(dag_loose.number_of_edges(), 1)


class TestCausalityStructure(unittest.TestCase):
    def test_matrix_empty_graph(self):
        dag = nx.DiGraph()
        dag.add_nodes_from(['A', 'B'])
        matrix = get_adjacency_matrix(dag)
        self.assertEqual(matrix.sum().sum(), 0)

    def test_matrix_none_input(self):
        matrix = get_adjacency_matrix(None)
        self.assertEqual(matrix.shape, (2, 2))

    def test_matrix_reverse_edge(self):
        dag = nx.DiGraph()
        dag.add_edge('B', 'A') 
        matrix = get_adjacency_matrix(dag)
        self.assertEqual(matrix.loc['B', 'A'], 1)


# class TestCausalBenchmark(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.data_folder = os.path.join('data', 'pairs')
#         cls.ground_truths = get_all_ground_truths(cls.data_folder)
#         cls.alpha = 0.05
#         print(f"\n[Setup] Testing {len(cls.ground_truths)} pairs...")
#
#     def test_all_pairs_anm(self):
#         passed, total = 0, 0
#         sorted_files = sorted(self.ground_truths.keys())
#
#         print(f"\n{'File':<15} | {'Ground Truth':<15} | {'Prediction':<15} | {'Status'}")
#         print("-" * 60)
#
#         for filename in sorted_files:
#             expected_truth = self.ground_truths[filename]
#             if expected_truth not in ['A --> B', 'B --> A']: continue
#
#             with self.subTest(file=filename):
#                 df = load_tuebingen_pair(self.data_folder, filename)
#
#                 # SILENCE the library internal chatter here
#                 with open(os.devnull, 'w') as fnull:
#                     with redirect_stdout(fnull), redirect_stderr(fnull):
#                         prediction_full, _, _ = check_causal_direction_anm(df, alpha=self.alpha)
#
#                 prediction_core = prediction_full.split(" (")[0]
#                 is_correct = (prediction_core == expected_truth)
#
#                 status = "PASS" if is_correct else "FAIL"
#                 print(f"{filename:<15} | {expected_truth:<15} | {prediction_core:<15} | {status}")
#
#                 if is_correct: passed += 1
#                 total += 1
#                 self.assertEqual(prediction_core, expected_truth)
#
#         print("-" * 60)
#         print(f"Final Accuracy: {passed}/{total} ({(passed/total)*100:.1f}%)")


if __name__ == '__main__':
    unittest.main()