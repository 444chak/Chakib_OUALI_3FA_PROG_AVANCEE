package MONTE_CARLO;

public class Result {

    private final long total;
    private final double error;
    private final double estimation;
    private final int ntot;
    private final int nbProcess;
    private long time;

    public Result(long total, double error, double estimation, int ntot, int nbProcess, long time) {
        this.total = total;
        this.error = error;
        this.estimation = estimation;
        this.ntot = ntot;
        this.nbProcess = nbProcess;
        this.time = time;
    }

    public void setTime(long time) {
        this.time = time;
    }

    public long getTotal() {
        return total;
    }

    public double getError() {
        return error;
    }

    public double getEstimation() {
        return estimation;
    }

    public int getNtot() {
        return ntot;
    }

    public int getNbProcess() {
        return nbProcess;
    }

    public long getTime() {
        return time;
    }

    @Override
    public String toString() {
        return "Result{" + "total=" + total + ", error=" + error + ", estimation=" + estimation + ", ntot=" + ntot + ", nbProcess=" + nbProcess + ", time=" + time + '}';
    }
}
