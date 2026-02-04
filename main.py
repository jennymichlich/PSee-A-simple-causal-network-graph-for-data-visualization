import argparse
import os
import matplotlib.pyplot as plt
from src.loaders import load_tuebingen_pair
from src.causality import run_pc_algo_library
from src.graphs import draw_causal_graph

def main():

    print("In main.")
    # parser = argparse.ArgumentParser(description="Run PC Algorithm on Tuebingen Data")
    # parser.add_argument('--pair', type=str, default='pair0001.txt', 
    #                     help="The name of the file to analyze (e.g., pair0001.txt)")
    # parser.add_argument('--alpha', type=float, default=0.05, 
    #                     help="Significance level for independence tests")
    # parser.add_argument('--output', type=str, default='output_graph.png',
    #                     help="Filename to save the resulting graph")
    
    # args = parser.parse_args()


    # data_folder = 'data\pairs'
    
    # print(f"--- Starting Analysis for {args.pair} ---")

    # print("Loading data...")
    # df = load_tuebingen_pair(data_folder, args.pair)
    
    # if df is None:
    #     print("Stopping: Could not load data.")
    #     return
    # else:
    #     print(df.head())
    #     return

if __name__ == "__main__":
    main()