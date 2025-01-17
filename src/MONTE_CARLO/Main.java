package MONTE_CARLO;

import MONTE_CARLO.Assignment102.PiMonteCarlo;
import MONTE_CARLO.Pi.Master;

public class Main {

    public static void main(String[] args) throws Exception {
        // Assignment 102
        System.out.println("--------Assignment 102--------");
        PiMonteCarlo PiVal = new PiMonteCarlo(10000000);
        long startTime = System.currentTimeMillis();
        double value = PiVal.getPi();
        long stopTime = System.currentTimeMillis();
        System.out.println("Approx value:" + value);
        System.out.println("Difference to exact value of pi: " + (value - Math.PI));
        System.out.println("Error: " + (value - Math.PI) / Math.PI * 100 + " %");
        System.out.println("Available processors: " + Runtime.getRuntime().availableProcessors());
        System.out.println("Time Duration: " + (stopTime - startTime) + "ms");

        // Pi
        System.out.println("\n--------Pi--------");
        long total;
        total = new Master().doRun(5000000, 10);
        System.out.println("total from Master = " + total);
    }
}
