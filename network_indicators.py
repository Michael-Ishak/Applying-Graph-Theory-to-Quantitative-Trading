import numpy as np
import pandas as pd
import networkx as nx
import ts2vg
import matplotlib.pyplot as plt
import seaborn as sns


def shortest_path_length(close: np.array, lookback: int):
    """
    This function calculates the average shortest path length for positive and negative
    transformations of a given time series data.

    Args:
        close (np.array): A NumPy array representing the closing prices of a time series.
        lookback (int): The number of past data points to consider for calculating the shortest path.

    Returns:
        tuple[np.ndarray, np.ndarray]: A tuple containing two NumPy arrays.
            - avg_short_dist_p (np.ndarray): An array of average shortest path lengths for the positive transformed data.
            - avg_short_dist_n (np.ndarray): An array of average shortest path lengths for the negative transformed data.

    Raises:
        ValueError: If the lookback value is less than 1.
    """
    avg_short_dist_p = np.zeros(len(close))
    avg_short_dist_n = np.zeros(len(close))

    avg_short_dist_p[:] = np.nan
    avg_short_dist_n[:] = np.nan

    for i in range(lookback, len(close)):
        dat = close[i - lookback + 1 : i + 1]

        pos = ts2vg.NaturalVG()
        pos.build(dat)

        neg = ts2vg.NaturalVG()
        neg.build(-dat)

        neg = neg.as_networkx()
        pos = pos.as_networkx()

        avg_short_dist_p[i] = nx.average_shortest_path_length(pos)
        avg_short_dist_n[i] = nx.average_shortest_path_length(neg)

    return avg_short_dist_p, avg_short_dist_n


if __name__ == "__main__":
    data = pd.read_csv("AUDNZD.raw_M10_202201030300_202312292350_processed.csv")

    data["r"] = np.log(data["<CLOSE>"]).diff().shift(-1)
    # Compute shortest average path length for last 12 vals
    pos, neg = shortest_path_length(data["<CLOSE>"].to_numpy(), 12)
    data["pos"] = pos
    data["neg"] = neg

    # Compute signals
    data["long_sig"] = 0
    data["short_sig"] = 0
    data.loc[data["pos"] > data["neg"], "long_sig"] = 1
    data.loc[data["pos"] < data["neg"], "short_sig"] = -1
    data["combined_sig"] = data["long_sig"] + data["short_sig"]

    # Compute returns
    data["long_ret"] = data["long_sig"] * data["r"]
    data["short_ret"] = data["short_sig"] * data["r"]
    data["comb_ret"] = data["combined_sig"] * data["r"]

    # Compute profit factor
    long_pf = (
        data[data["long_ret"] > 0]["long_ret"].sum()
        / data[data["long_ret"] < 0]["long_ret"].abs().sum()
    )
    short_pf = (
        data[data["short_ret"] > 0]["short_ret"].sum()
        / data[data["short_ret"] < 0]["short_ret"].abs().sum()
    )
    combined_pf = (
        data[data["comb_ret"] > 0]["comb_ret"].sum()
        / data[data["comb_ret"] < 0]["comb_ret"].abs().sum()
    )

    print("Long PF", long_pf)
    print("Short PF", short_pf)
    print("Combined PF", combined_pf)

    # Plot cumulative log return
    plt.style.use("dark_background")
    data["long_ret"].cumsum().plot(label="Long")
    data["short_ret"].cumsum().plot(label="Short")
    data["comb_ret"].cumsum().plot(label="Combined")
    plt.legend()
    plt.ylabel("Log Returns")
    plt.xlabel("Data Point")
    plt.show()

    # # HEATMAP OF PARAMETERS
    # heatmap_df = pd.DataFrame()

    # for lb in range(6, 25):
    #     print(lb)
    #     # Compute shortest average path length for last 12 vals
    #     pos, neg = shortest_path_length(data["<CLOSE>"].to_numpy(), lb)
    #     data["pos"] = pos
    #     data["neg"] = neg

    #     # Compute signals
    #     data["long_sig"] = 0
    #     data["short_sig"] = 0
    #     data.loc[data["pos"] > data["neg"], "long_sig"] = 1
    #     data.loc[data["pos"] < data["neg"], "short_sig"] = -1
    #     data["combined_sig"] = data["long_sig"] + data["short_sig"]

    #     # Compute returns
    #     data["long_ret"] = data["long_sig"] * data["r"]
    #     data["short_ret"] = data["short_sig"] * data["r"]
    #     data["comb_ret"] = data["combined_sig"] * data["r"]

    #     # Compute profit factor
    #     long_pf = (
    #         data[data["long_ret"] > 0]["long_ret"].sum()
    #         / data[data["long_ret"] < 0]["long_ret"].abs().sum()
    #     )
    #     short_pf = (
    #         data[data["short_ret"] > 0]["short_ret"].sum()
    #         / data[data["short_ret"] < 0]["short_ret"].abs().sum()
    #     )
    #     combined_pf = (
    #         data[data["comb_ret"] > 0]["comb_ret"].sum()
    #         / data[data["comb_ret"] < 0]["comb_ret"].abs().sum()
    #     )

    #     heatmap_df.loc[lb, "Long"] = long_pf
    #     heatmap_df.loc[lb, "Short"] = short_pf
    #     heatmap_df.loc[lb, "Combined"] = combined_pf

    # plt.style.use("dark_background")
    # sns.heatmap(heatmap_df.T, annot=True)
    # plt.xlabel("Visibility Graph Lookback")
    # plt.show()
