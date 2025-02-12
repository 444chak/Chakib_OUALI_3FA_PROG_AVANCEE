package MONTE_CARLO;

import MONTE_CARLO.Assignment102.PiMonteCarlo;
import MONTE_CARLO.Pi.Master;

public class Main {

    public static void main(String[] args) throws Exception {
        String machineName = System.getenv("COMPUTERNAME");

        int workers;
        int numberOfRuns;
        int totalCount;
        String algo = "";

        if (args.length > 0) {
            workers = Integer.parseInt(args[0]);
            numberOfRuns = Integer.parseInt(args[1]);
            totalCount = Integer.parseInt(args[2]);
            algo = args[3];

        } else {
            workers = 1;
            numberOfRuns = 10;
            totalCount = 120000000;
        }

        // Assignment 102
        if (algo.equals("ass102")) {
            runAssignment102(numberOfRuns, totalCount, machineName, workers);
        }
        if (algo.equals("pi")) {
            runPi(numberOfRuns, totalCount / workers, machineName, workers);
        }

    }

    private static void runPi(int numberOfRuns, int totalCount, String machineName, int workers) throws Exception {
        System.out.println("\n--------Pi--------");
        // define file
        FileWriterUtil fileWriterUtil = new FileWriterUtil("Pi", machineName);

        for (int i = 0; i < numberOfRuns; i++) {
            // Run program
            Result result;
            result = new Master().doRun(totalCount, workers, false);

            fileWriterUtil.writeToFile(result);
        }
        System.out.println(fileWriterUtil.getFilePath());
    }

    private static void runAssignment102(int numberOfRuns, int totalCount, String machineName, int workers) throws Exception {
        System.out.println("--------Assignment 102--------");
        // define file 
        FileWriterUtil fileWriterUtilAssignment102 = new FileWriterUtil("Assignment102", machineName);

        for (int i = 0; i < numberOfRuns; i++) {
            // Run program
            PiMonteCarlo PiVal = new PiMonteCarlo(totalCount, workers);
            long startTime = System.currentTimeMillis();
            PiVal.getPi();
            long stopTime = System.currentTimeMillis();

            // write to file
            Result resultAssignment = PiVal.getResult();
            resultAssignment.setTime(stopTime - startTime);
            fileWriterUtilAssignment102.writeToFile(resultAssignment);
        }
        System.out.println(fileWriterUtilAssignment102.getFilePath());
    }

}
