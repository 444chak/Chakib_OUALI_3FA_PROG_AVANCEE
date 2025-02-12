import subprocess
import numpy as np
import matplotlib.pyplot as plt
import csv
import time


import pathlib
import argparse

path = pathlib.Path(__file__).parent.absolute()
path = path / "MONTE_CARLO"

dir_out = pathlib.Path(__file__).parent.absolute() / "MONTE_CARLO" / "out"


def run_java(workers, number_of_experiments, total_count, faible=False, ass102=False):
    file = path / "Main.java"
    algo = "pi" if not ass102 else "ass102"
    result = subprocess.run(
        [
            "java",
            file,
            str(workers),
            str(number_of_experiments),
            str(total_count * workers if faible else total_count),
            str(algo),
        ],
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")


# nb_workers = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 18]
nb_workers = [1, 2, 3, 4, 5, 6, 8]


def scalabilite(
    nb_workers, nb_experiments=10, total_count=1200000, faible=False, ass102=False
):
    speedup_times = []
    for i in nb_workers:
        print(
            "Running Master-Worker with ", i, " workers", "| Total count: ", total_count
        )
        out = run_java(i, nb_experiments, total_count, faible, ass102)

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


def plot_scalabilite(
    nb_workers, speedup_times, speedup2=None, speedup3=None, faible=False
):
    sP = list(map(lambda x: speedup_times[0] / x, speedup_times))
    sP2 = list(map(lambda x: speedup2[0] / x, speedup2)) if speedup2 else None
    sP3 = list(map(lambda x: speedup3[0] / x, speedup3)) if speedup3 else None

    plt.plot(nb_workers, sP, label="Speedup Sockets", marker="o")
    if speedup2:
        plt.plot(nb_workers, sP2, label="Speedup Pi.java", marker="o")
    if speedup3:
        plt.plot(nb_workers, sP3, label="Speedup Ass102.java", marker="o")
    plt.xlabel("Number of workers")
    plt.ylabel("Speedup")
    title = faible and "Scalabilité faible" or "Scalabilité forte"
    plt.title(title)
    plt.grid()
    # perfect speedup
    if not faible:
        plt.plot(
            [1, nb_workers[-1]], [1, nb_workers[-1]], "--", label="Perfect Speedup"
        )
        plt.legend()
        plt.axis("equal")
        max_value = max(nb_workers)
        plt.xlim(0, max_value)
        plt.ylim(0, max_value)
        plt.yticks(range(1, max_value + 1))
        plt.xticks(range(1, max_value + 1))
    if faible:
        plt.plot(
            [1, nb_workers[-1]],
            [0.5, 0.5],
            "--",
        )
        plt.legend()
        plt.xlim(1, max(nb_workers))
        plt.ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.xticks(range(1, max(nb_workers) + 1))
    # adjust the size of the plot
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Run Monte Carlo simulation with multiple workers"
    )
    parser.add_argument(
        "--experiments", type=int, default=10, help="Number of experiments"
    )
    parser.add_argument("--count", type=int, default=120000000, help="Total count")
    parser.add_argument("--faible", type=bool, default=False, help="Faible")

    args = parser.parse_args()
    speedup_times = scalabilite(nb_workers, args.experiments, args.count, args.faible)
    speedup_times2 = scalabilite(
        nb_workers, args.experiments, args.count // 100, args.faible
    )
    speedup_times3 = scalabilite(
        nb_workers, args.experiments, args.count // 1000, args.faible
    )
    plot_scalabilite(nb_workers, speedup_times, speedup_times2, speedup_times3)


def scalabilite_sockets(
    nb_workers, nb_experiments=10, total_count=1200000, faible=False
):
    speedup_times = []

    for i in nb_workers:
        ports = [25545 + i for i in range(i)]
        workers = [
            subprocess.Popen(
                ["java", path / "Sockets" / "WorkerSocket.java", str(port)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            for port in ports
        ]
        time.sleep(1)
        master = subprocess.run(
            [
                "java",
                path / "Sockets" / "MasterSocket.java",
                str(i),
                str(total_count),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        with open(
            pathlib.Path(__file__).parent.absolute()
            / master.stdout.decode("utf-8").strip().split("\n")[-1]
        ) as f:
            data = csv.reader(f, delimiter="\t")
            header = next(data)
            data = list(data)

        times = [float(row[header.index("Time")]) for row in data]

        speedup_times.append(np.mean(times))

        for worker in workers:
            worker.kill()

    return speedup_times


if __name__ == "__main__":
    # plot_scalabilite(
    #     nb_workers,
    #     scalabilite(nb_workers, faible=True, total_count=12000000),
    #     faible=True,
    # )

    sp_sockets = scalabilite_sockets(nb_workers, total_count=120000000)
    sp_normal = scalabilite(nb_workers, total_count=120000000)
    sp_ass102 = scalabilite(nb_workers, total_count=120000000, ass102=True)
    plot_scalabilite(nb_workers, sp_normal, sp_sockets, sp_ass102)
