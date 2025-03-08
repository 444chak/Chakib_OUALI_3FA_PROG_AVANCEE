import pathlib
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import csv

path = pathlib.Path(__file__).parent.absolute()
path = path / "MONTE_CARLO"

dir_out = pathlib.Path(__file__).parent.absolute() / "MONTE_CARLO" / "out"


def run_java(file, args):
    result = subprocess.run(
        [
            "java",
            file,
            *args,
        ],
        stdout=subprocess.PIPE,
    )
    return result.stdout.decode("utf-8")


def clean_out_dir():
    for f in dir_out.glob("*"):
        f.unlink()


def call_main(workers, number_of_experiments, total_count, algo, *args):
    file = path / "Main.java"
    out = run_java(
        file, [str(workers), str(number_of_experiments), str(total_count), algo, *args]
    )
    return out.strip().split("\n")[-1]


def call_main_sockets(workers, number_of_experiments, total_count, *args):
    file = path / "Main.java"
    outs = []
    for i in range(1, workers + 1):
        out = run_java(
            file,
            [str(i), str(number_of_experiments), str(total_count), "socket", *args],
        )
        outs.append([int(i), out.strip().split("\n")[-1]])
    return merge_outs_in_1_file(outs)


def merge_outs_in_1_file(outs):
    with open(dir_out / "merged_out.txt", "w") as f:
        for i, out in outs:
            with open(out) as f2:
                if i == 1:
                    # write header
                    f.write(f2.readline())
                    f2.readline()
                    f.write(f"{i}-------------------\n")
                    f.write(f2.read())
                else:  # dont write header
                    f2.readline()
                    f.write(f"{i}-------------------\n")
                    f.write(f2.read())
    # remove outs file and rename merged_out.txt outs[-1]
    for i, out in outs:
        pathlib.Path(out).unlink()
    (dir_out / "merged_out.txt").rename(outs[-1][1])
    return outs[-1][1]


# print(call_main(5, 10, 1, "pi"))
# print(call_main_sockets(5, 10, 1))


def speedup(out):
    """
    each block of n workers is separated by "n-------------------"
    File is structured as follows:
    NbProcess	Error	Estimation	Ntot	Time	Total
    1-------------------
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    2-------------------
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    xxx		xxx		xxx		xxx		xxx		xxx
    ...

    Return list of speedup for each process (sp = T1/Tp) [[nbP, sP], [nbP+1, sP+1], ...]

    """
    # search index of "Time" column in header
    time_index = -1
    with open(out) as f:
        data = csv.reader(f, delimiter="\t")
        header = next(data)
        time_index = header.index("Time")

    actual = 0
    actualTimes = []
    times = []  # [[nbP, meanTime], ...]
    with open(out) as f:
        next(f)  # Skip header line
        for line in f:
            if "-------------------" in line:
                if actual != 0:
                    times.append([actual, np.mean(actualTimes)])

                actual = int(line.split("-")[0])
                actualTimes = []
            else:
                actualTimes.append(float(line.split("\t")[time_index]))

        times.append([actual, np.mean(actualTimes)])

    speedups = [[times[0][0], 1.0]]  # Add the first speedup (1 worker, speedup = 1)
    for i in range(1, len(times)):
        speedups.append([times[i][0], times[0][1] / times[i][1]])

    return speedups


def perfect_speedup(n):
    return [[i, i] for i in range(1, n + 1)]


def speedup_curve(speedups, label, linestyle="-", marker="x"):
    return (
        ([x[0] for x in speedups], [x[1] for x in speedups]),
        linestyle,
        label,
        marker,
    )


def plot_curve(speedup_curve, subplot):
    subplot.plot(
        *speedup_curve[0],
        speedup_curve[1],
        label=speedup_curve[2],
        marker=speedup_curve[3],
    )


def plot_speedups(max_workers, title, subplot=None):
    # Use provided subplot or create a new figure if none is provided
    if subplot is None:
        subplot = plt.gca()

    # plot perfect speedup
    subplot.plot(
        [x[0] for x in perfect_speedup(max_workers)],
        [x[1] for x in perfect_speedup(max_workers)],
        ":",
        label="Perfect speedup",
        c="black",
    )

    # labels
    subplot.set_xlabel("Number of workers")
    subplot.set_ylabel("Speedup")

    # grid
    subplot.grid()
    subplot.set_aspect("equal")
    subplot.set_xlim(0, max_workers + 0.5)
    subplot.set_ylim(0, max_workers + 0.5)

    # ticks
    subplot.set_yticks(range(1, max_workers + 1))
    subplot.set_xticks(range(1, max_workers + 1))

    # title
    subplot.set_title(title)
    subplot.legend()
    return subplot


def plot_error_graph(data_dict, title, xlabel, ylabel, output_file=None):
    """
    Plots error vs number of points for multiple datasets on the same graph.

    :param data_dict: Dictionary mapping dataset names to lists of tuples (Npoints, Error).
    :param title: Title of the graph.
    :param xlabel: X-axis label.
    :param ylabel: Y-axis label.
    :param output_file: Path to save the graph (optional).
    """
    plt.figure(figsize=(12, 8))

    # Different colors for different datasets
    colors = ["blue", "red", "green", "purple", "orange"]
    colors_dark = ["navy", "darkred", "darkgreen", "indigo", "darkorange"]

    for i, (label, data) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        color_dark = colors_dark[i % len(colors_dark)]

        # Convert data to numpy arrays
        n_points = np.array([d[0] for d in data])
        errors = np.array([d[1] for d in data])

        # Calculate medians for each unique value of Npoints
        unique_n_points = np.unique(n_points)
        medians = [np.median(errors[n_points == n]) for n in unique_n_points]

        # Plot individual points (with low alpha for clarity)
        plt.scatter(
            n_points, errors, color=color, alpha=0.2, s=20, label=f"{label} - points"
        )

        # Plot medians with connecting lines
        plt.plot(
            unique_n_points,
            medians,
            color=color_dark,
            linestyle="-",
            marker="o",
            markersize=8,
            label=f"{label} - median",
        )

    # Format the graph
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()

    if output_file:
        plt.savefig(output_file)


def extract_error(file_path):
    """
    Extracts Ntot (number of points) and Error columns from a file.

    :param file_path: Path to the output file.
    :return: List of tuples (Npoints, Error).
    """
    data = []
    first_n_points = None
    with open(file_path, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)

        try:
            n_points_index = header.index("Ntot")
            error_index = header.index("Error")
        except ValueError as e:
            raise ValueError(
                "Columns 'Ntot' or 'Error' are missing in the file."
            ) from e

        for row in reader:
            # Check if the row is valid
            if len(row) > max(n_points_index, error_index):
                try:
                    n_points = int(row[n_points_index])

                    error = float(row[error_index])
                    if first_n_points is None:
                        first_n_points = n_points
                    data.append((first_n_points, error))
                except ValueError:
                    pass  # Skip malformed rows
    return data


def plot_weak_scaling(max_workers, title):
    # plot linear 1 line
    plt.plot(
        [x for x in range(1, max_workers + 1)],
        [1 for x in range(1, max_workers + 1)],
        ":",
        label="Perfect speedup",
    )

    # labels
    plt.xlabel("Number of workers")
    plt.ylabel("Speedup")

    # grid
    plt.grid()
    plt.xlim(0, max_workers + 0.5)
    plt.ylim(0, 1.5)

    # window size

    # ticks
    plt.xticks(range(1, max_workers + 1))

    # title
    plt.title(title)
    plt.legend()
    plt.show()


def weakCurvesPi(s10e6=False, s10e7=False):
    # pi = call_main(16, 10, 10000000, "pi", "True")
    # piSocket = call_main_sockets(16, 10, 10000000, "True")

    pi10e6 = dir_out / "CHAK_LAPTOP" / "Pi" / "s_faible" / "16W_10E6_Pi_CHAK-LAPTOP.txt"
    pi10e7 = dir_out / "CHAK_LAPTOP" / "Pi" / "s_faible" / "16W_10E7_Pi_CHAK-LAPTOP.txt"

    speedupCurvePi10e6 = speedup_curve(
        speedup(pi10e6), "16 workers, 10^6 points, Pi, CHAK-LAPTOP", "--"
    )
    speedupCurvePi10e7 = speedup_curve(
        speedup(pi10e7), "16 workers, 10^7 points, CHAK-LAPTOP", "--"
    )

    if s10e6:
        plot_curve(speedupCurvePi10e6, plt)

    if s10e7:
        plot_curve(speedupCurvePi10e7, plt)


def weakCurvesPiSocket(s10e6=False, s10e7=False):
    piSocket10e6 = (
        dir_out
        / "CHAK_LAPTOP"
        / "PiSocket"
        / "s_faible"
        / "16W_10E6_PiSocket_CHAK-LAPTOP.txt"
    )
    piSocket10e7 = (
        dir_out
        / "CHAK_LAPTOP"
        / "PiSocket"
        / "s_faible"
        / "16W_10E7_PiSocket_CHAK-LAPTOP.txt"
    )

    speedupCurvePiSocket10e6 = speedup_curve(
        speedup(piSocket10e6), "16 workers, 10^6 points, PiSocket, CHAK-LAPTOP", "--"
    )
    speedupCurvePiSocket10e7 = speedup_curve(
        speedup(piSocket10e7), "16 workers, 10^7 points, PiSocket, CHAK-LAPTOP", "--"
    )

    if s10e6:
        plot_curve(speedupCurvePiSocket10e6, plt)

    if s10e7:
        plot_curve(speedupCurvePiSocket10e7, plt)


CHAK_LAPTOP_PI_S_FORTE = dir_out / "CHAK_LAPTOP" / "Pi" / "s_forte"
CHAK_LAPTOP_PISOCKET_S_FORTE = dir_out / "CHAK_LAPTOP" / "PiSocket" / "s_forte"

pi_s_forte = {
    "10e6": CHAK_LAPTOP_PI_S_FORTE / "20W_10E6_CHAK-LAPTOP.txt",
    "10e7": CHAK_LAPTOP_PI_S_FORTE / "20W_10E7_CHAK-LAPTOP.txt",
    "10e8": CHAK_LAPTOP_PI_S_FORTE / "20W_10E8_CHAK-LAPTOP.txt",
    "10e9": CHAK_LAPTOP_PI_S_FORTE / "20W_10E9_CHAK-LAPTOP.txt",
}

piSocket_s_forte = {
    "10e6": CHAK_LAPTOP_PISOCKET_S_FORTE / "20W_10E6_CHAK-LAPTOP.txt",
    "10e7": CHAK_LAPTOP_PISOCKET_S_FORTE / "20W_10E7_CHAK-LAPTOP.txt",
    "10e8": CHAK_LAPTOP_PISOCKET_S_FORTE / "20W_10E8_CHAK-LAPTOP.txt",
    "10e9": CHAK_LAPTOP_PISOCKET_S_FORTE / "20W_10E9_CHAK-LAPTOP.txt",
}


def piCurves(subplot, a10e6=False, a10e7=True, a10e8=False, a10e9=True):
    # pi10e6 = call_main(20, 10, 1000000, "pi")
    # pi10e7 = call_main(20, 10, 10000000, "pi")
    # pi10e8 = call_main(20, 10, 100000000, "pi")
    # pi10e9 = call_main(20, 10, 1000000000, "pi")

    speedupCurvePi10e6 = speedup_curve(
        speedup(pi_s_forte["10e6"]), "20 workers, 10^6 points, Pi"
    )
    speedupCurvePi10e7 = speedup_curve(
        speedup(pi_s_forte["10e7"]), "20 workers, 10^7 points, Pi"
    )
    speedupCurvePi10e8 = speedup_curve(
        speedup(pi_s_forte["10e8"]), "20 workers, 10^8 points, Pi"
    )
    speedupCurvePi10e9 = speedup_curve(
        speedup(pi_s_forte["10e9"]), "20 workers, 10^9 points, Pi"
    )

    for curve in [
        speedupCurvePi10e6 if a10e6 else None,
        speedupCurvePi10e7 if a10e7 else None,
        speedupCurvePi10e8 if a10e8 else None,
        speedupCurvePi10e9 if a10e9 else None,
    ]:
        if curve is not None:
            plot_curve(curve, subplot)


def socketsCurves(subplot, a10e6=False, a10e7=True, a10e8=False, a10e9=True):
    # piSocket10e6 = call_main_sockets(20, 10, 1000000)
    # piSocket10e7 = call_main_sockets(20, 10, 10000000)
    # piSocket10e8 = call_main_sockets(20, 10, 100000000)
    # piSocket10e8 = call_main_sockets(20, 10, 1000000000)

    speedupCurvePiSocket10e6 = speedup_curve(
        speedup(piSocket_s_forte["10e6"]), "20 workers, 10^6 points, PiSocket"
    )
    speedupCurvePiSocket10e7 = speedup_curve(
        speedup(piSocket_s_forte["10e7"]), "20 workers, 10^7 points, PiSocket"
    )
    speedupCurvePiSocket10e8 = speedup_curve(
        speedup(piSocket_s_forte["10e8"]), "20 workers, 10^8 points, PiSocket"
    )
    speedupCurvePiSocket10e9 = speedup_curve(
        speedup(piSocket_s_forte["10e9"]), "20 workers, 10^9 points, PiSocket"
    )

    for curve in [
        speedupCurvePiSocket10e6 if a10e6 else None,
        speedupCurvePiSocket10e7 if a10e7 else None,
        speedupCurvePiSocket10e8 if a10e8 else None,
        speedupCurvePiSocket10e9 if a10e9 else None,
    ]:
        if curve is not None:
            plot_curve(curve, subplot)


def assignment102Curves(subplot):
    a102_10e6 = (
        dir_out
        / "CHAK_LAPTOP"
        / "Assignment102"
        / "s_forte"
        / "10W_10E6_Assignment102_CHAK-LAPTOP.txt"
    )
    a102_10e7 = (
        dir_out
        / "CHAK_LAPTOP"
        / "Assignment102"
        / "s_forte"
        / "8W_10E7_Assignment102_CHAK-LAPTOP.txt"
    )

    speedupCurveAss102_10e6 = speedup_curve(
        speedup(a102_10e6), "10 workers, 10^6 points, Pi, CHAK-LAPTOP", "--"
    )
    speedupCurveAss102_10e7 = speedup_curve(
        speedup(a102_10e7), "8 workers, 10^7 points, CHAK-LAPTOP", "--"
    )

    plot_curve(speedupCurveAss102_10e6, subplot)
    plot_curve(speedupCurveAss102_10e7, subplot)


################

# fig, (left, right) = plt.subplots(1, 2, figsize=(15, 7))
# plot_speedups(20, "Speedup Curve CHAK_LAPTOP, 16 THREADS", left)
# plot_speedups(20, "Speedup Curve CHAK_LAPTOP, 16 THREADS", right)

# socketsCurves(left, a10e6=False, a10e7=True, a10e8=False, a10e9=False)
# socketsCurves(right, a10e6=False, a10e7=False, a10e8=False, a10e9=True)
# piCurves(left, a10e6=False, a10e7=True, a10e8=False, a10e9=False)
# piCurves(right, a10e6=False, a10e7=False, a10e8=False, a10e9=True)
# left.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")
# right.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")

# plt.tight_layout()
# plt.show()

################ ass 102

# fig, graph = plt.subplots(1, 1, figsize=(15, 7))

# plot_speedups(10, "Speedup Curve - Assignment 102 - CHAK_LAPTOP", graph)
# assignment102Curves(graph)
# graph.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")
# plt.tight_layout()
# plt.show()

############# ass102 error

# error10e6 = extract_error(
#     dir_out
#     / "CHAK_LAPTOP"
#     / "Assignment102"
#     / "s_forte"
#     / "10W_10E6_Assignment102_CHAK-LAPTOP.txt"
# )

# error10e7 = extract_error(
#     dir_out
#     / "CHAK_LAPTOP"
#     / "Assignment102"
#     / "s_forte"
#     / "8W_10E7_Assignment102_CHAK-LAPTOP.txt"
# )

# data_dict = {
#     "10^6 points": error10e6,
#     "10^7 points": error10e7,
# }

# plot_error_graph(
#     data_dict,
#     "Error vs Number of Points - Assignment 102",
#     "Number of Points (Npoints)",
#     "Absolute Error",
# )

# plt.tight_layout()
# plt.show()


###############

# fig, graph = plt.subplots(1, 1, figsize=(15, 7))
# plot_speedups(20, "Speedup Curve - Pi - CHAK_LAPTOP, 16 THREADS", graph)
# piCurves(graph)
# graph.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")
# plt.tight_layout()
# plt.show()

###############

# fig, graph = plt.subplots(1, 1, figsize=(15, 7))
# plot_speedups(20, "Speedup Curve - PiSocket - CHAK_LAPTOP, 16 THREADS", graph)
# socketsCurves(graph)
# graph.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")
# plt.tight_layout()
# plt.show()

###############


###############

# Extract error data from files
# error10e6 = extract_error(pi_s_forte["10e6"])
# error10e7 = extract_error(pi_s_forte["10e7"])
# error10e8 = extract_error(pi_s_forte["10e8"])
# error10e9 = extract_error(pi_s_forte["10e9"])

# error10e6 = extract_error(piSocket_s_forte["10e6"])
# error10e7 = extract_error(piSocket_s_forte["10e7"])
# error10e8 = extract_error(piSocket_s_forte["10e8"])
# error10e9 = extract_error(piSocket_s_forte["10e9"])

# # Create a dictionary of data for the combined plot
# data_dict = {
#     "10^6 points": error10e6,
#     "10^7 points": error10e7,
#     "10^8 points": error10e8,
#     "10^9 points": error10e9,
# }

# # Plot all data on the same graph
# plot_error_graph(
#     data_dict,
#     "Error vs Number of Points - Monte Carlo PiSocket Estimation",
#     "Number of Points (Npoints)",
#     "Absolute Error",
# )

# plt.tight_layout()
# plt.show()

###############


# weakCurvesPi(s10e6=True, s10e7=True)
# plot_weak_scaling(16, "Weak Scaling Curve - Pi")
# plt.show()

# weakCurvesPiSocket(s10e6=True, s10e7=True)
# plot_weak_scaling(16, "Weak Scaling Curve - PiSocket")
# plt.show()

###############

# error_weak_pi_10e6 = extract_error(
#     dir_out / "CHAK_LAPTOP" / "Pi" / "s_faible" / "16W_10E6_Pi_CHAK-LAPTOP.txt"
# )

# error_weak_pi_10e7 = extract_error(
#     dir_out / "CHAK_LAPTOP" / "Pi" / "s_faible" / "16W_10E7_Pi_CHAK-LAPTOP.txt"
# )

# data_dict = {
#     "10^6 points": error_weak_pi_10e6,
#     "10^7 points": error_weak_pi_10e7,
# }

# plot_error_graph(
#     data_dict,
#     "Error vs Number of Points - Monte Carlo Pi Estimation",
#     "Number of Points (Npoints)",
#     "Absolute Error",
# )

# plt.tight_layout()
# plt.show()

###############

# error_weak_pisocket_10e6 = extract_error(
#     dir_out
#     / "CHAK_LAPTOP"
#     / "PiSocket"
#     / "s_faible"
#     / "16W_10E6_PiSocket_CHAK-LAPTOP.txt"
# )

# error_weak_pisocket_10e7 = extract_error(
#     dir_out
#     / "CHAK_LAPTOP"
#     / "PiSocket"
#     / "s_faible"
#     / "16W_10E7_PiSocket_CHAK-LAPTOP.txt"
# )

# data_dict = {
#     "10^6 points": error_weak_pisocket_10e6,
#     "10^7 points": error_weak_pisocket_10e7,
# }

# plot_error_graph(
#     data_dict,
#     "Error vs Number of Points - Monte Carlo PiSocket Estimation",
#     "Number of Points (Npoints)",
#     "Absolute Error",
# )

# plt.tight_layout()
# plt.show()

################### Erreur expérience distribuée ################
# data = [
#     (2 * 10**9, 2.3575172837409821 * 10**-5),
#     (4 * 10**9, 1.0177846524687415 * 10**-5),
#     (8 * 10**9, 1.0747921043959614 * 10**-5),
#     (1.6 * 10**10, 4.6105085509244952 * 10**-6),
#     (3.2 * 10**10, 2.8263219557848443 * 10**-6),
#     (6.4 * 10**10, 1.2763940615949628 * 10**-6),
#     (1.28 * 10**11, 1.3741649324992772 * 10**-6),
# ]

# plt.figure(figsize=(10, 8))

# points = [d[0] for d in data]
# erreurs = [d[1] for d in data]

# plt.loglog(points, erreurs, "bo-", markersize=8, linewidth=2)

# for i, (x, y) in enumerate(zip(points, erreurs)):
#     plt.annotate(
#         f"{x:.1e}",
#         xy=(x, y),
#         xytext=(5, 5),
#         textcoords="offset points",
#         ha="left",
#         va="bottom",
#         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.7),
#     )

# log_points = np.log10(points)
# log_erreurs = np.log10(erreurs)
# pente, ordonnee = np.polyfit(log_points, log_erreurs, 1)

# x_range = np.logspace(np.log10(min(points)), np.log10(max(points)), 100)
# plt.loglog(
#     x_range,
#     10 ** (ordonnee) * x_range**pente,
#     "r--",
#     label=f"Pente: {pente:.3f} (1/√N: {-0.5:.3f})",
# )

# plt.xlabel("Nombre de Points (N)")
# plt.ylabel("Error")
# plt.title("Error vs Nombre de Points - Monte Carlo Distribué")
# plt.grid(True, which="both", ls="--", alpha=0.7)
# plt.legend()

# plt.loglog(x_range, 0.01 * x_range ** (-0.5), "g:", label="Théorique: 1/√N")
# plt.legend()

# plt.tight_layout()
# plt.show()


########### Speedup expériences distribuées ###########

# data_time = [
#     (1, 68974),
#     (2, 69189),
#     (4, 70436),
#     (8, 70450),
#     (16, 70484),
#     (32, 71908),
#     (64, 70890),
# ]


# def speedup_manual(data_time):
#     speedups = []
#     for i in range(len(data_time)):
#         speedups.append([data_time[i][0], data_time[0][1] / data_time[i][1]])
#     return speedups


# speedups = speedup_manual(data_time)

# speedupCurve = speedup_curve(speedups, "Distributed Monte Carlo (Weak Scaling)")

# plt.figure(figsize=(10, 8))
# plt.plot(
#     [1, 64], [1, 1], ":", label="Perfect Weak Scaling", c="black"
# )  # Horizontal line at y=1

# plot_curve(speedupCurve, plt)

# plt.xlabel("Number of Workers")
# plt.ylabel("Efficiency (T₁/Tₚ)")
# plt.grid(True)
# plt.title("Weak Scaling - Distributed Monte Carlo")
# plt.xlim(0, 64 + 0.5)
# plt.ylim(0, 1.5)
# plt.xticks(range(0, 65, 4))
# plt.legend()
# plt.show()
