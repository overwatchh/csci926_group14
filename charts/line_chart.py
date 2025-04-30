import matplotlib.pyplot as plt
import os

def generate_line_chart(x, y, output_path):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path)
    plt.close(fig)
    return output_path
