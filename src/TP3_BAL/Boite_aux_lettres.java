package TP3_BAL;

import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeUnit;

/**
 * Classe Boite_aux_lettres
 */
public class Boite_aux_lettres {

    /**
     * Default constructor
     */
    public Boite_aux_lettres() {
    }

    private final BlockingQueue<String> boite_aux_lettres = new ArrayBlockingQueue<>(10);

    /**
     * Fonction pour écrire une lettre
     *
     * @param lettre Lettre à écrire
     * @return boolean Retourne vrai si la lettre a été écrite
     */
    public synchronized boolean ecrire(String lettre) throws Exception {
        return boite_aux_lettres.offer(lettre, 2000, TimeUnit.MILLISECONDS);
    }

    /**
     * Fonction pour retirer une lettre
     *
     * @return String Retourne la lettre retirée
     */
    public synchronized String retirer() throws Exception {
        return boite_aux_lettres.poll(200, TimeUnit.MILLISECONDS);
    }

    /**
     * Fonction pour obtenir le stock de la boite aux lettres
     *
     * @return int Retourne le stock de la boite aux lettres
     */
    public int getStock() {
        return boite_aux_lettres.size();
    }

}
