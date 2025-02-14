# Rapport - Calcul de $\pi$ par la méthode de Monte Carlo - Programmation Avancée

Chakib OUALI - 3FA - 2024

---

## Table des matières

- [Rapport - Calcul de $\\pi$ par la méthode de Monte Carlo - Programmation Avancée](#rapport---calcul-de-pi-par-la-méthode-de-monte-carlo---programmation-avancée)
  - [Table des matières](#table-des-matières)
  - [Introduction](#introduction)
  - [Principe de la méthode de Monte Carlo](#principe-de-la-méthode-de-monte-carlo)
    - [Généralités](#généralités)
    - [Parallélisme](#parallélisme)
  - [Implémentation](#implémentation)
  - [Paradigmes de programmation utilisés](#paradigmes-de-programmation-utilisés)
    - [Parallélisme de boucle, itération parallèle](#parallélisme-de-boucle-itération-parallèle)
    - [Modèle master-worker](#modèle-master-worker)
  - [Analyse des sources \& Réorganisation](#analyse-des-sources--réorganisation)
    - [*Assignment102*](#assignment102)
    - [*Pi*](#pi)
      - [Main](#main)
      - [Master](#master)
      - [Worker](#worker)
  - [Utilisations de sockets](#utilisations-de-sockets)
    - [Analyse des sources](#analyse-des-sources)
      - [MasterSocket](#mastersocket)
      - [WorkerSocket](#workersocket)
  - [Automatisation de l'exécution des différents programmes](#automatisation-de-lexécution-des-différents-programmes)
  - [Analyse de performances](#analyse-de-performances)
    - [Définition de scalabilité faible et forte](#définition-de-scalabilité-faible-et-forte)
    - [Mesures de performances dans le cadre de la norme ISO/IEC 25010](#mesures-de-performances-dans-le-cadre-de-la-norme-isoiec-25010)
    - [1. **Functional Suitability (Adéquation fonctionnelle)**](#1-functional-suitability-adéquation-fonctionnelle)
    - [2. **Performance Efficiency (Efficacité des performances)**](#2-performance-efficiency-efficacité-des-performances)
    - [3. **Maintenability (Maintenabilité du code)**](#3-maintenability-maintenabilité-du-code)

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

<img src="assets/f1_monte_carlo.png" alt="Figure 1 : Illustration de la méthode de Monte Carlo pour estimer $\pi$" width="500">

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

## Paradigmes de programmation utilisés

### Parallélisme de boucle, itération parallèle

Le parallélisme de boucle est un paradigme de programmation parallèle qui consiste à exécuter plusieurs itérations d'une boucle en parallèle. Dans le cas de la méthode de Monte Carlo, chaque itération de la boucle consiste à générer un point aléatoire et à vérifier s'il tombe à l'intérieur du cercle. En parallélisant ces itérations, on peut accélérer le calcul de $\pi$.

### Modèle master-worker

Le modèle master-worker est un modèle de programmation parallèle dans lequel un processus maître distribue des tâches à des processus esclaves (ou workers) pour maximiser l'utilisation des ressources disponibles. Dans le cas de la méthode de Monte Carlo, le processus maître est responsable de diviser le travail en tâches et de les distribuer aux workers pour effectuer les calculs. Le processus maître agrège ensuite les résultats des workers pour obtenir une estimation de $\pi$.

## Analyse des sources & Réorganisation

### *Assignment102*

(Parallélisme de boucle, paradigme d'itération parallele)

À l'origine, le code source de *Assignment102* était contenu dans un seul fichier Java avec trois classes : `Assignment102`, `PiMonteCarlo` et `MonteCarlo`. La première classe est en réalité le point d'entrée du programme, qu'on inscrit dans un fichier séparé `Main.java`. Les deux autres classes sont des classes utilitaires pour le calcul de $\pi$ par la méthode de Monte Carlo. Pour une meilleure organisation du code, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java`, `PiMonteCarlo.java` et `MonteCarlo.java`.

`Main.java` contient les appels aux méthodes de calcul de $\pi$ et l'affichage des résultats. On remarque qu'elle affiche la valeur estimée de $\pi$ par le programme, la différence avec la valeur réelle de $\pi$ (récupérée de `Math.PI`) et le temps d'exécution du programme.

`PiMonteCarlo.java` contient la classe `PiMonteCarlo` qui initialise et appel les threads pour le calcul de $\pi$ par la méthode de Monte Carlo. Cette classe utilise la classe `MonteCarlo` pour effectuer les calculs.

`MonteCarlo.java` contient la classe `MonteCarlo` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Runnable` pour être exécutée par un thread.

Ci-après, le diagramme UML des classes *Assignment102* après réorganisation :

<img src="assets/Assignment102UML.jpg" alt="UML Assignment102" width="1000">

### *Pi*

(Paradigme master-worker)

Le code source de *Pi* est également organisé en trois classes : `Pi`, `Master` et `Worker`. La classe `Pi` est le point d'entrée du programme. Et les deux classes suivent le modèle maître-esclave pour le calcul de $\pi$ par la méthode de Monte Carlo. Comme pour *Assignment102*, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java` qui correspond à la classe `Pi`, `Master.java` et `Worker.java`.

#### Main

`Main.java` contient l'appel à la classe `Master` pour lancer le calcul de $\pi$ par la méthode de Monte Carlo. Elle affiche également les résultats obtenus.

#### Master

`Master.java` contient la classe `Master` qui initialise et gère les tâches de calcul de Monte Carlo. Elle utilise la classe `Worker` pour effectuer les calculs.

#### Worker

`Worker.java` contient la classe `Worker` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Callable` pour renvoyer un résultat.

Ce programme suit le paradigme master-worker pour paralléliser le calcul de $\pi$ par la méthode de Monte Carlo. Le maître initialise les workers, leur envoie les tâches à effectuer et agrège les résultats pour obtenir une estimation de $\pi$. Dans le code, le maître est représenté par la classe `Master` et les workers par la classe `Worker`.

TODO : UML

## Utilisations de sockets

### Analyse des sources

Le code source dédié à la programmation à mémoire distribuée utilise des sockets en Java pour envoyer et recevoir des messages entre les machines. Deux fichiers sont à notre disposition : `MasterSocket.java` et `WorkerSocket.java`. On en déduit que le programme suit le modèle master-worker.

#### MasterSocket

Dans un premier temps, on initialise un nombre de workers avec leurs ports respectifs. Pour chaque worker, on crée un socket et on envoie le nombre d'itérations à effectuer pour le calcul de $\pi$. Ensuite, on attend les résultats de chaque worker et on les agrège pour obtenir une estimation de $\pi$.

#### WorkerSocket

Chaque worker crée un socket pour recevoir le nombre d'itérations à effectuer pour le calcul de $\pi$. Pour l'instant le worker n'effectue pas le calcul de Pi.

Pour compléter le programme, il faudrait ajouter la méthode de Monte Carlo pour le calcul de $\pi$ dans la classe `WorkerSocket`. Pour cela, on utilise le code de la `Pi` pour calculer la valeur de $\pi$. On envoie ensuite le résultat au maître pour l'agrégation.

TODO : Rajouter UML

Pour lancer le programme, il faut exécuter nos WorkerSocket avec les ports correspondants, puis exécuter le MasterSocket avec les ports des workers définit précédemment.

## Automatisation de l'exécution des différents programmes

Pour automatiser l'exécution des différents programmes *Assignment102*, *Pi* et *PiSocket*, il a fallu créer une classe main sous cette forme :

```java
...
 public static void main(String[] args) throws Exception {

  int workers;
  int numberOfRuns;
  int totalCount;
  String algo = "";

  if (args.length > 0) {
      workers = Integer.parseInt(args[0]);
      numberOfRuns = Integer.parseInt(args[1]);
      totalCount = Integer.parseInt(args[2]);
      algo = args[3];

  } else {
      workers = 5;
      numberOfRuns = 10;
      totalCount = 10000000;
      algo = "pi";
  }

  // Assignment 102
  if (algo.equals("ass102")) {
      runAssignment102(numberOfRuns, totalCount, machineName, workers);
  }
  if (algo.equals("pi")) {
      runPi(numberOfRuns, totalCount, machineName, workers);
  }
  if (algo.equals("socket")) {
      runMasterWorkerSocket(workers, totalCount, numberOfRuns);
  }
}
```

L'objectif étant de lancer le programme avec les paramètres qui nous intéressent. Par exemple, pour lancer le programme *Assignment102* avec 5 workers, 10 runs et 10000000 itérations, on exécute la commande suivante :

```bash
java Main 5 10 10000000 ass102
```

Pour prévoir les tests des différents algorithmes et l'analyse de performance, on a ajouté une classe permettant d'inscrire les résultats dans un fichier. Il s'agit de la classe `FileWriterUtil`. Cette classe créer un fichier dans le répertoire `out` avec en paramètre un objet `Result`. Ces fichiers sont créés dans notre classe `Main` après chaque exécution des algorithmes.

Un fichier de résultat se présente sous cette forme :

```txt
NbProcess Error Estimation Ntot Time Total
1-------------------
1 2.2557144351084918E-4 3.140884 1000000 58 785221
1 3.664849447910635E-4 3.142744 1000000 23 785686
...
2-------------------
2 0.0010463948616796842 3.14488 1000000 9 786220
...
```

## Analyse de performances

### Définition de scalabilité faible et forte

La scalabilité est la capacité d'un système à s'adapter à une charge de travail croissante ou à augmenter le nombre de ressources pour améliorer les performances. On distingue deux types de scalabilité :

- La scalabilité forte : la capacité d'un système à maintenir un niveau de performance constant lorsqu'on augmente le nombre de ressources (par exemple, le nombre de processeurs).
- La scalabilité faible : la capacité d'un système à maintenir un niveau de performance constant lorsqu'on augmente la charge de travail (par exemple, le nombre de tâches à effectuer).

Pour mesurer la scalabilité, on utilise le speedup, qui est le rapport entre le temps d'exécution d'un programme sur un seul processeur et le temps d'exécution du même programme sur plusieurs processeurs. On peut calculer le speedup comme suit :

$$
\text{Speedup} = \frac{T_{1}}{T_{n}}
$$

où :

- $T_{1}$ est le temps d'exécution du programme sur un seul processeur.
- $T_{n}$ est le temps d'exécution du programme sur $n$ processeurs.

Le speedup idéal est linéaire, c'est-à-dire que le speedup est égal au nombre de processeurs utilisés. Cependant, en pratique, le speedup est souvent inférieur au nombre de processeurs en raison des surcharges de communication et de synchronisation entre les processeurs (overhead).

<img src="assets/f2_perfect_speedup.png" alt="Speedup" width="500">

*Figure 2 : Speedup idéal*

Dans cette figure la droite noire correspond le speedup idéal dans le cas de la scalabilité forte. La droite bleue correspond quant à elle à la scalabilité faible.

Ainsi, grâce à l'automatisation de l'exécution des différents programmes et de l'écriture des résultats dans un fichier, on peut facilement analyser les performances des algorithmes et mesurer leur scalabilité.

### Mesures de performances dans le cadre de la norme ISO/IEC 25010

La norme *ISO/IEC 25010* définit un cadre pour évaluer la qualité des logiciels en se basant sur plusieurs critères. Dans le cas du calcul de $\pi$ par la méthode de Monte Carlo, plusieurs mesures peuvent être appliquées pour évaluer les performances du programme.  

### 1. **Functional Suitability (Adéquation fonctionnelle)**  

L’adéquation fonctionnelle mesure la capacité du logiciel à fournir des fonctions qui répondent aux besoins spécifiés. Dans notre cas, cela se traduit par la justesse du calcul de $\pi$.  

- **Functional Correctness (Correction fonctionnelle)**  
  - On compare la valeur estimée de $\pi$ avec la valeur réelle (`Math.PI` en Java).  
  - Une erreur relative peut être calculée (c'est celle qu'on utilise dans nos programme et qu'on enregistre dans les fichiers de résultats) :  
    $$ \text{Erreur} = \left| \frac{\pi_{\text{estimé}} - \pi_{\text{réel}}}{\pi_{\text{réel}}} \right| $$  
  - Le nombre d’itérations influence la précision du résultat.  

### 2. **Performance Efficiency (Efficacité des performances)**  

Ce critère mesure la rapidité et l’utilisation des ressources du programme.  

- **Time Behavior (Comportement temporel)**  
  - **Temps d’exécution total** :  
    On mesure le temps nécessaire pour exécuter l’algorithme en fonction du nombre de threads (`T_n`).  
  - **Speedup** :  
    On évalue l’accélération obtenue en augmentant le nombre de cœurs processeurs (`P`) :  
    $$ \text{Speedup} = \frac{T_1}{T_P} $$  
  - **Évolution du temps d’exécution** en fonction du nombre d’itérations (`N`).  

- **Resource Utilization (Utilisation des ressources)**  
  - Utilisation du processeur (`CPU usage`).  
  - Occupation mémoire (quantité de RAM utilisée).  
  - Bande passante consommée dans le cas de la version distribuée (sockets).  

- **Capacity (Capacité maximale)**  
  - Combien de threads (workers) peuvent être utilisés **avant que la performance ne se dégrade** ?  
  - Influence du **nombre de processus (`P`) sur l’overhead** (communication entre threads ou machines).  

### 3. **Maintenability (Maintenabilité du code)**  

- **Modularity (Modularité)** :  
  - Séparation des responsabilités en classes (`Main`, `Master`, `Worker`).  
  - Découpage du code en fichiers distincts (`Assignment102.java`, `Pi.java`, etc.).  
- **Reusability (Réutilisabilité)** :  
  - Possibilité de réutiliser la classe `Worker` dans d’autres simulations Monte Carlo.  
- **Testability (Testabilité)** :  
  - Facilité à tester la précision du calcul en automatisant la comparaison avec la vraie valeur de $\pi$.  

En appliquant ces critères de la norme *ISO/IEC 25010*, nous pouvons analyser les performances du programme et identifier des pistes d’amélioration. Les principaux défis sont la gestion de l’overhead et l’optimisation du parallélisme pour maximiser le speedup et l’efficacité de l’algorithme.

TODO : Sources, crédits
