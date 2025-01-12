# Rapport - Calcul de $\pi$ par la méthode de Monte Carlo

## Introduction

Ce rapport présente l'implémentation et l'analyse de la méthode de Monte Carlo pour estimer la valeur de π. La méthode de Monte Carlo est une technique de simulation qui utilise des nombres aléatoires pour résoudre des problèmes mathématiques ou physiques. Dans ce cas, nous utilisons cette méthode pour estimer la valeur de π en générant des points aléatoires dans un carré et en comptant combien de ces points tombent à l'intérieur d'un cercle inscrit dans ce carré.

## Principe de la méthode de Monte Carlo

La méthode de Monte Carlo pour estimer π repose sur le fait que la probabilité qu'un point aléatoire tombe à l'intérieur d'un cercle est proportionnelle à la surface du cercle par rapport à la surface du carré qui l'entoure. En générant un grand nombre de points aléatoires et en comptant combien de ces points tombent à l'intérieur du cercle, nous pouvons estimer la valeur de π.

TODO : Pseudo-code, maths fait en cours au propre (avec graphique etc.)

## Implémentation

TODO : Rajouter UML

L'implémentation de cette méthode en Java utilise plusieurs classes pour structurer le code et tirer parti des fonctionnalités de parallélisme offertes par le langage. Les principales classes utilisées sont :

- `Main` : Contient la méthode principale pour exécuter le programme.
- `PiMonteCarlo` : Classe principale pour estimer la valeur de π en utilisant la méthode de Monte Carlo.
- `MonteCarlo` : Classe qui représente une tâche de simulation Monte Carlo.
- `Master` : Coordonne l'exécution des tâches Monte Carlo en utilisant un pool de threads.
- `Worker` : Représente une tâche individuelle de simulation Monte Carlo.

## Analyse des sources

### Classe `Main`

La classe `Main` initialise une instance de `PiMonteCarlo` avec un nombre donné de lancers et mesure le temps d'exécution pour estimer la valeur de π.

### Classe PiMonteCarlo

La classe PiMonteCarlo utilise un pool de threads pour exécuter les tâches Monte Carlo en parallèle et calcule la valeur de π en fonction des résultats obtenus.

### Classe MonteCarlo

La classe MonteCarlo représente une tâche de simulation Monte Carlo qui génère des points aléatoires et compte ceux qui tombent à l'intérieur du cercle.

### Classe Master

La classe `Master` coordonne l'exécution des tâches Monte Carlo en utilisant un pool de threads. Elle soumet les tâches à un `ExecutorService` et attend que toutes les tâches soient terminées pour calculer la valeur finale de π.

### Classe Worker

La classe `Worker` représente une tâche individuelle de simulation Monte Carlo. Elle implémente l'interface `Callable` pour permettre la récupération du résultat de chaque tâche.

## Réorganisation des fichiers

Pour améliorer la structure du projet, chaque classe doit être placée dans un fichier séparé :

- `Main.java`
- `PiMonteCarlo.java`
- `MonteCarlo.java`
- `Master.java`
