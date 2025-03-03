package MONTE_CARLO.Pi;

import java.util.Random;
import java.util.concurrent.Callable;

/**
 * Task for running the Monte Carlo simulation.
 */
class Worker implements Callable<Long> {

    private final int numIterations;

    public Worker(int num) {
        this.numIterations = num;
    }

    @Override
    public Long call() {
        long circleCount = 0;
        Random prng = new Random();
        for (int j = 0; j < numIterations; j++) {
            double x = prng.nextDouble();
            double y = prng.nextDouble();
            if ((x * x + y * y) < 1) {
                ++circleCount;
            }
        }
        return circleCount;
    }
}
