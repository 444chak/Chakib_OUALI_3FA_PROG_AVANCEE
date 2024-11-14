package TP3_BAL;

/**
 * Classe Producteur
 */
public class Producteur extends Thread {

    /**
     * Default constructor
     */
    public Producteur() {
    }

    public Boite_aux_lettres boite_aux_lettres;

    /**
     * Fonction pour écrire une lettre
     */
    @Override
    public void run() {
        try {
            for (char lettre = 'A'; lettre <= 'Z'; lettre++) {
                Thread.sleep(500);
                boolean added = boite_aux_lettres.ecrire(String.valueOf(lettre));

                if (added) {
                    System.out.println("[" + Thread.currentThread().getName() + "]"
                            + "[" + boite_aux_lettres.getStock() + "] Ecriture de la lettre " + lettre);
                } else {
                    System.out.println("[" + Thread.currentThread().getName() + "]"
                            + "[" + boite_aux_lettres.getStock() + "] La boite est pleine");
                }
            }

        } catch (Exception e) {
            System.out.println("[" + Thread.currentThread().getName() + "]" + e.getMessage());
        }
    }

}
