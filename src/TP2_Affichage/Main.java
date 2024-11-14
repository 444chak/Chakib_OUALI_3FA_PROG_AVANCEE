package TP2_Affichage;

public class Main {

    public static void main(String[] args) {
        Affichage TA = new Affichage("AAA");
        Affichage TB = new Affichage("BB");
        Affichage TC = new Affichage("CCCC");
        Affichage TD = new Affichage("DDD");

        TA.start();
        TC.start();
        TB.start();
        TD.start();

    }

}
