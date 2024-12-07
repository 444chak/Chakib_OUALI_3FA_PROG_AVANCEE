package MONTE_CARLO;
/**
 * Approximates PI using the Monte Carlo method. Demonstrates use of Callables,
 * Futures, and thread pools.
 */
public class Pi {
    public static void main(String[] args) throws Exception {
        long total;
        // 10 workers, 50000 iterations each
        total = new Master().doRun(5000000, 10);
        System.out.println("total from Master = " + total);
    }
}

