# Projet Gestion de projet - Projet Voiture

## Description

Ce projet consiste à concevoir un module mobile autonome capable de participer à une course de type Formule 1 sur un circuit défini. L'objectif est de concevoir, développer et tester un robot piloté par un Raspberry Pi 3, en utilisant la méthode Agile Scrum.

## Fonctionnalités réalisées

Le projet implémente les fonctionnalités suivantes, issues des **User Stories**, à l'exception des US **#9**, **#11**, **#14**, et **#15** :

### Pilote de course
- Visualisation en temps réel de la vitesse et de l'état du module.
- Arrêt précis sur la ligne d'arrivée.
- Manœuvrabilité optimisée pour les demi-tours.

### Directeur de course
- Définition dynamique du nombre de tours.
- Relance du module à distance en cas de panne.

### Mécanicien
- Mode test pour les capteurs et moteurs.
- Accès aux logs et diagnostics à distance.

### Superviseur Technique
- Connexion SSH/Wi-Fi avec le module.
- Réalisation de tests unitaires sur les capteurs et moteurs.
- Documentation des choix techniques.

## Fonctionnalités non réalisées

- [ ] **US#9** : Détection et évitement des obstacles.
- [ ] **US#11** : Optimisation des trajectoires.
- [ ] **US#14** : Faire un tour complet du circuit avec démarrage au feu vert et arrêt sur la ligne.
- [ ] **US#15** : Faire une course avec 4 autres modules.

## Technologies utilisées

- **Langage** : Python 3
- **Matériel** :
  - Raspberry Pi 3 Model B
  - Capteurs ultrason HC-SR04
  - Capteur infrarouge
  - Moteurs DC & servomoteurs
- **Méthodologie** : Scrum (Sprint Planning, Daily, Review & Rétrospective)
- **Outils** :
  - Trello pour le Scrum Board
  - GitHub pour la gestion du code
  - SSH & VNC pour le contrôle du module

## Installation

1. Flash de la carte µSD avec Raspbian (GUI).
2. Connexion SSH au Raspberry Pi.
3. Lancer le script d’initialisation :
   ```bash
   python3 main.py

