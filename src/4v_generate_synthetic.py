import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression


class CausalModel:
    def __init__(self, n_samples=1000):
        self.n = n_samples

    def generate_fork(self):
        """Fork structure: X <- W -> Y and W -> Z"""
        W = np.random.randn(self.n)
        X = 2 * W + np.random.randn(self.n) * 0.5
        Y = -1.5 * W + np.random.randn(self.n) * 0.5
        Z = 1.2 * W + np.random.randn(self.n) * 0.5
        return {'W': W, 'X': X, 'Y': Y, 'Z': Z}

    def generate_collider(self):
        """Collider structure: X -> W <- Y and W -> Z"""
        X = np.random.randn(self.n)
        Y = np.random.randn(self.n)
        W = 1.5 * X + 2 * Y + np.random.randn(self.n) * 0.5
        Z = 1.3 * W + np.random.randn(self.n) * 0.5
        return {'W': W, 'X': X, 'Y': Y, 'Z': Z}

    def generate_chain(self):
        """Chain structure: X -> W -> Y -> Z"""
        X = np.random.randn(self.n)
        W = 1.5 * X + np.random.randn(self.n) * 0.5
        Y = 2 * W + np.random.randn(self.n) * 0.5
        Z = 1.2 * Y + np.random.randn(self.n) * 0.5
        return {'W': W, 'X': X, 'Y': Y, 'Z': Z}


# Generate datasets
model = CausalModel(n_samples=1000)

fork_data = model.generate_fork()
collider_data = model.generate_collider()
chain_data = model.generate_chain()

df_fork = pd.DataFrame(fork_data)
df_collider = pd.DataFrame(collider_data)
df_chain = pd.DataFrame(chain_data)

lr = LinearRegression()

print("=== FOUR-VARIABLE FORK (X, Y, Z share W) ===")
print(f"Cor(X,Y): {pearsonr(df_fork['X'], df_fork['Y'])[0]:.3f}")
print(f"Cor(X,Z): {pearsonr(df_fork['X'], df_fork['Z'])[0]:.3f}")

# Condition on W
lr.fit(df_fork[['W']], df_fork['X'])
X_res = df_fork['X'] - lr.predict(df_fork[['W']])
lr.fit(df_fork[['W']], df_fork['Y'])
Y_res = df_fork['Y'] - lr.predict(df_fork[['W']])
print(f"Partial Cor(X,Y|W): {pearsonr(X_res, Y_res)[0]:.3f} (should be ~0)")


print("\n=== FOUR-VARIABLE COLLIDER (X → W ← Y → Z) ===")
print(f"Cor(X,Y): {pearsonr(df_collider['X'], df_collider['Y'])[0]:.3f} (should be ~0)")

# Conditioning on W induces dependence
lr.fit(df_collider[['W']], df_collider['X'])
X_res = df_collider['X'] - lr.predict(df_collider[['W']])
lr.fit(df_collider[['W']], df_collider['Y'])
Y_res = df_collider['Y'] - lr.predict(df_collider[['W']])
print(f"Partial Cor(X,Y|W): {pearsonr(X_res, Y_res)[0]:.3f} (should be non-zero)")


print("\n=== FOUR-VARIABLE CHAIN (X → W → Y → Z) ===")
print(f"Cor(X,Z): {pearsonr(df_chain['X'], df_chain['Z'])[0]:.3f}")

# Conditioning on mediators blocks association
lr.fit(df_chain[['W','Y']], df_chain['X'])
X_res = df_chain['X'] - lr.predict(df_chain[['W','Y']])
lr.fit(df_chain[['W','Y']], df_chain['Z'])
Z_res = df_chain['Z'] - lr.predict(df_chain[['W','Y']])
print(f"Partial Cor(X,Z|W,Y): {pearsonr(X_res, Z_res)[0]:.3f} (should be ~0)")


# -------- Visualization --------
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].scatter(df_fork['X'], df_fork['Y'], alpha=0.5)
axes[0].set_title('Fork: X ← W → Y and W -> Z')
axes[0].set_xlabel('X')
axes[0].set_ylabel('Y')

axes[1].scatter(df_collider['X'], df_collider['Y'], alpha=0.5)
axes[1].set_title('Collider: X -> W <- Y and W -> Z')
axes[1].set_xlabel('X')
axes[1].set_ylabel('Y')

axes[2].scatter(df_chain['X'], df_chain['Z'], alpha=0.5)
axes[2].set_title('Chain: X → W → Y → Z')
axes[2].set_xlabel('X')
axes[2].set_ylabel('Z')

plt.tight_layout()
plt.savefig('four_variable_causal_structures.png', dpi=150)
print("\nPlot saved as 'four_variable_causal_structures.png'")


# Save datasets
df_fork.to_csv('fork_data_4var.csv', index=False)
df_collider.to_csv('collider_data_4var.csv', index=False)
df_chain.to_csv('chain_data_4var.csv', index=False)

print("\nDatasets saved as CSV files")
