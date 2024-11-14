package TP3_BAL;

import java.io.*;
import java.util.*;

/**
 * 
 */
public class Consommateur extends Thread {

    /**
     * Default constructor
     */
    public Consommateur() {
    }

    /**
     * 
     */
    public Boite_aux_lettres boite_aux_lettres;

    /**
     * 
     */
    public void run() {
        try {
            String lettre = boite_aux_lettres.retirer();
            System.out.println(lettre);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

}