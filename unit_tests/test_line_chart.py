import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib")))

import pytest
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
from io import BytesIO
import random

def generate_line_chart(data, labels, title="Line Chart"):
    if not isinstance(data, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(data) != len(labels):
        raise ValueError("Data and labels must have the same length.")
    if not data or not labels:
        raise ValueError("Data and labels cannot be empty.")
    fig, ax = plt.subplots()
    ax.plot(labels, data)
    ax.set_title(title)
    return fig

def create_random_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [random.uniform(0, 100) for _ in range(length)]
    labels = [f"Label_{i}" for i in range(length)]
    return data, labels

test_cases = [create_random_dataset(seed) for seed in range(60)]

@pytest.mark.parametrize("data, labels", test_cases)
def test_generate_chart_with_random_data(data, labels):
    fig = generate_line_chart(data, labels)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"
    assert fig.axes[0].get_title() == "Line Chart"
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(data)
    plt.close(fig)

def test_chart_custom_title():
    data = [10, 20]
    labels = ["X", "Y"]
    title = "Custom Line Title"
    fig = generate_line_chart(data, labels, title=title)
    assert fig.axes[0].get_title() == title
    plt.close(fig)

@pytest.mark.parametrize(
    "bad_data, bad_labels, expected_exception",
    [
        ([], [], ValueError),
        ("bad", ["A", "B"], TypeError),
        ([1, 2], "bad", TypeError),
        ([1, 2], ["A"], ValueError),
        (object(), ["A", "B"], TypeError),
        ([1, 2], object(), TypeError),
        ({1: "a"}, ["a"], TypeError),
        ([1, 2], {1: "a"}, TypeError),
    ],
)
def test_invalid_inputs_raise_errors(bad_data, bad_labels, expected_exception):
    with pytest.raises(expected_exception):
        generate_line_chart(bad_data, bad_labels)

@pytest.mark.parametrize(
    "extreme_data, labels",
    [
        ([0, 0, 0], ["A", "B", "C"]),
        ([1e10, 1e12, 1e14], ["A", "B", "C"]),
        ([-100, -50, -10], ["A", "B", "C"]),
        ([1, 0, -1], ["A", "B", "C"]),
    ],
)
def test_chart_extreme_values(extreme_data, labels):
    fig = generate_line_chart(extreme_data, labels)
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(extreme_data)
    plt.close(fig)

def test_chart_line_count():
    data = [5, 15, 25]
    labels = ["First", "Second", "Third"]
    fig = generate_line_chart(data, labels)
    lines = fig.axes[0].lines
    assert len(lines) == 1
    plt.close(fig)
