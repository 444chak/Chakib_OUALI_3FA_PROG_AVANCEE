import subprocess
import numpy as np
import matplotlib.pyplot as plt
import csv


import pathlib

path = pathlib.Path(__file__).parent.absolute()
path = path / "MONTE_CARLO"

NUMBER_OF_EXPERIMENTS = 10
TOTAL_COUNT = 1200


def run_java(workers):
    file = path / "Main.java"
    subprocess.run(["javac", file])
    result = subprocess.run(
        [
            "java",
            "MONTE_CARLO.Main",
            str(workers),
            str(NUMBER_OF_EXPERIMENTS),
            str(TOTAL_COUNT),
        ],
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")


speedup_times = []

nb_workers = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 18]

for i in nb_workers:
    out = run_java(i)
    print("-----------------")
    print(out.strip().split("\n")[-1])

    with open(
        pathlib.Path(__file__).parent.absolute() / out.strip().split("\n")[-1]
    ) as f:
        data = csv.reader(f, delimiter="\t")
        header = next(data)  # Skip the header
        data = list(data)

    times = [float(row[header.index("Time")]) for row in data]

    speedup_times.append(np.mean(times))

    print("Mean time (ms): ", np.mean(times), "| with workers: ", i)


sP = list(map(lambda x: speedup_times[0] / x, speedup_times))

plt.plot(nb_workers, sP, label="Speedup", marker="o")
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

dir_out = pathlib.Path(__file__).parent.absolute() / "MONTE_CARLO" / "out"

# clear the directory
for f in dir_out.iterdir():
    f.unlink()
