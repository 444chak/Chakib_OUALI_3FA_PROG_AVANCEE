package TP3_BAL;

/**
 * 
 */
public class Boite_aux_lettres {

    /**
     * Default constructor
     */
    public Boite_aux_lettres() {
    }

    /**
     * 
     */
    private String lettre;

    /**
     * 
     */
    public boolean disponible = true;

    /**
     * @param lettre
     */
    public synchronized void ecrire(String lettre) throws Exception {
        if (disponible) {
            this.lettre = lettre;
            disponible = false;
        } else {
            throw new Exception("La boite est pleine");
        }
    }

    /**
     * @return
     */
    public synchronized String retirer() throws Exception {
        if (!disponible) {
            disponible = true;
            return lettre;
        } else {
            throw new Exception("La boite est vide");
        }
    }

}