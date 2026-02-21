import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

## The three main structures used in this dataset are forks, colliders, and chains.

class CausalModel:
    def __init__(self, n_samples=1000):
        self.n = n_samples

    ## In the fork structure, the initial causal agent Z moves to X and Y, where
    ## noise is added to correlate X and Y. This is also demonstrated in the final plots.
    
    def generate_fork(self):
        """Fork structure: X <- Z -> Y"""
        Z = np.random.randn(self.n)
        X = 2 * Z + np.random.randn(self.n) * 0.5
        Y = -1.5 * Z + np.random.randn(self.n) * 0.5
        return {'X': X, 'Y': Y, 'Z': Z}

    ## In the collider structure, the initial causal agents X and Y move to influence Z, where
    ## noise is added to correlate X and Y. This is also demonstrated in the final plots.
    
    def generate_collider(self):
        """Collider structure: X -> Z <- Y"""
        X = np.random.randn(self.n)
        Y = np.random.randn(self.n)
        Z = 1.5 * X + 2 * Y + np.random.randn(self.n) * 0.5
        return {'X': X, 'Y': Y, 'Z': Z}

    ## In the chain structure, the initial causal agent X influences Z and Y in a chain, where
    ## noise is added to correlate Z and Y. This is also demonstrated in the final plots.
    
    def generate_chain(self):
        """Chain structure: X -> Z -> Y"""
        X = np.random.randn(self.n)
        Z = 1.5 * X + np.random.randn(self.n) * 0.5
        Y = 2 * Z + np.random.randn(self.n) * 0.5
        return {'X': X, 'Y': Y, 'Z': Z}


# Generate datasets
model = CausalModel(n_samples=1000)

fork_data = model.generate_fork()
collider_data = model.generate_collider()
chain_data = model.generate_chain()

# Convert to DataFrames
df_fork = pd.DataFrame(fork_data)
df_collider = pd.DataFrame(collider_data)
df_chain = pd.DataFrame(chain_data)

# Verify causal properties
print("=== FORK STRUCTURE (X <- Z -> Y) ===")
print(f"Cor(X,Y): {pearsonr(df_fork['X'], df_fork['Y'])[0]:.3f} (should be correlated)")
# Conditional independence test (residuals after regressing out Z)
from sklearn.linear_model import LinearRegression

## The linear regressions check the correlation of the desired variables.

lr = LinearRegression()
lr.fit(df_fork[['Z']], df_fork['X'])
X_residual = df_fork['X'] - lr.predict(df_fork[['Z']])
lr.fit(df_fork[['Z']], df_fork['Y'])
Y_residual = df_fork['Y'] - lr.predict(df_fork[['Z']])
print(f"Partial Cor(X,Y|Z): {pearsonr(X_residual, Y_residual)[0]:.3f} (should be ~0)")

print("\n=== COLLIDER STRUCTURE (X -> Z <- Y) ===")
print(f"Cor(X,Y): {pearsonr(df_collider['X'], df_collider['Y'])[0]:.3f} (should be ~0)")
# Conditioning on Z creates dependence
lr.fit(df_collider[['Z']], df_collider['X'])
X_residual = df_collider['X'] - lr.predict(df_collider[['Z']])
lr.fit(df_collider[['Z']], df_collider['Y'])
Y_residual = df_collider['Y'] - lr.predict(df_collider[['Z']])
print(f"Partial Cor(X,Y|Z): {pearsonr(X_residual, Y_residual)[0]:.3f} (should be non-zero)")

print("\n=== CHAIN STRUCTURE (X -> Z -> Y) ===")
print(f"Cor(X,Y): {pearsonr(df_chain['X'], df_chain['Y'])[0]:.3f} (should be correlated)")

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].scatter(df_fork['X'], df_fork['Y'], alpha=0.5)
axes[0].set_title('Fork: X ← Z → Y')
axes[0].set_xlabel('X')
axes[0].set_ylabel('Y')

axes[1].scatter(df_collider['X'], df_collider['Y'], alpha=0.5)
axes[1].set_title('Collider: X → Z ← Y')
axes[1].set_xlabel('X')
axes[1].set_ylabel('Y')

axes[2].scatter(df_chain['X'], df_chain['Y'], alpha=0.5)
axes[2].set_title('Chain: X → Z → Y')
axes[2].set_xlabel('X')
axes[2].set_ylabel('Y')

plt.tight_layout()
plt.savefig('causal_structures.png', dpi=150)
print("\nPlot saved as 'causal_structures.png'")

# Save datasets
df_fork.to_csv('fork_data.csv', index=False)
df_collider.to_csv('collider_data.csv', index=False)
df_chain.to_csv('chain_data.csv', index=False)
print("\nDatasets saved as CSV files")
