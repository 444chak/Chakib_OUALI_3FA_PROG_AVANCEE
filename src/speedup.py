import subprocess
import numpy as np
import matplotlib.pyplot as plt
import csv


import pathlib
import argparse

path = pathlib.Path(__file__).parent.absolute()
path = path / "MONTE_CARLO"

dir_out = pathlib.Path(__file__).parent.absolute() / "MONTE_CARLO" / "out"


def run_java(workers, number_of_experiments, total_count):
    file = path / "Main.java"
    subprocess.run(["javac", file])
    result = subprocess.run(
        [
            "java",
            "MONTE_CARLO.Main",
            str(workers),
            str(number_of_experiments),
            str(total_count),
        ],
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")


nb_workers = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 18]


def scalabilite_forte(nb_workers, nb_experiments=10, total_count=1200000):
    speedup_times = []
    for i in nb_workers:
        print(
            "Running Master-Worker with ", i, " workers", "| Total count: ", total_count
        )
        out = run_java(i, nb_experiments, total_count)

        print(out.strip().split("\n")[-1])

        with open(
            pathlib.Path(__file__).parent.absolute() / out.strip().split("\n")[-1]
        ) as f:
            data = csv.reader(f, delimiter="\t")
            header = next(data)  # Skip the header
            data = list(data)

        times = [float(row[header.index("Time")]) for row in data]

        speedup_times.append(np.mean(times))

        print("Mean time (ms): ", np.mean(times))
        print("-----------------")

    # clear the directory
    for f in dir_out.iterdir():
        f.unlink()

    return speedup_times


def plot_scalabilite_forte(nb_workers, speedup_times, speedup2=None, speedup3=None):
    sP = list(map(lambda x: speedup_times[0] / x, speedup_times))
    sP2 = list(map(lambda x: speedup2[0] / x, speedup2)) if speedup2 else None
    sP3 = list(map(lambda x: speedup3[0] / x, speedup3)) if speedup3 else None

    plt.plot(nb_workers, sP, label="Speedup", marker="o")
    if speedup2:
        plt.plot(nb_workers, sP2, label="Speedup (2)", marker="o")
    if speedup3:
        plt.plot(nb_workers, sP3, label="Speedup (3)", marker="o")
    plt.xlabel("Number of workers")
    plt.ylabel("Speedup")
    plt.title("Speedup vs Number of workers")
    plt.grid()
    # perfect speedup
    plt.plot([1, nb_workers[-1]], [1, nb_workers[-1]], "--", label="Perfect Speedup")
    plt.legend()
    plt.axis("equal")
    max_value = max(nb_workers)
    plt.xlim(1, max_value)
    plt.ylim(1, max_value)
    plt.yticks(range(1, max_value + 1))
    plt.xticks(range(1, max_value + 1))
    # adjust the size of the plot
    plt.gcf().set_size_inches(10, 7)
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Run Monte Carlo simulation with multiple workers"
    )
    parser.add_argument(
        "--experiments", type=int, default=10, help="Number of experiments"
    )
    parser.add_argument("--count", type=int, default=1200000000, help="Total count")

    args = parser.parse_args()
    speedup_times = scalabilite_forte(nb_workers, args.experiments, args.count)
    speedup_times2 = scalabilite_forte(nb_workers, args.experiments, args.count // 100)
    speedup_times3 = scalabilite_forte(nb_workers, args.experiments, args.count // 1000)
    plot_scalabilite_forte(nb_workers, speedup_times, speedup_times2, speedup_times3)


if __name__ == "__main__":
    main()
