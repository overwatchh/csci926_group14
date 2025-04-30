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
def generate_area_chart(data, labels, title="Area Chart"):
    if not isinstance(data, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(data) != len(labels):
        raise ValueError("Data and labels must have the same length.")
    if not data or not labels:
        raise ValueError("Data and labels cannot be empty.")

    fig, ax = plt.subplots()
    ax.fill_between(range(len(data)), data, step="mid", alpha=0.5)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_title(title)
    return fig


# -------- Helpers for Tests --------
def create_random_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [random.uniform(0, 100) for _ in range(length)]
    labels = [f"Label_{i}" for i in range(length)]
    return data, labels


test_cases = [create_random_dataset(seed) for seed in range(60)]


# --------- Tests Start Here ---------


@pytest.mark.parametrize("data, labels", test_cases)
def test_generate_area_chart_with_random_data(data, labels):
    fig = generate_area_chart(data, labels)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"  # PNG file magic number

    # Check title
    assert fig.axes[0].get_title() == "Area Chart"

    # Check x-ticks match labels
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    # Matplotlib can sometimes add empty ticks if the plot is too small, filter out empty labels
    xticklabels = [label for label in xticklabels if label]
    assert xticklabels == labels
    assert len(xticklabels) == len(data)


def test_area_chart_custom_title():
    data = [10, 20]
    labels = ["X", "Y"]
    title = "Custom Area Title"
    fig = generate_area_chart(data, labels, title=title)
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
def test_invalid_inputs_raise_errors_area_chart(
    bad_data, bad_labels, expected_exception
):
    with pytest.raises(expected_exception):
        generate_area_chart(bad_data, bad_labels)


@pytest.mark.parametrize(
    "extreme_data, labels",
    [
        ([0, 0, 0], ["A", "B", "C"]),
        ([1e10, 1e12, 1e14], ["A", "B", "C"]),
        ([-100, -50, -10], ["A", "B", "C"]),
        ([1, 0, -1], ["A", "B", "C"]),
    ],
)
def test_area_chart_extreme_values(extreme_data, labels):
    fig = generate_area_chart(extreme_data, labels)
    xticklabels = [tick.get_text() for tick in fig.axes[0].get_xticklabels()]
    xticklabels = [label for label in xticklabels if label]
    assert xticklabels == labels
    assert len(xticklabels) == len(extreme_data)


def test_area_chart_xticks_and_patch_count():
    data = [5, 15, 25]
    labels = ["First", "Second", "Third"]
    fig = generate_area_chart(data, labels)
    ax = fig.axes[0]

    # Check xticks
    xticklabels = [tick.get_text() for tick in ax.get_xticklabels()]
    xticklabels = [label for label in xticklabels if label]
    assert xticklabels == labels

    # Check that the plot has 1 PolyCollection (area under the curve)
    collections = ax.collections
    assert len(collections) == 1
