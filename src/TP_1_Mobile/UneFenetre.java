package TP_1_Mobile;

import javax.swing.*;
import java.awt.*;

class UneFenetre extends JFrame {
    private final int LARG = 400;
    private final int MOBILE_LARG = 400, MOBILE_HAUT = 10;
    private final int MOBILE_COUNT = 20;

    public UneFenetre() {
        Container container = getContentPane(); // obtenir le conteneur de la fenêtre
        container.setLayout(new GridLayout(MOBILE_COUNT, 1)); // définir le gestionnaire de mise en page du conteneur

        UnMobile[] mobiles = new UnMobile[MOBILE_COUNT];
        Thread[] mobileThreads = new Thread[MOBILE_COUNT];
//        JButton[] boutons = new JButton[MOBILE_COUNT];
        for (int i = 0; i < mobiles.length; i++) {
            mobiles[i] = new UnMobile(MOBILE_LARG, MOBILE_HAUT);
            container.add(mobiles[i]);
            mobileThreads[i] = new Thread(mobiles[i]);
            mobileThreads[i].start();

//            boutons[i] = new JButton("Arrêter/Reprendre");
//            container.add(boutons[i]);
        }

//        for (int i = 0; i < mobiles.length; i++) {
//            int finalI = i;
//            boutons[i].addActionListener(e -> {
//                if (mobileThreads[finalI].isAlive()) {
//                    mobileThreads[finalI].interrupt();
//                } else {
//                    mobileThreads[finalI] = new Thread(mobiles[finalI]);
//                    mobileThreads[finalI].start();
//                }
//            });
//        }

//        setSize(LARG * 2, MOBILE_HAUT * MOBILE_COUNT * 2); // définir la taille de la fenêtre
        setSize(LARG, MOBILE_HAUT * MOBILE_COUNT * 2); // définir la taille de la fenêtre
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // définir l'opération de fermeture par défaut
        setVisible(true);// afficher la fenêtre
    }
}
