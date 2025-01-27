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
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write("Error\tEstimation\tNtot\tNbProcess\tTime\tTotal");
            writer.newLine();
        } catch (IOException e) {
        }
    }

    public void writeToFile(Result result) {

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write(result.getError() + "\t" + result.getEstimation() + "\t" + result.getNtot() + "\t" + result.getNbProcess() + "\t" + result.getTime() + "\t" + result.getTotal());
            writer.newLine();
        } catch (IOException e) {
        }
    }
}
