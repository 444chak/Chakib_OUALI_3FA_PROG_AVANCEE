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

    static int maxServer = 8;
    static final int[] tab_port = {25545, 25546, 25547, 25548, 25549, 25550, 25551, 25552, 25553, 25554, 25555, 25556, 25557, 25558, 25559, 25560}; // 16 ports

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

        System.out.println("#########################################");
        System.out.println("# Computation of PI by MC method        #");
        System.out.println("#########################################");

        if (args.length > 0) {
            numWorkers = Integer.parseInt(args[0]);
            if (numWorkers > maxServer) {
                throw new IllegalArgumentException("Number of workers must be less than " + maxServer);
            }
            totalCount = Integer.parseInt(args[1]) / numWorkers;
        } else {
            throw new IllegalArgumentException("Number of workers is required and total count is required");
        }

        //create worker's socket
        for (int i = 0; i < numWorkers; i++) {
            sockets[i] = new Socket(ip, tab_port[i]);
            System.out.println("SOCKET = " + sockets[i]);

            reader[i] = new BufferedReader(new InputStreamReader(sockets[i].getInputStream()));
            writer[i] = new PrintWriter(new BufferedWriter(new OutputStreamWriter(sockets[i].getOutputStream())), true);
        }

        String message_to_send;
        message_to_send = String.valueOf(totalCount);

        long stopTime, startTime;
        FileWriterUtil fileWriterUtil = new FileWriterUtil("PiSocket", System.getenv("COMPUTERNAME"));

        for (int j = 0; j < 10; j++) {
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

            System.out.println("\nPi : " + pi);
            System.out.println("Error: " + (Math.abs((pi - Math.PI)) / Math.PI) + "\n");

            System.out.println("Ntot: " + totalCount * numWorkers);
            System.out.println("Available processors: " + numWorkers);
            System.out.println("Time Duration (ms): " + (stopTime - startTime) + "\n");

            System.out.println((Math.abs((pi - Math.PI)) / Math.PI) + " " + totalCount * numWorkers + " " + numWorkers + " " + (stopTime - startTime));

            Result result = new Result(total, (Math.abs((pi - Math.PI)) / Math.PI), pi, totalCount * numWorkers, numWorkers, (stopTime - startTime));

            System.out.println("\n Repeat computation (y/N): ");
            fileWriterUtil.writeToFile(result);
        }
        System.out.println(fileWriterUtil.getFilePath());

    }
}
