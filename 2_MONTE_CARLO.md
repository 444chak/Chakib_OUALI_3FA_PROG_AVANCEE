# Rapport - Calcul de $\pi$ par la méthode de Monte Carlo - Programmation Avancée

Chakib OUALI - 3FA - 2024

---

## Introduction

Ce rapport présente l'implémentation et l'analyse de la méthode de Monte Carlo pour estimer la valeur de $\pi$. La méthode de Monte Carlo est une technique de simulation qui utilise des nombres aléatoires pour résoudre des problèmes mathématiques ou physiques. Dans ce cas, nous utilisons cette méthode pour estimer la valeur de $\pi$ en générant des points aléatoires dans un carré et en comptant combien de ces points tombent à l'intérieur d'un cercle inscrit dans ce carré.

## Principe de la méthode de Monte Carlo

### Généralités

La méthode de Monte Carlo pour estimer $\pi$ repose sur le fait que la probabilité qu'un point aléatoire tombe à l'intérieur d'un cercle est proportionnelle à la surface du cercle par rapport à la surface du carré qui l'entoure. En générant un grand nombre de points aléatoires et en comptant combien de ces points tombent à l'intérieur du cercle, nous pouvons estimer la valeur de $\pi$.

On défini un carré de côté 1, et un cercle de rayon 1 inscrit dans ce carré. La surface du carré est de 1, et la surface du cercle est de $\pi$. La probabilité qu'un point aléatoire tombe à l'intérieur du cercle est donc $\frac{\pi}{4}$, car la surface du cercle est $\pi$ et la surface du carré est 4.
La probabilité qu'un point aléatoire tombe à l'intérieur du cercle se calcule donc comme suit :

$$
P(X_{p} | d_{p} < 1) = \frac{\pi}{4}
$$

Avec

- $X_{p}$ : le point aléatoire
- $d_{p}$ : la distance entre le point aléatoire et le centre du cercle
  - c'est à dire $\sqrt{x_{p}^2 + y_{p}^2}$ avec $x_{p}$ et $y_{p}$ les coordonnées du point aléatoire

On peut illustrer ce problème avec un tel graphique :  

![Figure 1](assets/f1_monte_carlo.png)
*Figure 1 : Illustration de la méthode de Monte Carlo pour estimer $\pi$*

- L'équation de la courbe (cercle) est $x^2 + y^2 = 1$.  
- On place aléatoirement des points dans le carré de côté 1, et on compte combien de ces points tombent à l'intérieur du cercle.  

D'un point de vue algorithmique, on peut résumer la méthode de Monte Carlo pour estimer $\pi$ comme suit :

```pseudo
nombre_de_points_dans_le_cercle = 0
nombre_de_points_total = 0
nombre_de_points_total_max = 1000000 

tant que nombre_de_points_total < nombre_de_points_total_max:
    x = random(0, 1)
    y = random(0, 1)
    distance = sqrt(x^2 + y^2)
    
    si distance < 1:
        nombre_de_points_dans_le_cercle += 1
    
    nombre_de_points_total += 1
fin tant que

pi_estime = 4 * nombre_de_points_dans_le_cercle / nombre_de_points_total
```

### Parallélisme

Pour accélérer le calcul de $\pi$ par la méthode de Monte Carlo, on peut paralléliser le calcul.  
Le modèle de parallélisme choisi est la parallélisation par tâches.

Les tâches dans notre algorithmes sont les suivantes :

- Compter le nombre de points aléatoires qui tombent à l'intérieur du cercle
- Agréger les résultats de chaque tâche pour obtenir une estimation de $\pi$

Les sous-tâches quant à elles sont les suivantes :

- Générer $i$ points aléatoires
- Incrémenter le compteur de points dans le cercle si le point est à l'intérieur du cercle
- Renvoyer le nombre de points dans le cercle

On peut dans un premier temps définir en tant que section critique la condition pour incrémenter le compteur de points dans le cercle et l'incrémentation elle-même.

On obtient cet algorithme :

```pseudo
nombre_de_points_dans_le_cercle = 0
nombre_de_points_total = 0
nombre_de_points_total_max = 1000000

fonction critique condition_incrementation(distance):
    si distance < 1:
        nombre_de_points_dans_le_cercle += 1

pour x de 0 à nombre_de_points_total_max:
    x = random(0, 1)
    y = random(0, 1)
    distance = sqrt(x^2 + y^2)
    condition_incrementation(distance)
fin pour

pi_estime = 4 * nombre_de_points_dans_le_cercle / nombre_de_points_total
```

On peut également faire des boucles intermédiaires pour diviser le travail entre plusieurs threads.

```pseudo
nombre_de_points_dans_le_cercle = 0
nombre_de_points_total = 0
nombre_de_points_total_max = 1000000
nombre_de_threads = 4
nombre_de_points_par_thread = nombre_de_points_total_max / nombre_de_threads

fonction critique condition_incrementation(distance):
    si distance < 1:
        nombre_de_points_dans_le_cercle += 1

pour i de 0 à nombre_de_threads:
    lancer_thread(generer_points, nombre_de_points_par_thread)
fin pour

pi_estime = 4 * nombre_de_points_dans_le_cercle / nombre_de_points_total
```

Ici, chaque thread est responsable de générer un certain nombre de points aléatoires et de compter combien de ces points tombent à l'intérieur du cercle. Les résultats de chaque thread sont ensuite agrégés pour obtenir une estimation de $\pi$.

## Implémentation

La méthode de Monte Carlo est implémentée en Java à partir de deux projets différents. Une, nommée *Assignment102*, développée par Karthik Jain (TODO:Source), et l'autre, *Pi*, développée par le Dr. Steve Kautz de l'IOWA State University (TODO:Source). Ces deux projets utilisent des threads pour exécuter les tâches Monte Carlo en parallèle et calculer la valeur de $\pi$ en fonction des résultats obtenus.

## Analyse des sources & Réorganisation

### *Assignment102*

(Parallélisme de boucle, paradigme d'itération parallele)

À l'origine, le code source de *Assignment102* était contenu dans un seul fichier Java avec trois classes : `Assignment102`, `PiMonteCarlo` et `MonteCarlo`. La première classe est en réalité le point d'entrée du programme, qu'on inscrit dans un fichier séparé `Main.java`. Les deux autres classes sont des classes utilitaires pour le calcul de $\pi$ par la méthode de Monte Carlo. Pour une meilleure organisation du code, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java`, `PiMonteCarlo.java` et `MonteCarlo.java`.

`Main.java` contient les appels aux méthodes de calcul de $\pi$ et l'affichage des résultats. On remarque qu'elle affiche la valeur estimée de $\pi$ par le programme, la différence avec la valeur réelle de $\pi$ (récupérée de `Math.PI`) et le temps d'exécution du programme.

`PiMonteCarlo.java` contient la classe `PiMonteCarlo` qui initialise et appel les threads pour le calcul de $\pi$ par la méthode de Monte Carlo. Cette classe utilise la classe `MonteCarlo` pour effectuer les calculs.

`MonteCarlo.java` contient la classe `MonteCarlo` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Runnable` pour être exécutée par un thread.

Ci-après, le diagramme UML des classes *Assignment102* après réorganisation :

![UML Assignment102](assets/Assignment102UML.jpg)

### *Pi*

(Paradigme master-worker)

Le code source de *Pi* est également organisé en trois classes : `Pi`, `Master` et `Worker`. La classe `Pi` est le point d'entrée du programme. Et les deux classes suivent le modèle maître-esclave pour le calcul de $\pi$ par la méthode de Monte Carlo. Comme pour *Assignment102*, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java` qui correspond à la classe `Pi`, `Master.java` et `Worker.java`.

#### Main

`Main.java` contient l'appel à la classe `Master` pour lancer le calcul de $\pi$ par la méthode de Monte Carlo. Elle affiche également les résultats obtenus.

#### Master

`Master.java` contient la classe `Master` qui initialise et gère les tâches de calcul de Monte Carlo. Elle utilise la classe `Worker` pour effectuer les calculs.

#### Worker

`Worker.java` contient la classe `Worker` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Callable` pour renvoyer un résultat.

## Utilisations de sockets

### Analyse des sources

Le code source dédié à la programmation à mémoire distribuée utilise des sockets en Java pour envoyer et recevoir des messages entre les machines. Deux fichiers sont à notre disposition : `MasterSocket.java` et `WorkerSocket.java`. On en déduit que le programme suit le modèle master-worker.

#### MasterSocket

Dans un premier temps, on initialise un nombre de workers avec leurs ports respectifs. Pour chaque worker, on crée un socket et on envoie le nombre d'itérations à effectuer pour le calcul de $\pi$. Ensuite, on attend les résultats de chaque worker et on les agrège pour obtenir une estimation de $\pi`.

TODO : Rajouter UML

#### WorkerSocket

Chaque worker crée un socket pour recevoir le nombre d'itérations à effectuer pour le calcul de $\pi`. Pour l'instant le worker n'effectue pas le calcul de Pi.

TODO : Rajouter UML

---

Pour lancer le programme, il faut exécuter nos WorkerSocket avec les ports correspondants, puis exécuter le MasterSocket avec les ports des workers définit précédemment.

TODO : Sources, crédits
