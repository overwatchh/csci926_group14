import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib")))

import pytest
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
from io import BytesIO
import random

def generate_histogram_chart(data, bins, title="Histogram Chart"):
    if not isinstance(data, (list, tuple)) or not isinstance(bins, int):
        raise TypeError("Data must be a list or tuple and bins must be an integer.")
    if not data:
        raise ValueError("Data cannot be empty.")
    if bins <= 0:
        raise ValueError("Bins must be a positive integer.")
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    ax.set_title(title)
    return fig

def create_random_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [random.uniform(0, 100) for _ in range(length)]
    bins = random.randint(1, length)
    return data, bins

test_cases = [create_random_dataset(seed) for seed in range(60)]

@pytest.mark.parametrize("data, bins", test_cases)
def test_generate_chart_with_random_data(data, bins):
    fig = generate_histogram_chart(data, bins)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"
    bars = fig.axes[0].patches
    assert len(bars) == bins
    plt.close(fig)

def test_chart_custom_title():
    data = [1, 2, 3]
    bins = 3
    title = "Custom Hist Title"
    fig = generate_histogram_chart(data, bins, title=title)
    assert fig.axes[0].get_title() == title
    plt.close(fig)

@pytest.mark.parametrize(
    "bad_data, bad_bins, expected_exception",
    [
        ([], 1, ValueError),
        ("bad", 5, TypeError),
        ([1, 2, 3], "bad", TypeError),
        ([1, 2], 0, ValueError),
        ([1, 2], -1, ValueError),
    ],
)
def test_invalid_inputs_raise_errors(bad_data, bad_bins, expected_exception):
    with pytest.raises(expected_exception):
        generate_histogram_chart(bad_data, bad_bins)

@pytest.mark.parametrize(
    "extreme_data, bins",
    [
        ([0, 0, 0], 3),
        ([1e10, 1e12, 1e14], 3),
        ([-100, -50, -10], 3),
        ([1, 0, -1], 3),
    ],
)
def test_chart_extreme_values(extreme_data, bins):
    fig = generate_histogram_chart(extreme_data, bins)
    bars = fig.axes[0].patches
    assert len(bars) == bins
    plt.close(fig)

def test_chart_bar_count():
    data = [5, 15, 25]
    bins = 3
    fig = generate_histogram_chart(data, bins)
    bars = fig.axes[0].patches
    assert len(bars) == bins
    plt.close(fig)
