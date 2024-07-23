# Applying-Graph-Theory-to-Quantitative-Trading
Exploring the use of visibility graphs in generating trading signals in the FX market

**10 minute data from 03/01/2022 to 29/12/2023 (2 years worth of data, roughly 74,000 data points)**

In the realm of network science, visibility graphs offer a powerful tool for analyzing time series data.  They translate the dynamics of a time series into a network structure, revealing hidden relationships and patterns not readily apparent in the raw data.

Brief overview of how they work:

1. **Nodes and Connections**: Each data point in the time series becomes a node in the visibility graph.  Two nodes are connected by an edge if there exists a "line of sight" between them, meaning no intermediate data points obstruct the view.

2. **Line of Sight**:  Imagine drawing a straight line between two data points.  If no other data point lies above or below this line, the two points are deemed "visible" to each other and a connection is established.

The idea behind this is what these graphs allow us to do. Visibility graphs allow us to:

1. **Uncover Hidden Correlations**: By capturing the interplay between data points, visibility graphs can reveal subtle correlations that might be missed in traditional analysis methods.

2. **Characterise Time Series Dynamics**: The structure of the resulting network can tell us a lot about the underlying dynamics of the time series.  For example, dense networks with many connections may indicate strong dependencies between data points, while sparse networks suggest weaker relationships.

![Positive_visibility_graph](https://github.com/user-attachments/assets/8740f881-d3c4-410e-b6c9-1cfa8bff1d1f)

This is the visibility graph of the first 91 data points from the AUDNZD FX dataset. Notably, the red-lines (visibility lines) are above the price, so the resulting graph contains information about which prices are visible from higher prices. This means it only gives half of the information that it could. Therefore we create a negative version.

![Negative_visibility_graph](https://github.com/user-attachments/assets/6356bc71-12be-4d0c-84a7-c1e201f74e6d)

Conversely, this visibility graph of when the input data is multiplied by -1.

The graphs have different lengths, and we use this later to compare them and build a simple trading rule.

The metric we use to analyse the two graphs is the "average shortest path length" from the networkx library. This is the shortest path length to traverse between nodes.

![Maximum_shortest_path_length](https://github.com/user-attachments/assets/c4ecfc84-2056-42a5-8c35-ab28590073c8)

The maximum average shortest path length is shown above.

![Minimum_shortest_path_length](https://github.com/user-attachments/assets/17c01454-a488-4856-b4c5-25bb8c630f38)

The minimum average shortest path length is shown above.

The price of the minimum shortest path length had the opposite behaviour to the maximum, and every node is linked whereas in the maximum shortest path length only 3 nodes are linked. This means that price at the maximum average shortest path length does not sure much correlation, whereas at the minimum, clear patterns can be seen.

When we put positive and negative visibility plots onto a single graph:
![positive_negative_price_plot](https://github.com/user-attachments/assets/fa035d84-1950-433a-ab03-18dfe99cb3f4)

We can see that the average shortest path length of positive/negative closing price are stationary with each other and is indicative of a possible indicator that we could use.

Therefore, the simple trading rule created is:

1. **LONG**: if positive shortest path length is above the negative.
2. **SHORT**: if negative shortest path length is above the positive.

![log_returns](https://github.com/user-attachments/assets/42825952-8ee1-49fc-b226-745dabfcb4fe)

The cumulative log returns are shown above.
Profit Factors:
1. Long PF 1.09496
2. Short PF 1.09828
3. Combined PF 1.09656

![heatmap](https://github.com/user-attachments/assets/e5c9c67f-de03-4733-b7ff-b8a735e32a1e)

A heatmap of the average shortest path length trading rule with varying lookbacks show a drop off in performance at higher lookbacks but the results seem to be robust.

Drawbacks:
1. Fees and slippage not accounted for.
2. Strategy is in the market 100% of the time.
