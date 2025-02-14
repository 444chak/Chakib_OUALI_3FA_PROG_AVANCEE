package MONTE_CARLO.Sockets;

import MONTE_CARLO.FileWriterUtil;
import MONTE_CARLO.Result;
import java.io.*;
import java.net.*;

/**
 * Master is a client. It makes requests to numWorkers.
 *
 */
public class MasterSocket {

    static int maxServer = 30;

    static String[] tab_total_workers = new String[maxServer];
    static final String ip = "127.0.0.1";
    static BufferedReader[] reader = new BufferedReader[maxServer];
    static PrintWriter[] writer = new PrintWriter[maxServer];
    static Socket[] sockets = new Socket[maxServer];

    public static void main(String[] args) throws Exception {

        // MC parameters
        int totalCount = 16000000; // total number of throws on a Worker
        int total = 0; // total number of throws inside quarter of disk
        double pi;

        int numWorkers = maxServer;
        int numberOfRuns = 10;

        System.out.println("#########################################");
        System.out.println("# Computation of PI by MC method        #");
        System.out.println("#########################################");
        int[] workers_ports;

        boolean scalaFaible = false;

        if (args.length > 0) {
            numWorkers = Integer.parseInt(args[0]);
            if (numWorkers > maxServer) {
                throw new IllegalArgumentException("Number of workers must be less than " + maxServer);
            }
            totalCount = Integer.parseInt(args[1]) / numWorkers;
            numberOfRuns = Integer.parseInt(args[2]);
            workers_ports = new int[numWorkers];
            for (int i = 0; i < numWorkers; i++) {
                workers_ports[i] = Integer.parseInt(args[i + 3]);
            }
            if (args.length > 3 + numWorkers) {
                scalaFaible = Boolean.parseBoolean(args[3 + numWorkers]);
                if (scalaFaible) {
                    totalCount = Integer.parseInt(args[1]);
                }
            }

        } else {
            throw new IllegalArgumentException("Number of workers is required and total count is required");
        }

        //create worker's socket
        for (int i = 0; i < numWorkers; i++) {
            sockets[i] = new Socket(ip, workers_ports[i]);
            System.out.println("SOCKET = " + sockets[i]);

            reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
            writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())), true);
        }

        String message_to_send;
        message_to_send = String.valueOf(totalCount);

        long stopTime, startTime;
        FileWriterUtil fileWriterUtil = new FileWriterUtil("PiSocket", System.getenv("COMPUTERNAME"));

        for (int j = 0; j < numberOfRuns; j++) {
            total = 0;

            startTime = System.currentTimeMillis();
            // initialize workers
            for (int i = 0; i < numWorkers; i++) {
                writer[i].println(message_to_send); // send a message to each worker
            }

            //listen to workers's message 
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

            // System.out.println("\nPi : " + pi);
            // System.out.println("Error: " + (Math.abs((pi - Math.PI)) / Math.PI) + "\n");
            // System.out.println("Ntot: " + totalCount * numWorkers);
            // System.out.println("Available processors: " + numWorkers);
            // System.out.println("Time Duration (ms): " + (stopTime - startTime) + "\n");
            // System.out.println((Math.abs((pi - Math.PI)) / Math.PI) + " " + totalCount * numWorkers + " " + numWorkers + " " + (stopTime - startTime));
            Result result = new Result(total, (Math.abs((pi - Math.PI)) / Math.PI), pi, totalCount * numWorkers, numWorkers, (stopTime - startTime));

            // System.out.println(result);
            // System.out.println("\n Repeat computation (y/N): ");
            fileWriterUtil.writeToFile(result);
        }
        for (int i = 0; i < numWorkers; i++) {
            writer[i].println("END"); // send a message to stop each worker
        }
        System.out.println(fileWriterUtil.getFilePath());
    }

}
