# PSee-A-simple-causal-network-graph-for-data-visualization
## 1. Team
Jenny M. Michlich 
& Carlo Tak


## 2. Project Description:
Murmurings of the replication crisis have been ongoing since the early years of my first undergraduate experience, but this conversation has moved from university hallways to public discourse in academic literature. Science, broadly, has been called out regarding the lack of reproducibility of major findings from prominent scholars and smaller labs alike (Shrout & Rodgers, 2018). While effective coding protocols (Azevedo et al., 2025) and the emerging field of Metascience (Peterson & Panofsky, 2023) offer pathways forward, we believe a significant driver of this crisis is the scientific community's over-reliance on correlative data. 

Correlations are often undirected and unstable, leading to findings that fail to replicate when context changes. We propose that by moving from correlative studies to studies of **modeled causation**, researchers can identify more robust, reproducible mechanisms. To support this, we have developed **PSee**, a Python-based tool utilizing the PC algorithm (Spirtes et al., 2000). Our implementation aims to help researchers quickly investigate causal and multilevel network graphs that propose mechanisms for complex systems. Currently, PSee models two-variable, three-variable, and four-variable systems, producing publication-ready network graphs that host two levels of organization within the modeled system as proposed by Gebharter (2017).


## 3. Installation

To set up the PSee project environment, we recommend using **Conda**. [cite_start]This ensures all specialized causal inference libraries, such as `pgmpy` and `causal-learn`, are installed correctly.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/jennymichlich/PSee-A-simple-causal-network-graph-for-data-visualization.git](https://github.com/jennymichlich/PSee-A-simple-causal-network-graph-for-data-visualization.git)
   cd PSee-A-simple-causal-network-graph-for-data-visualization

2. **Create the Conda environment:**
    This command uses the provided environment.yml file to install Python 3.10 and all necessary dependencies.
    ```bash
    conda env create -f environment.yml

3. **Activate the environment:**
    ```bash
    conda activate psee_env


## 4. User Documentation
PSee is executed via the command line using `main.py`. The program loads data, performs causal discovery using Additive Noise Models (ANM) and the PC Algorithm, and visualizes the resulting network.

### Basic Usage
To analyze the default data pair:
    ```bash
    python main.py

### Command-Line Arguments
The following flags allow you to customize the analysis based on the parameters defined in `main.py`:

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `--pair` | `str` | `pair0001.txt` | The name of the file in `data/pairs/` to analyze. |
| `--alpha` | `float` | `0.05` | Significance level for independence tests. |
| `--output` | `str` | `output_graph.png` | Filename to save the resulting graph. |
| `--test` | `str` | `pearsonr` | Statistical test to use (options: `pearsonr`, `fisher-z`, `chi_square`). |


## 5. License

This project is licensed under the **MIT License**.

### Motivation for Selecting the MIT License
The selection of the MIT License for the PSee project was guided by several key factors relevant to our research goals and the academic community:

* **Facilitating Scientific Reproducibility**: Given that PSee was developed as a direct response to the replication crisis in psychology and the broader sciences, it was imperative to choose a license that imposes minimal legal barriers to access and reuse.
* **Encouraging Open Collaboration**: By utilizing a permissive license, we allow researchers and students to freely adapt our implementation of the PC algorithm for various complex adaptive systems without fear of restrictive legal obligations.
* **Library Compatibility and Integration**: Our project relies on several key open-source libraries, including **pgmpy** and **causal-learn** for causal discovery, as well as **pandas**, **networkx**, and **matplotlib** for data handling and visualization. The MIT License ensures seamless legal compatibility with these widely used tools.
* **Simplicity and Clarity**: The brevity of the MIT License aligns with our goal of providing "simple tools" for scientists, allowing contributors to focus on the statistical logic of causal discovery rather than complex legal documentation.


## 6. Contributing & Bug Reports

### Reporting Bugs
If you encounter any issues or have feature requests, please follow these steps:
* Navigate to the **Issues** tab in this GitHub repository.
* Click **New Issue** to open a ticket.
* Provide a detailed description of the bug, including steps to reproduce it, the dataset used, and any error messages received.

### How to Contribute
We welcome contributions from researchers and developers who share our goal of providing accessible tools to address the replication crisis through modeled causation:
1. **Fork** the repository to your own GitHub account.
2. Create a new **feature branch** for your updates (e.g., `git checkout -b feature/NewCausalMetric`).
3. **Commit** your changes. 
4. **Note on Documentation**: Per our project requirements, please ensure you include **in-code comments** that clearly explain the reasoning and functionality of any new code additions.
5. **Push** your branch to GitHub and open a **Pull Request** for review.



## 7. References
1. Shrout, P. E., & Rodgers, J. L. (2018). Psychology, science, and knowledge construction: Broadening perspectives from the replication crisis. Annual review of psychology, 69(1), 487-510.
2. Azevedo, I., Vasconcelos, A. P., Teixeira, E., & Soares, S. (2025, September). Survey-Based Insights into the Replication Crisis and the 3R in Software Engineering. In Simpósio Brasileiro de Engenharia de Software (SBES) (pp. 405-415). SBC.
3. Peterson, D., & Panofsky, A. (2023). Metascience as a scientific social movement. Minerva, 61(2), 147-174.
4. Causation, Prediction, and Search P. Spirtes, C. Glymour, and R. Scheines (2nd edition, MIT Press, 2000)
5. Gebharter, A. Uncovering constitutive relevance relations in mechanisms. Philos Stud 174, 2645–2666 (2017). https://doi.org/10.1007/s11098-016-0803-3

