import java.awt.*;
import javax.swing.*;

class UneFenetre extends JFrame {
    UnMobile sonMobile;
    private final int LARG = 400, HAUT = 250;

    public UneFenetre() {
        sonMobile = new UnMobile(LARG, HAUT);
        add(sonMobile); // ajouter sonMobile a la fenetre
        Thread laThread = new Thread(sonMobile); // creer une thread laThread avec sonMobile
        setSize(LARG, HAUT); // définir la taille de la fenêtre
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // définir l'opération de fermeture par défaut
        setVisible(true);// afficher la fenetre
        laThread.start(); // lancer laThread
    }
}
