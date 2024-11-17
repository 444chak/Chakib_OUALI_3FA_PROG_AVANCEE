package TP3_BAL;

import java.util.Random;

/**
 * Classe Consommateur
 */
public class Consommateur extends Thread {

    /**
     * Default constructor
     */
    public Consommateur() {
    }

    public Boite_aux_lettres boite_aux_lettres;

    private final Random rand = new Random();

    /**
     * Fonction pour lire une lettre
     */
    @Override
    public void run() {
        try {
            while (true) {
                Thread.sleep(rand.nextInt(2000));
                String lettre = boite_aux_lettres.retirer();
                if (lettre != null) {
                    System.out.println("[" + Thread.currentThread().getName() + "]"
                            + "[" + boite_aux_lettres.getStock() + "] Lecture de la lettre " + lettre);
                } else {
                    System.out.println("[" + Thread.currentThread().getName() + "]"
                            + "[" + boite_aux_lettres.getStock() + "] La boite est vide");
                }
            }

        } catch (Exception e) {
            System.out.println("[" + Thread.currentThread().getName() + "]" + e.getMessage());
        }
    }

}
