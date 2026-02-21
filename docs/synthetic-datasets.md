# Building synthetic datasets for three-variable and four-variable systems

Two synthetic datasets were generated to further test our PSee algorithm. Descriptions of these datasets can be found below.

Three synthetic datasets were generated to illustrate how the structure of causal relationships between variables shapes the statistical patterns we observe in data. Each dataset contains three variables — X, Y, and Z — with the relationships between them constructed according to a different causal architecture. The datasets are designed so that their statistical properties, such as correlations and conditional dependencies, directly reflect the underlying causal structure that produced them, making them useful for studying how well analytical methods can recover or respect those structures.

Three synthetic datasets were generated to illustrate how causal relationships between variables shape the statistical patterns we observe in data. Each dataset contains four variables — W, X, Y, and Z — with the relationships between them constructed according to a different causal architecture. In the fork structure, a single common cause W drives X, Y, and Z, inducing correlations among them that vanish once W is accounted for. In the collider structure, X and Y independently cause W, which in turn causes Z, such that X and Y appear unrelated until conditioning on W reveals a dependence. In the chain structure, causation flows sequentially from X through W and Y to Z, so that the relationship between X and Z is entirely mediated by the intervening variables. The datasets are designed so that their statistical properties directly reflect the underlying causal structure that produced them, making them useful for studying how well analytical methods can recover or respect those structures.


### References for synthetic datasets:

1. Huang, J., Yao, Y., & Divakaran, A. (2025). Transforming Causality: Transformer-Based Temporal Causal Discovery with Prior Knowledge Integration. ArXiv.org. https://arxiv.org/abs/2508.15928
2. Assaad C, Devijver E, Gaussier E. 2022. Entropy-Based Discovery of Summary Causal Graphs in Time Series. Entropy. 24(8):1156–1156. doi:https://doi.org/10.3390/e24081156.
3. The ultimate guide to generating synthetic data for causal inference | Program Evaluation. (2020). Program Evaluation; PMAP 8141: Program Evaluation. https://evalsp21.classes.andrewheiss.com/example/synthetic-data/
