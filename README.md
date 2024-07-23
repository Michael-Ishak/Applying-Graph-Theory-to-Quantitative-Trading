# Applying-Graph-Theory-to-Quantitative-Trading
Exploring the use of visibility graphs in generating trading signals in the FX market

**10 minute data from 03/01/2022 to 29/12/2023 (2 years worth of data)**

In the realm of network science, visibility graphs offer a powerful tool for analyzing time series data.  They translate the dynamics of a time series into a network structure, revealing hidden relationships and patterns not readily apparent in the raw data.

Brief overview of how they work:

1. **Nodes and Connections**: Each data point in the time series becomes a node in the visibility graph.  Two nodes are connected by an edge if there exists a "line of sight" between them, meaning no intermediate data points obstruct the view.

2. **Line of Sight**:  Imagine drawing a straight line between two data points.  If no other data point lies above or below this line, the two points are deemed "visible" to each other and a connection is established.
