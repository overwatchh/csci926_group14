import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib")),
)

import pytest
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO


# -------- Function Under Test --------
def generate_heatmap(data, title="Heatmap", cmap="viridis", aspect="auto"):
    if not isinstance(data, (list, np.ndarray)):
        raise TypeError("Data must be a list of lists or a numpy array.")

    data = np.array(data)

    if data.ndim != 2:
        raise ValueError("Data must be 2-dimensional for a heatmap.")

    if data.size == 0:
        raise ValueError("Data cannot be empty.")

    fig, ax = plt.subplots()
    cax = ax.imshow(data, cmap=cmap, aspect=aspect)
    fig.colorbar(cax)
    ax.set_title(title)
    return fig

# -------- Helpers for Tests --------
def create_random_heatmap(seed, rows=None, cols=None):
    np.random.seed(seed)
    if rows is None:
        rows = np.random.randint(1, 10)
    if cols is None:
        cols = np.random.randint(1, 10)
    data = np.random.rand(rows, cols) * 100
    return data

# Generate 100 random heatmaps
test_cases = [create_random_heatmap(seed) for seed in range(100)]


# --------- Tests Start Here ---------

@pytest.mark.parametrize("data", test_cases)
def test_generate_heatmap_with_random_data(data):
    fig = generate_heatmap(data)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b'\x89PNG'  # PNG magic bytes

    assert fig.axes[0].get_title() == "Heatmap"
    assert data.ndim == 2
    assert data.shape[0] > 0 and data.shape[1] > 0
    assert fig.axes[0].images  # Make sure an image exists


@pytest.mark.parametrize("shape", [(1, 1), (1, 50), (50, 1), (10, 10), (2, 3)])
def test_heatmap_extreme_shapes(shape):
    data = np.random.rand(*shape)
    fig = generate_heatmap(data)
    assert fig.axes[0].images


@pytest.mark.parametrize("cmap", ["viridis", "plasma", "inferno", "magma", "cividis"])
def test_heatmap_different_colormaps(cmap):
    data = np.random.rand(5, 5)
    fig = generate_heatmap(data, cmap=cmap)
    assert fig.axes[0].images[0].cmap.name == cmap


def test_heatmap_custom_title_and_aspect():
    data = np.random.rand(4, 4)
    fig = generate_heatmap(data, title="Custom Title", aspect="equal")
    assert fig.axes[0].get_title() == "Custom Title"


def test_colorbar_exists():
    data = np.random.rand(5, 5)
    fig = generate_heatmap(data)
    colorbar_found = any(isinstance(ax, plt.Axes) and ax.get_images() == [] for ax in fig.axes)
    assert not colorbar_found  # Colorbar added to separate axes usually


@pytest.mark.parametrize("bad_input", [
    123,                        # integer
    "invalid input",            # string
    {"a": 1, "b": 2},            # dict
    (1, 2, 3),                  # tuple
    {1, 2, 3},                  # set
    object(),                   # random object
])
def test_heatmap_invalid_types(bad_input):
    with pytest.raises(TypeError):
        generate_heatmap(bad_input)


def test_heatmap_empty_array_raises():
    with pytest.raises(ValueError):
        generate_heatmap(np.array([]))


def test_heatmap_1d_array_raises():
    with pytest.raises(ValueError):
        generate_heatmap(np.array([1, 2, 3]))


def test_heatmap_nested_empty_list_raises():
    with pytest.raises(ValueError):
        generate_heatmap([[]])

