import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import networkx as nx
import os


def draw_causal_graph(graph, title="Causal Graph", node_color='lightblue', save_path=None):
    """
    This takes our two-variable graph and draws it nicely. We'll make sure
    the nodes look clean and the arrow (if there is one) is clear.
    """

    # Safety check: We prevent execution on None values to avoid crashes 
    # during automated testing or if the discovery algorithm fails to return a result.
    if graph is None:
        print("Error: No graph provided for visualization.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title(title)

    pos = nx.circular_layout(graph)

    # The 'connectionstyle' is set to a slight radius so that if the model 
    # detects feedback loops or reciprocal relationships, the arrows 
    # don't overlap, making the direction of causality immediately 
    # legible for publication.
    nx.draw(graph, pos, 
            ax=ax,
            with_labels=True, 
            node_color=node_color, 
            node_size=2000, 
            font_size=12, 
            font_weight='bold',
            arrows=True,
            arrowsize=20,
            connectionstyle='arc3, rad=0.1') 

    if save_path:
        directory = os.path.dirname(save_path)
        if directory: 
            os.makedirs(directory, exist_ok=True)
            
        plt.savefig(save_path)
        print(f"Graph successfully saved to: {save_path}")

    print("Opening plot window...")
    plt.show()


def save_graph_to_file(graph, filename):
    """   
    Saves the picture we just drew as a PNG or JPEG so we can put it 
    in a report.
    """
    if graph is not None:
        plt.savefig(filename)
        print(f"Graph successfully saved to {filename}")
