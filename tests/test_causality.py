import pytest
import pandas as pd
# We'll need to import our actual functions once they are written
from src.loaders import load_tuebingen_pair
from src.causality import run_pc_algorithm

def test_pc_finds_connection():
    """
    So, I'm not 100% sure if the basic PC algorithm can handle just two variables,
    but it should at least tell us they are related, right?
    
    The plan here:
    1. Load 'pair0001.txt' (Altitude -> Temp).
    2. Run our PC function.
    3. Just check if there is ANY edge between them (A-B or A->B).
    
    If it returns no edges, we know something is definitely broken.
    """
    # TODO: Load pair 1 data
    # TODO: Run the algorithm
    # TODO: Assert that graph.number_of_edges() > 0
    pass

def test_direction_accuracy_maybe():
    """
    Okay, this is the tricky one.
    
    The Tuebingen data has a ground truth (like A causes B), but I've read 
    that standard PC might fail to orient the arrow if there are no V-structures 
    (which you can't have with only 2 vars).
    
    But let's write this test anyway? If it fails, we can mark it as 'expected failure'
    or maybe we need to implement that 'Additive Noise Model' thing later.
    
    For now:
    1. Load pair 1.
    2. Check if the result is specifically A -> B.
    """
    # TODO: Load data
    # TODO: Run algorithm
    # TODO: Check if edge is A->B specifically
    pass

def test_adjacency_matrix_format():
    """
    This one is for Issue #3.
    
    Whatever the algorithm outputs, we need to make sure we can turn it into 
    an adjacency matrix (0s and 1s) so the graph plotting code doesn't crash.
    
    We should just check:
    - Is it a square matrix?
    - Are dimensions 2x2?
    """
    # TODO: Run algorithm
    # TODO: Convert result to matrix
    # TODO: Assert shape is (2, 2)
    pass

