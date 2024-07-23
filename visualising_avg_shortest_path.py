import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import ts2vg
from time_series_to_visibilty_graph import plot_ts_visibility
from network_indicators import shortest_path_length

data = pd.read_csv("AUDNZD.raw_M10_202201030300_202312292350_processed.csv")

# Get close prices and calculate shortest path lengths
lookback = 12
close_arr = data["<CLOSE>"].to_numpy()
pos, neg = shortest_path_length(close_arr, lookback)
data["pos"] = pos
data["neg"] = neg

# Find indices for maximum and minimum average shortest path
max_idx = data["pos"].idxmax()
min_idx = data["pos"].idxmin()

# Extract data for max and min periods
max_dat = data.iloc[max_idx - lookback + 1 : max_idx + 1]["<CLOSE>"].to_numpy()
min_dat = data.iloc[min_idx - lookback + 1 : min_idx + 1]["<CLOSE>"].to_numpy()

# Plot visibility graph for period with maximum and minimum average shortest paths
g = ts2vg.NaturalVG()
g.build(max_dat)
plot_ts_visibility(g.adjacency_matrix(), max_dat)

g = ts2vg.NaturalVG()
g.build(min_dat)
plot_ts_visibility(g.adjacency_matrix(), min_dat)

# Plot graphs
np.log(data["<CLOSE>"]).plot(color="white", label="data points", alpha=0.6)
plt.twinx()
data["neg"].plot(color="red", label="neg", alpha=0.8)
data["pos"].plot(color="green", label="pos", alpha=0.8)
plt.legend()
plt.xlabel("Data Point")
plt.ylabel("Price")
plt.show()
