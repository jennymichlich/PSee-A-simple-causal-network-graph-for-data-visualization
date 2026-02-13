import networkx as nx
import numpy as np
import pandas as pd
from causallearn.search.FCMBased.ANM.ANM import ANM
import warnings
# from sklearn.exceptions import ConvergenceWarning
# warnings.filterwarnings("ignore", category=ConvergenceWarning)


# ==========================================
# OPTION A: The Library Way (pgmpy)
# ==========================================

from pgmpy.estimators import PC

def run_pc_algo_library(data, alpha=0.05, test_name='pearsonr'):
    """
    Runs the PC algorithm.
    
    Args:
        data (pd.DataFrame): The data.
        alpha (float): Significance level (default 0.05).
        test_name (str): The statistical test to use. 
                         Options: 'pearsonr', 'fisher-z', 'chi_square', 'g_sq'.
                         Default is 'pearsonr' (best for continuous data).
    """
    try:
        print("Running PC Algorithm...")
        est = PC(data)
        model = est.estimate(return_type='dag', 
                             significance_level=alpha, 
                             ci_test=test_name,
                             show_progress=False)
        dag = nx.DiGraph(model)
        return dag
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_adjacency_matrix(dag):
    """
    Converts a pgmpy / networkx DAG into a clean 2x2 adjacency matrix.
    Ensures a valid DataFrame is returned even if dag is None (testing revealed this error).
    """
    # Create the default template
    matrix = pd.DataFrame(0, index=['A', 'B'], columns=['A', 'B'])
    
    # If dag is None or empty, we just return the zeros
    if dag is None:
        return matrix
        
    # Check for edges (if the nodes exist in the graph)
    if 'A' in dag.nodes and 'B' in dag.nodes:
        if dag.has_edge('A', 'B'):
            matrix.loc['A', 'B'] = 1
        if dag.has_edge('B', 'A'):
            matrix.loc['B', 'A'] = 1
            
    return matrix


def check_causal_direction_anm(df, alpha=0.05):
    """
    Determines the causal direction between two variables (A, B) using
    Additive Noise Models (ANM).
    """
    
    data_a = df['A'].to_numpy().reshape(-1, 1)
    data_b = df['B'].to_numpy().reshape(-1, 1)

    anm = ANM()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore") 
        p_forward, p_backward = anm.cause_or_effect(data_a, data_b)

    direction = "Inconclusive"
    
    if p_forward > alpha and p_backward < alpha:
        direction = "A --> B"    
    elif p_backward > alpha and p_forward < alpha:
        direction = "B --> A"     
    elif p_forward > p_backward:
        direction = "A --> B (Weak)"
    elif p_backward > p_forward:
        direction = "B --> A (Weak)"

    return direction, p_forward, p_backward


# ==========================================
# OPTION B: The Manual Way (From Scratch)
# ==========================================

def check_independence(data, var_a, var_b):
    """
    Helper for Manual Mode.
    
    Checks the math to see if two variables are related.
    """
    # TODO: Calculate the correlation between A and B
    # TODO: Run Fisher's Z-test (or a simple T-test for now)
    # TODO: Return True if the p-value is high (independent), False if low (related)
    return None

def orient_edges(skeleton):
    """
    Helper for Manual Mode.
    
    Decides which way the arrow points (Issue #4).
    For a 2-variable system, we might just look at the raw statistics 
    or just leave it undirected if we can't tell.
    """
    # TODO: If we have 3 variables, look for V-structures (X -> Z <- Y)
    # TODO: For 2 variables, we might return the graph as is
    return skeleton

def run_pc_algo_manual(data):
    """
    Addresses Issue #1 & #4 manually.
    """
    print("Running PC Algorithm (Manual Implementation)...")
    
    # 1. Start with a full graph (A connected to B)
    columns = data.columns
    graph = nx.complete_graph(columns)
    
    # 2. Check for independence (Skeleton Phase)
    # We look at every pair of variables
    for u, v in list(graph.edges()):
        independent = check_independence(data, u, v)
        if independent:
            print(f"Removing edge between {u} and {v}")
            graph.remove_edge(u, v)
    
    # 3. Orient the edges (make it a Directed Graph)
    # Turn the skeleton into a Directed Graph (DiGraph)
    final_graph = nx.DiGraph(graph)
    final_graph = orient_edges(final_graph)
    
    return final_graph


# ==========================================
# SHARED HELPER FUNCTIONS
# These work regardless of which option we chose above.
# ==========================================

def get_matrix(graph):
    """
    Addresses Issue #3: Produces an adjacency matrix.
    
    Takes the graph (from either Option A or B) and turns it into a grid.
    """
    if graph is None:
        return None
        
    # Convert graph to a numpy matrix (0s and 1s)
    matrix = nx.to_numpy_array(graph)
    return matrix
