package MONTE_CARLO;

import MONTE_CARLO.Assignment102.PiMonteCarlo;
import MONTE_CARLO.Pi.Master;
import MONTE_CARLO.Sockets.MasterSocket;
import MONTE_CARLO.Sockets.WorkerSocket;

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
            workers = 5;
            numberOfRuns = 10;
            totalCount = 10000000;
            algo = "pi";
        }

        // Assignment 102
        if (algo.equals("ass102")) {
            runAssignment102(numberOfRuns, totalCount, machineName, workers);
        }
        if (algo.equals("pi")) {
            runPi(numberOfRuns, totalCount, machineName, workers);
        }
        if (algo.equals("socket")) {
            runMasterWorkerSocket(workers, totalCount, numberOfRuns);
        }

    }

    private static void runPi(int numberOfRuns, int totalCount, String machineName, int workers) throws Exception {
        System.out.println("\n--------Pi--------");
        // define file
        FileWriterUtil fileWriterUtil = new FileWriterUtil("Pi", machineName);

        for (int j = 1; j <= workers; j++) {
            fileWriterUtil.writeToFile(j + "-------------------");
            for (int i = 0; i < numberOfRuns; i++) {
                // Run program
                Result result;
                result = new Master().doRun(totalCount, j, false);
                fileWriterUtil.writeToFile(result);
            }
        }

        System.out.println(fileWriterUtil.getFilePath());
    }

    private static void runAssignment102(int numberOfRuns, int totalCount, String machineName, int workers) throws Exception {
        System.out.println("--------Assignment 102--------");
        // define file 
        FileWriterUtil fileWriterUtilAssignment102 = new FileWriterUtil("Assignment102", machineName);

        for (int j = 1; j <= workers; j++) {
            fileWriterUtilAssignment102.writeToFile(j + "-------------------");
            for (int i = 0; i < numberOfRuns; i++) {
                // Run program
                PiMonteCarlo PiVal = new PiMonteCarlo(totalCount, j);
                long startTime = System.currentTimeMillis();
                PiVal.getPi();
                long stopTime = System.currentTimeMillis();

                // write to file
                Result resultAssignment = PiVal.getResult();
                resultAssignment.setTime(stopTime - startTime);
                fileWriterUtilAssignment102.writeToFile(resultAssignment);
            }
        }

        System.out.println(fileWriterUtilAssignment102.getFilePath());
    }

    private static void runMasterWorkerSocket(int currentWorkers, int totalCount, int numberOfRuns) throws Exception {
        System.out.println("--------Master-Worker Socket--------");

        // Start WorkerSockets
        System.out.println("\nTesting with " + currentWorkers + " worker(s)");
        int[] tab_port = new int[currentWorkers];
        // Start WorkerSockets
        for (int i = 0; i < currentWorkers; i++) {
            int port = 25545 + i;
            System.out.println("Starting WorkerSocket on port " + port);
            Thread.sleep(100);
            new Thread(() -> {
                try {
                    WorkerSocket.main(new String[]{String.valueOf(port)});
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
            tab_port[i] = port;

        }

        // Give some time for workers to start
        Thread.sleep(100);

        // Start MasterSocket with current number of workers
        String[] masterParams = new String[3 + currentWorkers]; // Adjust size
        masterParams[0] = String.valueOf(currentWorkers);
        masterParams[1] = String.valueOf(totalCount);
        masterParams[2] = String.valueOf(numberOfRuns);

        for (int i = 0; i < currentWorkers; i++) {
            masterParams[i + 3] = String.valueOf(25545 + i); // Pass correct ports
        }
        MasterSocket.main(masterParams);

    }

}
