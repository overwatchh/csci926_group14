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
def generate_stem_plot(data, labels, title="Stem Plot"):
    if not isinstance(data, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(data) != len(labels):
        raise ValueError("Data and labels must have the same length.")
    if not data or not labels:
        raise ValueError("Data and labels cannot be empty.")

    fig, ax = plt.subplots()
    ax.stem(range(len(data)), data)  # <-- FIX: removed use_line_collection
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title(title)
    return fig


# -------- Helpers for Tests --------
def create_random_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [random.uniform(-100, 100) for _ in range(length)]
    labels = [f"Label_{i}" for i in range(length)]
    return data, labels


test_cases = [create_random_dataset(seed) for seed in range(60)]


# --------- Tests Start Here ---------


@pytest.mark.parametrize("data, labels", test_cases)
def test_generate_stem_plot_with_random_data(data, labels):
    fig = generate_stem_plot(data, labels)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"  # PNG file magic number

    # Check title
    assert fig.axes[0].get_title() == "Stem Plot"

    # Check x-ticks match labels
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(data)


def test_stem_plot_custom_title():
    data = [10, 20]
    labels = ["X", "Y"]
    title = "Custom Stem Plot Title"
    fig = generate_stem_plot(data, labels, title=title)
    assert fig.axes[0].get_title() == title


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
def test_stem_plot_invalid_inputs_raise_errors(
    bad_data, bad_labels, expected_exception
):
    with pytest.raises(expected_exception):
        generate_stem_plot(bad_data, bad_labels)


@pytest.mark.parametrize(
    "extreme_data, labels",
    [
        ([0, 0, 0], ["A", "B", "C"]),
        ([1e10, 1e12, 1e14], ["A", "B", "C"]),
        ([-100, -50, -10], ["A", "B", "C"]),
        ([1, 0, -1], ["A", "B", "C"]),
    ],
)
def test_stem_plot_extreme_values(extreme_data, labels):
    fig = generate_stem_plot(extreme_data, labels)
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    assert xticklabels == labels
    assert len(xticklabels) == len(extreme_data)


def test_stem_plot_xticklabels_and_marker_count():
    data = [5, 15, 25]
    labels = ["First", "Second", "Third"]
    fig = generate_stem_plot(data, labels)
    ax = fig.axes[0]

    # Find the markerline
    markerlines = [
        child
        for child in ax.get_children()
        if isinstance(child, plt.Line2D) and child.get_marker() != "None"
    ]
    assert len(markerlines) >= 1  # At least one Line2D with markers

    # Now check how many points exist inside the markerline
    markerline = markerlines[0]
    num_points = len(markerline.get_xdata())
    assert num_points == len(data)

    # Also check xticklabels
    xticklabels = [tick.get_text() for tick in ax.get_xticklabels()]
    assert xticklabels == labels
