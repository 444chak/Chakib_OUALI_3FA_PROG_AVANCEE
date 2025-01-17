package MONTE_CARLO.Assignment102;
// Estimate the value of Pi using Monte-Carlo Method, using parallel program

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicInteger;



public class PiMonteCarlo {

    AtomicInteger nAtomSuccess;
    int nThrows;
    double value;

    public PiMonteCarlo(int i) {
        this.nAtomSuccess = new AtomicInteger(0);
        this.nThrows = i;
        this.value = 0;
    }

    public double getPi() {
        int nProcessors = Runtime.getRuntime().availableProcessors();
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
        return value;
    }
}
