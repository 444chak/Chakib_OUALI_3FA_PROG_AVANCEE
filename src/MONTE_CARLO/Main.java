package MONTE_CARLO;

import MONTE_CARLO.Assignment102.PiMonteCarlo;
import MONTE_CARLO.Pi.Master;

public class Main {

    public static void main(String[] args) throws Exception {
        String machineName = System.getenv("COMPUTERNAME");

        int numberOfRuns = 10;
        int totalCount = 12000;
        int workers = 1;

        // Assignment 102
        System.out.println("--------Assignment 102--------");
        // define file 
        FileWriterUtil fileWriterUtilAssignment102 = new FileWriterUtil("Assignment102", machineName);

        for (int i = 0; i < numberOfRuns; i++) {
            System.out.println("Run " + i);
            // Run program
            PiMonteCarlo PiVal = new PiMonteCarlo(totalCount);
            long startTime = System.currentTimeMillis();
            PiVal.getPi();
            long stopTime = System.currentTimeMillis();

            // write to file
            Result resultAssignment = PiVal.getResult();
            resultAssignment.setTime(stopTime - startTime);
            fileWriterUtilAssignment102.writeToFile(resultAssignment);
        }
        // Pi
        System.out.println("\n--------Pi--------");
        // define file
        FileWriterUtil fileWriterUtil = new FileWriterUtil("Pi", machineName);

        for (int i = 0; i < numberOfRuns; i++) {
            System.out.println("Run " + i);
            // Run program
            Result result;
            result = new Master().doRun(totalCount, workers, false);

            fileWriterUtil.writeToFile(result);
        }
        // Run program

    }
}
