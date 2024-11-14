package TP_1_Mobile;

import Semaphores.Semaphore;
import Semaphores.SemaphoreGeneral;
import java.awt.*;
import javax.swing.*;

class UnMobile extends JPanel implements Runnable {

    int saLargeur, saHauteur, sonDebDessin;
    final int sonPas = 10, sonCote = 40;
    static Semaphore sem = new SemaphoreGeneral(2);

    int sonTemps = (int) (Math.random() * ((40 - 5) + 1)) + 5;

    UnMobile(int telleLargeur, int telleHauteur) {
        super();
        saLargeur = telleLargeur;
        saHauteur = telleHauteur;
        setSize(telleLargeur, telleHauteur);
    }

    @Override
    public void run() {
        while (!Thread.currentThread().isInterrupted()) {
            int tiers = saLargeur / 3;
            int deuxTiers = 2 * saLargeur / 3;
            int finDessin = saLargeur - sonPas;
            // debut à 1/3 de la largeur
            for (sonDebDessin = 0; sonDebDessin < tiers; sonDebDessin += sonPas) {
                repaint();
                try {
                    Thread.sleep(sonTemps);
                } catch (InterruptedException Exp) {
                    Thread.currentThread().interrupt();
                }
            }
            // 1/3 de la largeur à 2/3 de la largeur
//            sem.syncWait();
            synchronized (JPanel.class) {
                for (sonDebDessin = tiers; sonDebDessin < deuxTiers; sonDebDessin += sonPas) {
                    repaint();
                    try {
                        Thread.sleep(sonTemps);
                    } catch (InterruptedException Exp) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
//            sem.syncSignal();

            // 2/3 de la largeur à la fin
            for (sonDebDessin = deuxTiers; sonDebDessin < finDessin; sonDebDessin += sonPas) {
                repaint();
                try {
                    Thread.sleep(sonTemps);
                } catch (InterruptedException Exp) {
                    Thread.currentThread().interrupt();
                }
            }

            // retour à gauche
            // fin à deux tiers de la largeur
            for (sonDebDessin = saLargeur - sonPas; sonDebDessin > deuxTiers; sonDebDessin -= sonPas) {
                // la position de départ est saLargeur - sonPas, c'est-à-dire la position d'arrêt de la première boucle,
                // on décrémente sonDebDessin de sonPas pour revenir à gauche
                repaint();
                try {
                    Thread.sleep(sonTemps);
                } catch (InterruptedException Exp) {
                    Thread.currentThread().interrupt();
                }
            }

            // deux tiers de la largeur à un tiers de la largeur
//            sem.syncWait();
            synchronized (JPanel.class) {
                for (sonDebDessin = deuxTiers; sonDebDessin > tiers; sonDebDessin -= sonPas) {
                    repaint();
                    try {
                        Thread.sleep(sonTemps);
                    } catch (InterruptedException Exp) {
                        Thread.currentThread().interrupt();
                    }
                }
            }
//            sem.syncSignal();

            // un tiers de la largeur à la fin
            for (sonDebDessin = tiers; sonDebDessin > 0; sonDebDessin -= sonPas) {
                repaint();
                try {
                    Thread.sleep(sonTemps);
                } catch (InterruptedException Exp) {
                    Thread.currentThread().interrupt();
                }
            }
        }
    }

    @Override
    public void paintComponent(Graphics telCG) {
        super.paintComponent(telCG);
        telCG.fillRect(sonDebDessin, saHauteur / 2, sonCote, sonCote);
    }
}
