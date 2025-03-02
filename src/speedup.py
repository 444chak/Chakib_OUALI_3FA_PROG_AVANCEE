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


############################ 10^8 points ############################


def scalaForte10e8():
    # pi = call_main(16, 10, 100000000, "pi")
    # ass102 = call_main(8, 10, 100000000, "ass102")
    # piSocket = call_main_sockets(16, 10, 100000000)

    pi = dir_out / "F_16W_10E8_Pi_CHAK-DESKTOP.txt"
    # ass102 = dir_out / "F_8W_10E8_Assignment102_CHAK-DESKTOP.txt"
    piSocket = dir_out / "F_16W_10E8_PiSocket_CHAK-DESKTOP.txt"

    speedupCurvePi = speedup_curve(
        speedup(pi), "16 workers, 10^8 points, Pi, CHAK-DESKTOP", "-."
    )
    # speedupCurveAss102 = speedup_curve(
    #     speedup(ass102), "8 workers, 10^8 points, Assignment102, CHAK-DESKTOP"
    # )
    speedupCurvePiSocket = speedup_curve(
        speedup(piSocket), "16 workers, 10^8 points, PiSocket, CHAK-DESKTOP", "-."
    )

    for curve in [speedupCurvePi, speedupCurvePiSocket]:
        plot_curve(curve)


############################ 10^7 points ############################
def scalaForte10e7():
    # pi = call_main(16, 10, 100000000, "pi")
    # ass102 = call_main(16, 10, 100000000, "ass102")
    # piSocket = call_main_sockets(16, 10, 100000000)

    pi = dir_out / "F_16W_10E7_Pi_CHAK-DESKTOP.txt"
    ass102 = dir_out / "F_8W_10E7_Assignment102_CHAK-DESKTOP.txt"
    piSocket = dir_out / "F_16W_10E7_PiSocket_CHAK-DESKTOP.txt"

    speedupCurvePi = speedup_curve(
        speedup(pi), "16 workers, 10^7 points, Pi, CHAK-DESKTOP"
    )
    speedupCurveAss102 = speedup_curve(
        speedup(ass102), "8 workers, 10^7 points, Assignment102, CHAK-DESKTOP"
    )
    speedupCurvePiSocket = speedup_curve(
        speedup(piSocket), "16 workers, 10^7 points, PiSocket, CHAK-DESKTOP"
    )

    for curve in [speedupCurvePi, speedupCurveAss102, speedupCurvePiSocket]:
        plot_curve(curve)


############################ 10^6 points ############################


def scalaForte10e6():
    # pi = call_main(16, 10, 1000000, "pi")
    # ass102 = call_main(10, 10, 1000000, "ass102")
    # piSocket = call_main_sockets(16, 10, 1000000)

    pi = dir_out / "F_16W_10E6_Pi_CHAK-DESKTOP.txt"
    ass102 = dir_out / "F_10W_10E6_Assignment102_CHAK-DESKTOP.txt"
    piSocket = dir_out / "F_16W_10E6_PiSocket_CHAK-DESKTOP.txt"

    speedupCurvePi = speedup_curve(speedup(pi), "16 workers, 10^6 points, Pi", "--")
    speedupCurveAss102 = speedup_curve(
        speedup(ass102), "10 workers, 10^6 points, Assignment102", "--"
    )
    speedupCurvePiSocket = speedup_curve(
        speedup(piSocket), "16 workers, 10^6 points, PiSocket", "--"
    )

    for curve in [speedupCurvePi, speedupCurveAss102, speedupCurvePiSocket]:
        plot_curve(curve)


############################ Scalabilité faible 10^7 points ############################


def scalaFaible10e7():
    # pi = call_main(16, 10, 10000000, "pi", "True")
    # piSocket = call_main_sockets(16, 10, 10000000, "True")

    pi = dir_out / "W_16W_10E7_Pi_CHAK-DESKTOP.txt"
    piSocket = dir_out / "W_16W_10E7_PiSocket_CHAK-DESKTOP.txt"

    speedupCurvePi = speedup_curve(
        speedup(pi), "16 workers, 10^7 points, Pi, CHAK-DESKTOP", "--"
    )
    speedupCurvePiSocket = speedup_curve(
        speedup(piSocket), "16 workers, 10^7 points, PiSocket, CHAK-DESKTOP", "--"
    )

    for curve in [speedupCurvePi, speedupCurvePiSocket]:
        plot_curve(curve)


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


def piCurves(subplot):
    # pi10e6 = call_main(20, 10, 1000000, "pi")
    # pi10e7 = call_main(20, 10, 10000000, "pi")
    # pi10e8 = call_main(20, 10, 100000000, "pi")
    # pi10e9 = call_main(20, 10, 1000000000, "pi")

    a10e6 = False
    a10e7 = True
    a10e8 = False
    a10e9 = True

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


def socketsCurves(subplot):
    # piSocket10e6 = call_main_sockets(20, 10, 1000000)
    # piSocket10e7 = call_main_sockets(20, 10, 10000000)
    # piSocket10e8 = call_main_sockets(20, 10, 100000000)
    # piSocket10e8 = call_main_sockets(20, 10, 1000000000)

    a10e6 = False
    a10e7 = True
    a10e8 = False
    a10e9 = True

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


# scalaFaible10e7()
# plot_weak_scaling(16, "Speedup Curve")

# scalaForte10e6()
# plot_speedups(16, "Speedup Curve")

# scalaForte10e7()
# plot_speedups(16, "Speedup Curve")

# scalaForte10e8()

fig, (left, right) = plt.subplots(1, 2, figsize=(15, 7))
plot_speedups(20, "Speedup Curve - Sockets - CHAK_LAPTOP, 16 THREADS", left)
plot_speedups(20, "Speedup Curve - Pi - CHAK_LAPTOP, 16 THREADS", right)

socketsCurves(left)
piCurves(right)
left.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")
right.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), fontsize="small")

plt.tight_layout()
plt.show()

# Add legends to the subplots with better positioning
