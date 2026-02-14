import argparse
import os
import matplotlib.pyplot as plt
from src.loaders import load_tuebingen_pair
from src.causality import run_pc_algo_library, get_adjacency_matrix, check_causal_direction_anm
from src.graphs import draw_causal_graph
import networkx as nx


def main():

    print("In main.")
    parser = argparse.ArgumentParser(description="Run PC Algorithm on Tuebingen Data")
    parser.add_argument('--pair', type=str, default='pair0001.txt', 
                        help="The name of the file to analyze (e.g., pair0001.txt)")
    parser.add_argument('--alpha', type=float, default=0.05, 
                        help="Significance level for independence tests")
    parser.add_argument('--output', type=str, default='output_graph.png',
                        help="Filename to save the resulting graph")
    parser.add_argument('--test', type=str, default='pearsonr', 
                        help="Statistical test: pearsonr, fisher-z, or chi_square")

    args = parser.parse_args()

    # Use os.path.join for Windows/Linux compatibility
    data_folder = os.path.join('data', 'pairs')
    
    print(f"--- Starting Analysis for {args.pair} ---")

    print("Loading data...")
    df = load_tuebingen_pair(data_folder, args.pair)
    
    if df is None:
        print("Stopping: Could not load data.")
        return
    else:
        print("df :")
        print(df.head())

        direction, p_forward, p_backward = check_causal_direction_anm(df=df, alpha=0.05)
        print("direction :", direction)
        print("p_forward :", p_forward)
        print("p_backward :", p_backward)

        print("\nCorrelation Matrix:")
        print(df.corr()) 
        print("-------------------\n")

        dag = run_pc_algo_library(data=df, alpha=args.alpha)

        matrix = get_adjacency_matrix(dag=dag)
        print("matrix :")
        print(matrix)

        num_nodes = dag.number_of_nodes()
        print(f"Number of nodes: {num_nodes}")
        num_edges = dag.number_of_edges()
        print(f"Number of edges: {num_edges}")
        print(dag.edges(data=True))

        if dag is not None:

            undirected_graph = dag.to_undirected()

            print("\nPlotting graph...")
            
            pos = nx.circular_layout(dag)
            
            print(f"Node Positions: {pos}")
            
            plt.figure(figsize=(8, 6)) 
            plt.title(f"Causal Graph for {args.pair} (alpha={args.alpha})")
            nx.draw(undirected_graph, pos, 
                    with_labels=True, 
                    node_color='lightblue', 
                    node_size=2000,    
                    # arrowsize=20, 
                    font_size=12, 
                    font_weight='bold',
                    connectionstyle='arc3, rad=0.1') 
            
            # plt.savefig(args.output)
            # print(f"Graph saved to {args.output}")
            
            plt.show()
            
        else:
            print("No graph returned (PC Algorithm failed).")



if __name__ == "__main__":
    main()