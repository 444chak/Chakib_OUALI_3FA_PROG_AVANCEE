# Rapport - Calcul de $\pi$ par la méthode de Monte Carlo

## Introduction

Ce rapport présente l'implémentation et l'analyse de la méthode de Monte Carlo pour estimer la valeur de $\pi$. La méthode de Monte Carlo est une technique de simulation qui utilise des nombres aléatoires pour résoudre des problèmes mathématiques ou physiques. Dans ce cas, nous utilisons cette méthode pour estimer la valeur de $\pi$ en générant des points aléatoires dans un carré et en comptant combien de ces points tombent à l'intérieur d'un cercle inscrit dans ce carré.

## Principe de la méthode de Monte Carlo

La méthode de Monte Carlo pour estimer $\pi$ repose sur le fait que la probabilité qu'un point aléatoire tombe à l'intérieur d'un cercle est proportionnelle à la surface du cercle par rapport à la surface du carré qui l'entoure. En générant un grand nombre de points aléatoires et en comptant combien de ces points tombent à l'intérieur du cercle, nous pouvons estimer la valeur de $\pi$.

TODO : Pseudo-code, maths fait en cours au propre (avec graphique etc.)

## Implémentation

TODO : Rajouter UML

La méthode de Monte Carlo est implémentée en Java à partir de deux projets différents. Une, nommée *Assignment102*, développée par Karthik Jain (TODO:Source), et l'autre, *Pi*, développée par le Dr. Steve Kautz de l'IOWA State University (TODO:Source). Ces deux projets utilisent des threads pour exécuter les tâches Monte Carlo en parallèle et calculer la valeur de $\pi$ en fonction des résultats obtenus.

## Analyse des sources & Réorganisation

### *Assignment102*

À l'origine, le code source de *Assignment102* était contenu dans un seul fichier Java avec trois classes : `Assignment102`, `PiMonteCarlo` et `MonteCarlo`. La première classe est en réalité le point d'entrée du programme, qu'on inscrit dans un fichier séparé `Main.java`. Les deux autres classes sont des classes utilitaires pour le calcul de $\pi$ par la méthode de Monte Carlo. Pour une meilleure organisation du code, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java`, `PiMonteCarlo.java` et `MonteCarlo.java`.

`Main.java` contient les appels aux méthodes de calcul de $\pi$ et l'affichage des résultats. On remarque qu'elle affiche la valeur estimée de $\pi$ par le programme, la différence avec la valeur réelle de $\pi$ (récupérée de `Math.PI`) et le temps d'exécution du programme.

`PiMonteCarlo.java` contient la classe `PiMonteCarlo` qui initialise et appel les threads pour le calcul de $\pi$ par la méthode de Monte Carlo. Cette classe utilise la classe `MonteCarlo` pour effectuer les calculs.

`MonteCarlo.java` contient la classe `MonteCarlo` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Runnable` pour être exécutée par un thread.

### *Pi*

Le code source de *Pi* est également organisé en trois classes : `Pi`, `Master` et `Worker`. La classe `Pi` est le point d'entrée du programme. Et les deux classes suivent le modèle maître-esclave pour le calcul de $\pi$ par la méthode de Monte Carlo. Comme pour *Assignment102*, nous avons décidé de séparer ces classes dans des fichiers distincts : `Main.java` qui correspond à la classe `Pi`, `Master.java` et `Worker.java`.

`Main.java` contient l'appel à la classe `Master` pour lancer le calcul de $\pi$ par la méthode de Monte Carlo. Elle affiche également les résultats obtenus.

`Master.java` contient la classe `Master` qui initialise et gère les tâches de calcul de Monte Carlo. Elle utilise la classe `Worker` pour effectuer les calculs.

`Worker.java` contient la classe `Worker` qui effectue les calculs de Monte Carlo pour estimer la valeur de $\pi$. Cette classe implémente l'interface `Callable` pour renvoyer un résultat.

TODO : Sources, crédits
