import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../mathplotlib"))
)

import matplotlib.pyplot as plt


def test_basic_plot():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    assert len(ax.lines) == 1
