import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib")),
)

import pytest
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend for testing
from io import BytesIO
import random


# -------- Function Under Test --------
def generate_box_plot(data, labels, title="Box Plot Chart"):
    if not isinstance(data, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(data) != len(labels):
        raise ValueError("Data and labels must have the same length.")
    if not data or not labels:
        raise ValueError("Data and labels cannot be empty.")
    if not all(isinstance(d, (list, tuple)) for d in data):
        raise TypeError("Each item in data must be a list or tuple of numbers.")

    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title(title)
    return fig


# -------- Helpers for Tests --------
def create_random_boxplot_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [
        [random.uniform(0, 100) for _ in range(random.randint(5, 15))]
        for _ in range(length)
    ]
    labels = [f"Label_{i}" for i in range(length)]
    return data, labels


test_cases = [create_random_boxplot_dataset(seed) for seed in range(60)]


# --------- Tests Start Here ---------


@pytest.mark.parametrize("data, labels", test_cases)
def test_generate_box_plot_with_random_data(data, labels):
    fig = generate_box_plot(data, labels)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"  # PNG file magic number

    # Check title
    assert fig.axes[0].get_title() == "Box Plot Chart"

    # Check x-ticks match labels
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(data)


def test_box_plot_custom_title():
    data = [[10, 20, 30], [40, 50, 60]]
    labels = ["Group1", "Group2"]
    title = "Custom Box Plot Title"
    fig = generate_box_plot(data, labels, title=title)
    assert fig.axes[0].get_title() == title


@pytest.mark.parametrize(
    "bad_data, bad_labels, expected_exception",
    [
        ([], [], ValueError),
        ("bad", ["A", "B"], TypeError),
        ([[1, 2]], "bad", TypeError),
        (object(), ["A", "B"], TypeError),
        ([[1, 2]], object(), TypeError),
        ({1: [1, 2]}, ["a"], TypeError),
        ([[1, 2]], {1: "a"}, TypeError),
        ([1, 2, 3], ["A", "B", "C"], TypeError),  # Flat list instead of list of lists
    ],
)
def test_box_plot_invalid_inputs_raise_errors(bad_data, bad_labels, expected_exception):
    with pytest.raises(expected_exception):
        generate_box_plot(bad_data, bad_labels)


@pytest.mark.parametrize(
    "extreme_data, labels",
    [
        ([[0, 0, 0], [0, 0, 0]], ["A", "B"]),
        ([[1e10, 1e12, 1e14], [5e9, 5e11, 5e13]], ["A", "B"]),
        ([[-100, -50, -10], [-200, -150, -100]], ["A", "B"]),
        ([[1, 0, -1], [2, -2, 0]], ["A", "B"]),
    ],
)
def test_box_plot_extreme_values(extreme_data, labels):
    fig = generate_box_plot(extreme_data, labels)
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(extreme_data)


def test_box_plot_xticks_and_box_count():
    data = [[5, 15, 25], [10, 20, 30], [15, 25, 35]]
    labels = ["First", "Second", "Third"]
    fig = generate_box_plot(data, labels)
    ax = fig.axes[0]

    # Check xtick labels match
    xticklabels = [tick.get_text() for tick in ax.get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(data)

    # Check that some lines are drawn (boxplots create multiple Line2D objects)
    # Each box creates multiple lines: whiskers, caps, median, etc.
    # We cannot exactly count boxes, but we can assert that lines exist
    assert len(ax.lines) > 0
