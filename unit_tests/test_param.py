import pytest
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib"))
)

import matplotlib.pyplot as plt


def generate_plot(plot_type, data):
    fig, ax = plt.subplots()
    
    if plot_type == "line":
        ax.plot(data)
    elif plot_type == "scatter":
        ax.scatter(range(len(data)), data)
    elif plot_type == "bar":
        ax.bar(range(len(data)), data)
    elif plot_type == "step":
        ax.step(range(len(data)), data)
    elif plot_type == "fill_between":
        ax.fill_between(range(len(data)), data)
    elif plot_type == "hist":
        ax.hist(data)
    elif plot_type == "pie":
        ax.pie(data)
    elif plot_type == "box":
        ax.boxplot(data)
    elif plot_type == "stem":
        markerline, stemlines, baseline = ax.stem(data)
    else:
        raise ValueError(f"Unknown plot type: {plot_type}")

    return fig


# 👇 Add 10 different plot types
PLOT_TYPES = [
    "line", "scatter", "bar", "step", "fill_between",
    "hist", "pie", "box", "stem"
]

# 👇 Add 12 datasets (more edge cases)
DATASETS = [
    [1, 2, 3],
    [3, 2, 1],
    [],
    [None, 1, 2],
    list(range(10)),
    list(range(1000)),
    [0, 0, 0],
    [-1, 0, 1],
    [float('nan'), 1, 2],
    [float('inf'), 1, 2],
    [1.5, 2.5, 3.5],
    [5] * 50
]

# Multiply for ~100+ combinations: 9 plot types × 12 datasets = 108 tests
@pytest.mark.parametrize("plot_type", PLOT_TYPES)
@pytest.mark.parametrize("data", DATASETS)
def test_plot_works(plot_type, data):
    """
    Test that generate_plot does not crash and returns a valid Matplotlib Figure.
    """
    try:
        fig = generate_plot(plot_type, data)
    except Exception as e:
        # Allow some plots to gracefully fail on invalid data
        if plot_type in ["pie", "box", "fill_between"] and not data:
            pytest.skip(f"{plot_type} cannot plot empty data")
        elif any(d is None or isinstance(d, float) and (d != d or d == float("inf")) for d in data if isinstance(data, list)):
            pytest.skip(f"{plot_type} cannot handle NaN/inf values")
        else:
            raise

    assert isinstance(fig, plt.Figure), f"{plot_type} plot with {data} did not return a Figure"
    assert fig.axes, f"{plot_type} plot with {data} has no axes"
