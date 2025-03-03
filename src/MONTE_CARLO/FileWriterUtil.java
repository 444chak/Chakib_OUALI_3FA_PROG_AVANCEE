package MONTE_CARLO;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

public class FileWriterUtil {

    private final String filePath;

    public FileWriterUtil(String AlgorithmName, String machineName) {

        String prefix = "./MONTE_CARLO/out/";
        String dateString = new java.text.SimpleDateFormat("yy-MM-dd__HH-mm-ss-ms").format(new Date());
        String fpath = prefix + AlgorithmName + "_" + dateString + "_" + machineName + ".txt";
        // check if exists 
        Boolean exists = new java.io.File(fpath).exists();
        if (exists) {
            this.filePath = fpath + "_1";
        } else {
            this.filePath = fpath;
        }
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write("NbProcess\tError\tEstimation\tNtot\tTime\tTotal");
            writer.newLine();
        } catch (IOException e) {
        }

    }

    public void writeToFile(Result result) {

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write(result.getNbProcess() + "\t" + result.getError() + "\t" + result.getEstimation() + "\t" + result.getNtot() + "\t" + result.getTime() + "\t" + result.getTotal());
            writer.newLine();
        } catch (IOException e) {
        }
    }

    public void writeToFile(String string) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath, true))) {
            writer.write(string);
            writer.newLine();
        } catch (IOException e) {
        }
    }

    public String getFilePath() {
        return filePath.replace("./src/MONTE_CARLO/out/",
                "");
    }
}
