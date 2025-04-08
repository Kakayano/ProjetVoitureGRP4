# Projet Robot de Course F1 - Bachelier Informatique et Systèmes

## Description du projet

Le projet consiste à développer un module mobile en Python 3, capable de participer à une course de Formule 1 sur un circuit défini par les enseignants. Le robot devra être capable de :

- Effectuer un tour complet du circuit, avec chronométrage.
- S'arrêter après la ligne d'arrivée.
- Détecter et éviter les obstacles (parois, autres véhicules).
- Optimiser les trajectoires pour gagner du temps.

Des bonus peuvent être ajoutés à la fin des Sprints, tels que :

- Le départ automatisé du module.
- Le contrôle du module via une application Android Bluetooth.
- L'ajout d'une webcam pour la visualisation de la course.

## Matériel disponible

- Raspberry Pi 3 Modèle B
- Batterie PiJuice
- Alimentation AC/DC 2.4A
- 4 batteries 18650 (5800mAh chacune)
- Chargeur pour batteries 18650
- Carte µSD (vierge - nécessite l'installation de l'OS Raspbian)
- Module SunFounder (Smart Video Car Kit)

## Fonctionnalités principales

1. **Optimisation des trajectoires** : Le robot doit ajuster ses trajectoires pour gagner du temps.
2. **Détection d'obstacles** : Grâce aux capteurs à ultra-sons et infrarouge, le robot doit éviter les obstacles en temps réel.
3. **Affichage de la vitesse et de l'état** : L'interface doit afficher des informations en temps réel telles que la vitesse et l'état des capteurs.
4. **Arrêt automatique sur la ligne d'arrivée** : La voiture doit reconnaître et s'arrêter précisément à la ligne d'arrivée.
5. **Manœuvrabilité** : Le robot doit être capable de faire un demi-tour dans une zone étroite.

## User Stories

Les fonctionnalités du projet sont détaillées par les **user stories** suivantes :

- **Pilote** : Optimiser les trajectoires, détecter et éviter les obstacles, afficher la vitesse et l'état du module, s'arrêter sur la ligne d'arrivée.
- **Directeur de course** : Définir le nombre de tours, démarrer automatiquement les voitures au signal de départ, relancer un module à distance en cas de panne.
- **Spectateur** : Suivre la course en direct, voir le classement et les temps.
- **Mécanicien** : Tester tous les capteurs et moteurs avant chaque course, accéder aux logs et diagnostics.
- **Superviseur technique (PO)** : Assurer la connexion SSH/Wi-Fi, réaliser des tests unitaires sur les capteurs et moteurs, documenter les choix technologiques.

## Méthodologie de développement

Le projet suit la méthode **Scrum** pour la gestion des sprints. Chaque sprint dure **1 jour et demi** avec des réunions régulières :

- **Sprint Planning** : 60 min.
- **Daily Scrum** : 5 min.
- **Sprint Review** : 10 min pour présenter les fonctionnalités terminées.
- **Sprint Retrospective** : 15 min.
