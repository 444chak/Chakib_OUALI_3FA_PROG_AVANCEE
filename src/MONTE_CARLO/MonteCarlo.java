package MONTE_CARLO;

import java.util.concurrent.atomic.AtomicInteger;

class MonteCarlo implements Runnable {

    public AtomicInteger nAtomSuccess;

    @Override
    public void run() {
        double x = Math.random();
        double y = Math.random();
        if (x * x + y * y <= 1) {
            nAtomSuccess.incrementAndGet();
        }
    }
}
