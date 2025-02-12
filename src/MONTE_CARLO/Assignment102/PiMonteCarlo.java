package MONTE_CARLO.Assignment102;
// Estimate the value of Pi using Monte-Carlo Method, using parallel program

import MONTE_CARLO.Result;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;

public class PiMonteCarlo {

    AtomicInteger nAtomSuccess;
    int nThrows;
    double value;
    int nProcessors;

    public PiMonteCarlo(int i, int workers) {
        this.nAtomSuccess = new AtomicInteger(0);
        this.nThrows = i;
        this.value = 0;
        this.nProcessors = workers;
    }

    public double getPi() {
        ExecutorService executor = Executors.newWorkStealingPool(nProcessors);
        for (int i = 1; i <= nThrows; i++) {
            MonteCarlo worker = new MonteCarlo();
            worker.nAtomSuccess = nAtomSuccess;
            executor.execute(worker);
        }
        executor.shutdown();
        while (!executor.isTerminated()) {
        }
        value = 4.0 * nAtomSuccess.get() / nThrows;
        System.out.println("Approx value:" + value);
        System.out.println("Nombre de workers: " + nProcessors);
        System.out.println("nThrows" + nThrows);
        
        return value;
    }

    public Result getResult() {
        double error = (Math.abs((value - Math.PI)) / Math.PI);
        int ntot = nThrows;
        int nbProcess = Runtime.getRuntime().availableProcessors();
        long time = 0;
        Result result = new Result(nAtomSuccess.get(), error, value, ntot, nbProcess, time);
        return result;
    }
}
