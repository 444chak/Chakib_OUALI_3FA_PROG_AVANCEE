package TP2_Affichage;

/**
 * La classe TP2_Affichage.Affichage étend Thread et est utilisée pour afficher
 * une chaîne de caractères caractère par caractère. Elle utilise un sémaphore
 * pour s'assurer qu'un seul thread peut accéder à la section critique à la
 * fois.
 */
import Semaphores.Semaphore;
import Semaphores.SemaphoreBinaire;

public class Affichage extends Thread {

    String texte; // Le texte à afficher

    // Un sémaphore binaire pour contrôler l'accès à la section critique
    static Semaphore sem = new SemaphoreBinaire(1);

    /**
     * Constructeur pour initialiser le texte à afficher.
     *
     * @param txt Le texte à afficher
     */
    public Affichage(String txt) {
        texte = txt;
    }

    /**
     * La méthode run contient le code à exécuter par le thread. Elle utilise le
     * sémaphore pour assurer l'exclusion mutuelle lors de l'affichage du texte.
     */
    public void run() {

        // // Utilisation de synchronized pour contrôler l'accès à la section critique
        // synchronized (System.out) { //section critique
        //     for (int i = 0; i < texte.length(); i++) {
        //         System.out.print(texte.charAt(i));
        //         try {
        //             sleep(0);
        //         } catch (InterruptedException e) {
        //         }
        //         ;
        //     }
        // }
        // Utilisation de la classe Semaphore pour contrôler l'accès à la section critique
        sem.syncWait(); // Attendre que le sémaphore soit disponible
        for (int i = 0; i < texte.length(); i++) {
            System.out.print(texte.charAt(i)); // Afficher chaque caractère du texte
            try {
                sleep(0); // Dormir pendant une courte durée pour simuler un délai
            } catch (InterruptedException e) {
            }
        }
        sem.syncSignal(); // Signaler le sémaphore pour libérer le verrou
    }
}
