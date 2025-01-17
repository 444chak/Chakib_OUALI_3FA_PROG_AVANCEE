package MONTE_CARLO;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

public class FileWriterUtil {

    private final String filePath;

    public FileWriterUtil(String AlgorithmName, String machineName) {

        String prefix = "./src/MONTE_CARLO/out/";
        String dateString = new java.text.SimpleDateFormat("yy-MM-dd__HH-mm-ss").format(new Date());
        this.filePath = prefix + AlgorithmName + "_" + dateString + "_" + machineName + ".txt";
    }

    public void writeToFile(String error, String estimation, String numberCount, String nbProcess, String time) {

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            String c = error + " " + estimation + " " + numberCount + " " + nbProcess + " " + time;
            writer.write(c);
            writer.newLine();
        } catch (IOException e) {
        }
    }
}
