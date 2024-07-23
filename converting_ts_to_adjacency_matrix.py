import pandas as pd
import ts2vg
from time_series_to_visibilty_graph import plot_ts_visibility

# Read in FX data
data = pd.read_csv("AUDNZD.raw_M10_202201030300_202312292350_processed.csv")["<CLOSE>"][
    0:90
].values

# Initialise creating horizontal visibility graphs

natural_graph = ts2vg.NaturalVG()
# natural_graph.build(data) # Building graph for positive direction
natural_graph.build(data * -1)  # Building graph for negative direction

# Create adjacency matrix and plot
adj_matrix = natural_graph.adjacency_matrix()
print(adj_matrix)

plot_ts_visibility(adj_matrix, data, horizontal=False)
