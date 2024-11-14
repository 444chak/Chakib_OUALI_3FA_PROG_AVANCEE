package TP3_BAL;

import java.io.*;
import java.util.*;

/**
 * 
 */
public class Producteur extends Thread {

    /**
     * Default constructor
     */
    public Producteur() {
    }

    /**
     * 
     */
    public String lettre;

    /**
     * 
     */
    public Boite_aux_lettres boite_aux_lettres;

    /**
     * 
     */
    public void run() {
        try {
            boite_aux_lettres.ecrire(lettre);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

}