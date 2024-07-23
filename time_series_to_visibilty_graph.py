import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches


def plot_ts_visibility(
    network: np.array, data: np.array, times: np.array = None, horizontal: bool = False
):
    """
    This function visualizes a time series along with its corresponding visibility graph.

    Args:
        network (np.array): A 2D NumPy array representing the visibility network.
            - 1.0 indicates a connection between two data points.
            - 0.0 indicates no connection.
        data (np.array): A 1D NumPy array representing the time series data.
        times (np.array, optional): A 1D NumPy array representing the time points
            corresponding to the data. If not provided, the function will use the
            range of the data length.
        horizontal (bool, optional): A flag indicating whether to plot visibility
            lines horizontally or diagonally. Defaults to False (diagonal).

    Returns:
        None. This function creates a matplotlib plot and displays it.
    """
    # If times are not provided, use range of data length
    if times is None:
        times = np.arange(len(data))

    plt.style.use("dark_background")
    fig, axs = plt.subplots(2, 1, sharex=True)

    # Find all connections in the network
    connections = np.argwhere(network == 1.0)

    # Plot visibility lines
    if horizontal:
        for i, j in connections:
            if i < j:  # Avoid having multiple lines
                axs[0].plot(
                    [times[i], times[j]], [data[i], data[i]], color="red", alpha=0.8
                )
                axs[0].plot(
                    [times[i], times[j]], [data[j], data[j]], color="red", alpha=0.8
                )
    else:
        # Plot diagonal lines for visibility
        lines = np.array(
            [[times[i], times[j], data[i], data[j]] for i, j in connections if i < j]
        )
        if len(lines) > 0:
            axs[0].plot(lines[:, 0:2].T, lines[:, 2:4].T, color="red", alpha=0.8)

    axs[0].plot(times, data)
    axs[0].set_xlabel("Data Point")
    axs[0].set_ylabel("Instrument Value")
    axs[0].set_title("Time Series with Visibility Graph")
    axs[0].get_xaxis().set_ticks(list(times))

    # # Plot visibility graph
    for i in range(len(data)):
        axs[1].plot(times[i], 0, marker="o", color="orange")

    for i in range(len(data)):
        for j in range(i, len(data)):
            if network[i, j] == 1.0:
                Path = mpath.Path
                mid_time = (times[j] + times[i]) / 2.0
                diff = abs(times[j] - times[i])
                pp1 = mpatches.PathPatch(
                    Path(
                        [(times[i], 0), (mid_time, diff), (times[j], 0)],
                        [Path.MOVETO, Path.CURVE3, Path.CURVE3],
                    ),
                    fc="none",
                    transform=axs[1].transData,
                    alpha=0.5,
                )
                axs[1].add_patch(pp1)
    axs[1].get_yaxis().set_ticks([])
    axs[1].get_xaxis().set_ticks(list(times))
    axs[1].set_xlabel("Node")
    axs[1].set_ylabel("Visibility")
    axs[1].set_title("Visibility Graph")
    plt.show()
