import javax.swing.*;

class UneFenetre extends JFrame {
    UnMobile mobileTask;
    private final int LARG = 400, HAUT = 250;

    public UneFenetre() {
        mobileTask = new UnMobile(LARG, HAUT);
        add(mobileTask); // ajouter sonMobile a la fenêtre
        Thread mobileThread = new Thread(mobileTask); // créer une thread mobileThread avec sonMobile
        setSize(LARG, HAUT); // définir la taille de la fenêtre
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // définir l'opération de fermeture par défaut
        setVisible(true);// afficher la fenêtre
        mobileThread.start(); // lancer mobileThread
    }
}
