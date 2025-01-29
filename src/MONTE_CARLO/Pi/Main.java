package MONTE_CARLO.Pi;

import MONTE_CARLO.Result;

/**
 * Approximates PI using the Monte Carlo method. Demonstrates use of Callables,
 * Futures, and thread pools.
 */
public class Main {

    public static void main(String[] args) throws Exception {
        Result result;
        // 10 workers, 50000 iterations each
        result = new Master().doRun(5000000, 10, true);
        System.out.println("total from Master = " + result.getTotal());
    }
}
