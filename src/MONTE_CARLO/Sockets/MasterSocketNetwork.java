package MONTE_CARLO.Sockets;

import MONTE_CARLO.FileWriterUtil;
import MONTE_CARLO.Result;
import java.io.*;
import java.net.*;

/**
 * Master is a client. It makes requests to numWorkers.
 *
 */
public class MasterSocketNetwork {

    static int maxServer = 30;

    static String[] tab_total_workers = new String[maxServer];
    static BufferedReader[] reader = new BufferedReader[maxServer];
    static PrintWriter[] writer = new PrintWriter[maxServer];
    static Socket[] sockets = new Socket[maxServer];

    public static void main(String[] args) throws Exception {

        // ARGS :
        // 1. Number of workers
        // 2. Total count
        // 3. Number of runs
        // 4. Worker IP 1
        // 5. Worker port 1
        // 6. Worker IP 2
        // 7. Worker port 2
        // ...
        // 2 + 2 * numWorkers. Scala faible (true/false)
        // 2 + 2 * numWorkers + 1. Number of threads per worker

        // MC parameters
        int totalCount = 16000000; // total number of throws on a Worker
        int total = 0; // total number of throws inside quarter of disk
        double pi;

        int numWorkers = maxServer;
        int numberOfRuns = 10;

        int numberOfThreads = 1;

        System.out.println("#########################################");
        System.out.println("# Computation of PI by MC method        #");
        System.out.println("#########################################");

        boolean scalaFaible = false;

        if (args.length > 0) {
            numWorkers = Integer.parseInt(args[0]);
            if (numWorkers > maxServer) {
                throw new IllegalArgumentException("Number of workers must be less than " + maxServer);
            }
            totalCount = Integer.parseInt(args[1]) / numWorkers;
            numberOfRuns = Integer.parseInt(args[2]);

            if (args.length < 3 + numWorkers * 2) {
                throw new IllegalArgumentException("Insufficient worker IP and port arguments");
            }

            String[] workerIPs = new String[numWorkers];
            int[] workerPorts = new int[numWorkers];
            for (int i = 0; i < numWorkers; i++) {
                workerIPs[i] = args[3 + i * 2];
                workerPorts[i] = Integer.parseInt(args[4 + i * 2]);
            }

            if (args.length > 3 + numWorkers * 2) {
                scalaFaible = Boolean.parseBoolean(args[3 + numWorkers * 2]);
                if (scalaFaible) {
                    totalCount = Integer.parseInt(args[1]);
                }
            }

            if (args.length > 4 + numWorkers * 2) {
                numberOfThreads = Integer.parseInt(args[4 + numWorkers * 2]);
            }

            // create worker's socket
            for (int i = 0; i < numWorkers; i++) {
                sockets[i] = new Socket(workerIPs[i], workerPorts[i]);
                System.out.println("SOCKET = " + sockets[i]);

                reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
                writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())),
                        true);
            }

            String message_to_send;
            message_to_send = String.valueOf(totalCount);
            String message_to_send2 = String.valueOf(numberOfThreads);

            long stopTime, startTime;
            FileWriterUtil fileWriterUtil = new FileWriterUtil("PiSocket", System.getenv("COMPUTERNAME"));

            for (int j = 0; j < numberOfRuns; j++) {
                total = 0;

                startTime = System.currentTimeMillis();
                // initialize workers
                for (int i = 0; i < numWorkers; i++) {
                    writer[i].println(message_to_send); // send a message to each worker
                    writer[i].println(message_to_send2); // send a message to each worker
                }

                // listen to workers's message
                for (int i = 0; i < numWorkers; i++) {
                    tab_total_workers[i] = reader[i].readLine(); // read message from server
                    System.out.println("Client sent: " + tab_total_workers[i]);
                }

                // compute PI with the result of each workers
                for (int i = 0; i < numWorkers; i++) {
                    total += Integer.parseInt(tab_total_workers[i]);
                }

                pi = 4.0 * total / totalCount / numWorkers;
                stopTime = System.currentTimeMillis();

                Result result = new Result(total, (Math.abs((pi - Math.PI)) / Math.PI), pi, totalCount * numWorkers,
                        numWorkers, (stopTime - startTime));

                fileWriterUtil.writeToFile(result);
            }
            for (int i = 0; i < numWorkers; i++) {
                writer[i].println("END"); // send a message to stop each worker
            }
            System.out.println(fileWriterUtil.getFilePath());
        } else {
            throw new IllegalArgumentException("Number of workers, total count, and worker IPs and ports are required");
        }
    }
}
