import pandas as pd, numpy as np
import statsmodels.api as sm

sectors = ["XLC","XLY","XLP","XLE","XLF","XLV","XLI","XLB","XLRE","XLK","XLU"]

data = pd.read_csv("../data/prices.csv", index_col=0, parse_dates=True)
rets = data[sectors + ["SPY"]].pct_change().dropna() * 100

Y = rets[sectors].values                 # (n, 11)
X = sm.add_constant(rets["SPY"].values)  # (n, 2)

B_hat   = np.linalg.lstsq(X, Y, rcond=None)[0]   # (2, 11)
resids  = Y - X @ B_hat
Sigma_y = resids.T @ resids / len(resids)        # residual (idiosyncratic) covariance, (11, 11)

print("Residual covariance diagonal (idiosyncratic variances):")
print(pd.Series(np.diag(Sigma_y), index=sectors).round(3))

# Off-diagonals of Sigma_y tell us whether sectors still co-move after removing
# the shared SPY factor -- that's the "dependence on each other" question.
corr_y = Sigma_y / np.sqrt(np.outer(np.diag(Sigma_y), np.diag(Sigma_y)))
corr_df = pd.DataFrame(corr_y, index=sectors, columns=sectors)

print("\nResidual correlation matrix (off-diagonals = leftover cross-sector dependence):")
print(corr_df.round(2))

off_diag = corr_df.where(~np.eye(len(sectors), dtype=bool))
stacked = off_diag.stack().sort_values(key=lambda s: s.abs(), ascending=False)
pairs_seen = set()
print("\nTop residual correlation pairs (|corr|, after removing SPY factor):")
for (a, b), v in stacked.items():
    if (b, a) in pairs_seen:
        continue
    pairs_seen.add((a, b))
    print(f"  {a:5s} - {b:5s}: {v:+.3f}")
    if len(pairs_seen) >= 10:
        break
