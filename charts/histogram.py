import matplotlib.pyplot as plt
import os

def generate_histogram(data, bins, output_path):
    fig, ax = plt.subplots()
    ax.hist(data, bins=bins)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
