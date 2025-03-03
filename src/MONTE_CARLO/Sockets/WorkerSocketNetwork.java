package MONTE_CARLO.Sockets;

import MONTE_CARLO.Pi.Master;
import MONTE_CARLO.Result;
import java.io.*;
import java.net.*;

/**
 * Worker is a server. It receives requests from Master.
 *
 * @see MasterSocket
 */
public class WorkerSocketNetwork {

    static int port = 25545;
    private static boolean isRunning = true;

    /**
     * compute PI locally by MC and sends the number of points inside the disk
     * to Master.
     */
    public static void main(String[] args) throws Exception {

        // port number
        if (!("".equals(args[0]))) {
            port = Integer.parseInt(args[0]);
        }
        ServerSocket s = new ServerSocket(port);
        Socket soc = s.accept();

        System.out.println("Server started on port " + port);

        // Reading message from Master
        BufferedReader bRead = new BufferedReader(new InputStreamReader(soc.getInputStream()));

        // Sending message to Master
        PrintWriter pWrite = new PrintWriter(new BufferedWriter(new OutputStreamWriter(soc.getOutputStream())), true);
        String str;
        String str2;
        while (isRunning) {
            str = bRead.readLine(); // read message from Master
            str2 = bRead.readLine(); // read message from Master
            if (str == null || str.equals("END")) {
                isRunning = false;
            } else {
                System.out.println("Server receives totalCount = " + str);
                int numIterations = Integer.parseInt(str);
                Master master = new Master();
                int numWorkers = Integer.parseInt(str2);
                System.out.println("runned with " + numWorkers + " workers");
                Result result = master.doRun(numIterations / numWorkers, numWorkers, false, false);
                long circleCount = result.getTotal();
                System.out.println("circleCount = " + circleCount);
                System.out.println("Time = " + result.getTime());
                pWrite.println(circleCount);
            }
        }
        bRead.close();
        pWrite.close();
        soc.close();
        s.close();
    }
}
