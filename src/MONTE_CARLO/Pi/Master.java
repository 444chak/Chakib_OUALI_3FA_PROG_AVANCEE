package MONTE_CARLO.Pi;

import MONTE_CARLO.Result;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/**
 * Creates workers to run the Monte Carlo simulation and aggregates the results.
 */
public class Master {

    /**
     * Run the Monte Carlo simulation.
     *
     * @param totalCount The number of points to generate.
     * @param numWorkers The number of workers to use.
     * @param print Whether to print the results.
     * @return The results of the simulation.
     * @throws InterruptedException
     * @throws ExecutionException
     */
    public Result doRun(int totalCount, int numWorkers, Boolean print) throws InterruptedException, ExecutionException {

        long startTime = System.currentTimeMillis();

        // Create a collection of tasks
        List<Callable<Long>> tasks = new ArrayList<>();
        for (int i = 0; i < numWorkers; ++i) {
            tasks.add(new Worker(totalCount));
        }

        // Run them and receive a collection of Futures
        ExecutorService exec = Executors.newFixedThreadPool(numWorkers);
        List<Future<Long>> results = exec.invokeAll(tasks);
        long total = 0;

        // Assemble the results.
        for (Future<Long> f : results) {
            // Call to get() is an implicit barrier.  This will block
            // until result from corresponding worker is ready.
            total += f.get();
        }
        double pi = 4.0 * total / totalCount / numWorkers;

        long stopTime = System.currentTimeMillis();

        if (print) {
            System.out.println("\nPi : " + pi);
            System.out.println("Error: " + (Math.abs((pi - Math.PI)) / Math.PI) + "\n");

            System.out.println("Ntot: " + totalCount * numWorkers);
            System.out.println("Available processors: " + numWorkers);
            System.out.println("Time Duration (ms): " + (stopTime - startTime) + "\n");

            System.out.println((Math.abs((pi - Math.PI)) / Math.PI) + " " + totalCount * numWorkers + " " + numWorkers + " " + (stopTime - startTime));
        }

        exec.shutdown();
        double error = (Math.abs((pi - Math.PI)) / Math.PI);
        double estimation = pi;
        int ntot = totalCount * numWorkers;
        int nbProcess = numWorkers;
        long time = stopTime - startTime;
        Result result = new Result(total, error, estimation, ntot, nbProcess, time);
        return result;
    }
}
