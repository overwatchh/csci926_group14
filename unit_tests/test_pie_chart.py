import os
import sys
 

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../matplotlib")),
)

import pytest
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import random

def generate_pie_chart(data, labels, title="Pie Chart",colors=None):
    if not isinstance(data, (list, tuple)) or not isinstance(labels, (list, tuple)):
        raise TypeError("Data and labels must be lists or tuples.")
    if len(data) != len(labels):
        raise ValueError("Data and labels must have the same length.")
    if not data or not labels:
        raise ValueError("Data and labels cannot be empty.")
    if any(x < 0 for x in data):
        raise ValueError("Wedge sizes 'x' must be non negative values.")
    if all(x == 0 for x in data):
        raise ValueError("All data values are zero, cannot create a pie chart.")
    
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors)
    ax.set_title(title)
    return fig

def create_random_dataset(seed):
    random.seed(seed)
    length = random.randint(1, 10)
    data = [random.uniform(0, 100) for _ in range(length)]
    labels = [f"Label_{i}" for i in range(length)]
    colors = [f"#{random.randint(0,255):02x}{random.randint(0,255):02x}{random.randint(0,255):02x}" 
              for _ in range(length)]
    return data, labels,colors

test_cases = [create_random_dataset(seed) for seed in range(60)]

#-------------------------test-----------------------------------
@pytest.mark.parametrize("data, labels,colors", test_cases)
def test_generate_pie_chart_with_random_data(data, labels,colors):
    fig = generate_pie_chart(data, labels,colors=colors)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    assert buf.read(4) == b'\x89PNG' 
    #check title
    assert fig.axes[0].get_title() == "Pie Chart"
    #check labels and the number of sectors
    labels_in_chart = [patch.get_label() for patch in fig.axes[0].patches]
    assert labels_in_chart == labels
    assert len(labels_in_chart) == len(data)
    #check if colors are applied
    patches = fig.axes[0].patches
   # Convert string color "#rrggbb" to RGBA tuple
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4)) + (1.0,)

    for patch, expected_color in zip(patches, colors):
        expected_rgba = hex_to_rgb(expected_color)
        actual_rgba = patch.get_facecolor()
        assert all(abs(a - b) < 0.05 for a, b in zip(actual_rgba, expected_rgba))  # allow slight float error

 
def test_pie_chart_custom_title():
    data = [15, 30]
    labels = ["A", "B"]
    title = "Custom Pie Title"
    fig = generate_pie_chart(data, labels, title=title)
    assert fig.axes[0].get_title() == title

@pytest.mark.parametrize("bad_data, bad_labels, expected_exception", [
    ([], [], ValueError),
    ("bad", ["A", "B"], TypeError),
    ([1, 2], "bad", TypeError),
    ([1, 2], ["A"], ValueError),
    (object(), ["A", "B"], TypeError),
    ([1, 2], object(), TypeError),
    ({1: 'a'}, ['a'], TypeError),
    ([1, 2], {1: 'a'} , TypeError),
    ([0, 0, 0], ["A", "B", "C"], ValueError),
    ([0, -1], ["A", "B"], ValueError),
])
def test_pie_chart_invalid_inputs_raise_errors(bad_data, bad_labels, expected_exception):
    with pytest.raises(expected_exception):
        generate_pie_chart(bad_data, bad_labels)

@pytest.mark.parametrize("extreme_data, labels", [
    ([1e10, 1e12, 1e14], ["A", "B", "C"]),
    ([0.1, 0.2, 0.3], ["A", "B", "C"]),
    ([1, 0, 1], ["A", "B", "C"]),
])
def test_pie_chart_chart_extreme_values(extreme_data, labels):
    fig = generate_pie_chart(extreme_data, labels)
    labels_in_chart = [patch.get_label() for patch in fig.axes[0].patches]
    assert labels_in_chart == labels
    assert len(labels_in_chart) == len(extreme_data)

