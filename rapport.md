# Programmation parallèle sur machine à mémoire partagée

##  TD / TP 1 Mobile

### Analyse des sources

TODO : dossier de conception

starURL diagram de class

### Exercice 1

> Ecrire une classe UneFenetre dérivant de JFrame, cette classe aura un champ UnMobile
sonMobile, son constructeur devra ajouter sonMobile à la fenêtre, créer une thread avec sonMobile,
afficher la fenêtre et lancer la thread. Ecrire une classe Main testant la classe UneFenetre. 

La classe UneFenetre est définie dans le fichier `UneFenetre.java` :

Il faut instancier un objet de type UnMobile (appelé `mobileTask`), l'ajouter à la fenêtre, créer une thread (appelé `mobileThread`), afficher la fenêtre (et la paramétrer) et lancer la thread.
Les opérations peuvent être faites peu importe l'ordre, il ne s'agit pas de programmation séquentielle.

```java
public UneFenetre() {
        mobileTask = new UnMobile(LARG, HAUT);
        add(mobileTask); // ajouter sonMobile a la fenêtre
        Thread mobileThread = new Thread(mobileTask); // créer une thread mobileThread avec sonMobile
        setSize(LARG, HAUT); // définir la taille de la fenêtre
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // définir l'opération de fermeture par défaut
        setVisible(true);// afficher la fenêtre
        mobileThread.start(); // lancer mobileThread
    }
```

L'ordre suivant fonctionne tout autant que le précédent.

```java
public UneFenetre() {
    mobileTask = new UnMobile(LARG, HAUT);
    Thread mobileThread = new Thread(mobileTask); // créer une thread mobileThread avec sonMobile
    mobileThread.start(); // lancer mobileThread
    setSize(LARG, HAUT); // définir la taille de la fenêtre
    setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // définir l'opération de fermeture par défaut
    setVisible(true);// afficher la fenêtre
    add(mobileTask); // ajouter sonMobile a la fenêtre
}
```
---
> Faire en sorte que le mobile reparte en sens inverse lorsqu'il atteint une extrémité de la fenêtre

Il suffit de modifier la méthode `run` de la classe `UnMobile` pour que le mobile reparte en sens inverse lorsqu'il atteint une extrémité de la fenêtre.

```java
// pour revenir à gauche
for (sonDebDessin = saLargeur - sonPas; sonDebDessin > 0; sonDebDessin -= sonPas) {
    // la position de départ est saLargeur - sonPas, c'est-à-dire la position d'arrêt de la première boucle,
    // on décrémente sonDebDessin de sonPas pour revenir à gauche
    repaint();
    try {
        Thread.sleep(sonTemps);
    } catch (InterruptedException telleExcp) {
        telleExcp.printStackTrace();
    }
}
```