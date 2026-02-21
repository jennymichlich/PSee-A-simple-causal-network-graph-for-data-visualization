import argparse
import os
from src.loaders import load_causal_data
from src.causality import run_pc_algo_library, get_adjacency_matrix, check_causal_direction_anm
from src.graphs import draw_causal_graph


def main():
    parser = argparse.ArgumentParser(description="PSee: Hybrid Causal Discovery Pipeline")

    parser.add_argument('--nodes', type=int, default=2, choices=[2, 3, 4],
                        help="Number of variables in the dataset")
    parser.add_argument('--pair', type=str, default=None,
                        help="Filename (e.g., pair0001.txt or fork_data.csv)")
    parser.add_argument('--alpha', type=float, default=0.05,
                        help="Significance level for independence tests")

    args = parser.parse_args()

    # ---- Smart Defaults Configuration ----
    # INTENT: This dictionary was created to make the use of this program form the command line
    # easier for the user by using 'smart' default source file names.
    defaults = {
        2: (os.path.join('data', 'pairs'), 'pair0001.txt'),
        3: (os.path.join('data', 'synthetic', '3-variables'), 'collider_data.csv'),
        4: (os.path.join('data', 'synthetic', '4-variables'), 'synthetic_4_var.csv')
    }

    if args.pair is None:
        data_folder, target_file = defaults[args.nodes]
    else:
        data_folder = defaults[args.nodes][0]
        target_file = args.pair

    # ---- Data Loading Phase ----
    print(f"\n--- Loading: {target_file} ---")
    df = load_causal_data(data_folder, target_file)

    if df is None:
        return

    # ---- Phase 1: Structure Discovery (PC Algorithm) ----
    print(f"Running PC Algorithm on {len(df.columns)} variables...")
    dag = run_pc_algo_library(data=df, alpha=args.alpha)

    # ---- Phase 2: Direction Refinement (Hybrid ANM) ----
    # NOTE: Initial testing revealed that while the PC algorithm
    # successfully identified 'Collider' structures, it failed to correctly
    # orient 'Fork' structures (B <- A -> C).
    #
    # INTENT: This hybrid refinement phase was implemented specifically to
    # resolve these mis-identifications. By applying Additive Noise Modeling (ANM)
    # to every edge found by the PC algorithm, we hope to break the statistical ties
    # between Forks and Chains.

    print("Refining edge orientations using Additive Noise Models...")
    current_edges = list(dag.edges())

    for u, v in current_edges:
        pair_df = df[[u, v]]

        # ANM check
        direction, _, _ = check_causal_direction_anm(df=pair_df, alpha=0.05)

        # If ANM evidence suggests the reverse of the PC orientation, we flip it.
        # This correction is what allows the 'Fork' data to be correctly visualized.
        if direction == "B --> A":  # 'B' represents the second node in the pair (v)
            print(f"  [ANM Correction] Reversing edge {u}->{v} to {v}->{u}")
            dag.remove_edge(u, v)
            dag.add_edge(v, u)
        else:
            print(f"  [ANM Confirmed] Direction: {u}->{v}")

    # ---- Visualization and Export ----
    base_name = os.path.splitext(target_file)[0]
    output_path = os.path.join('results', f"{base_name}.png")
    display_title = f"Causal Analysis: {base_name}"

    print(f"\nFinal Graph: {dag.number_of_nodes()} nodes, {dag.number_of_edges()} edges.")
    print(f"Adjacency Matrix:\n{get_adjacency_matrix(dag=dag)}")

    draw_causal_graph(dag,
                      title=display_title,
                      save_path=output_path)


if __name__ == "__main__":
    main()
