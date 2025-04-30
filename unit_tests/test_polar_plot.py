import os
import sys
import numpy as np
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
def generate_polar_plot(theta,r, linewidth=1.5,color="b",title="Polar Plot"):
    if not isinstance(theta, (list, tuple, np.ndarray)) or not isinstance(r, (list, tuple, np.ndarray)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(theta) != len(r):
        raise ValueError("Data and labels must have the same length.")
    if len(theta) == 0:
        raise ValueError("theta and r cannot be empty.")

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(theta, r, linewidth=linewidth, color=color)
    ax.set_title(title)
    return fig


# -------- Helpers for Tests --------
def create_random_polar_dataset(seed):
    random.seed(seed)
    np.random.seed(seed)
    length = random.randint(3, 20)  
    theta = np.linspace(0, 2 * np.pi, length).tolist()
    r = [random.uniform(0, 100) for _ in range(length)]
    return theta, r

test_cases = [create_random_polar_dataset(seed) for seed in range(60)]

# --------- Tests Start Here ---------


@pytest.mark.parametrize("theta, r", test_cases)
def test_generate_polar_plot_with_random_data(theta, r):
    fig = generate_polar_plot(theta, r)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b"\x89PNG"  # PNG file magic number

    # Check title
    assert fig.axes[0].get_title() == "Polar Plot"
    assert fig.axes[0].name == 'polar'

def test_polar_plot_custom_title():
    theta = [0, 1, 2]
    r = [10, 20, 30]
    title = "Custom Polar Plot Title"
    fig = generate_polar_plot(theta, r, title=title)
    assert fig.axes[0].get_title() == title


@pytest.mark.parametrize(
    "bad_theta, bad_r, expected_exception",
    [
        ([], [], ValueError),
        ("bad", [1, 2], TypeError),
        ([1, 2], "bad", TypeError),
        ([1], [1, 2], ValueError),
        (object(), [1, 2], TypeError),
        ([1, 2], object(), TypeError),
    ],
)
def test_polar_plot_invalid_inputs_raise_errors(bad_theta, bad_r, expected_exception):
    with pytest.raises(expected_exception):
        generate_polar_plot(bad_theta,bad_r)


@pytest.mark.parametrize(
    "theta, r",
    [
        ([0, np.pi/2, np.pi], [0, 50, 100]),
        (np.linspace(0, 2*np.pi, 50), np.linspace(0, 1, 50)),
        ([0, 1, 2, 3], [1e10, 1e12, 1e14, 1e16]),
        ([0, 1, 2], [-10, 0, 10]),
    ],
)
def test_polar_plot_extreme_values(theta,r):
    fig = generate_polar_plot(theta, r)
    assert fig.axes[0].name == 'polar'

def test_line_color_and_width():
    theta = [0, 1, 2]
    r = [10, 20, 30]
    fig = generate_polar_plot(theta, r, color='red', linewidth=2.5)
    line = fig.axes[0].lines[0]
    assert line.get_color() == 'red'
    assert line.get_linewidth() == 2.5