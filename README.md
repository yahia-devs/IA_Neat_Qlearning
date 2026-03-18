# IA Neat & Q-Learning — Geometry Dash

Projet d'apprentissage par renforcement sur un jeu de type Geometry Dash codé from scratch avec pygame.

Deux approches testées et comparées :
- **NEAT** : algorithme neuro-évolutif via la librairie neat-python
- **Q-Learning** : implémenté from scratch, avec système de récompenses et table Q

## Le jeu

Jeu de type Geometry Dash codé from scratch avec pygame. Un personnage doit éviter des obstacles en sautant. L'IA apprend à jouer toute seule.

## Lancer le projet

```
pip install pygame neat-python numpy
```

Lancer l'IA NEAT :

```
python NEAT/play_ai.py
```

Lancer l'entrainement Q-Learning :

```
python Q_learning/train.py
```

Voir l'IA Q-Learning jouer :

```
python Q_learning/play_ai.py
```

## Structure

```
NEAT/
├── ai.py          entrainement NEAT
├── game.py        le jeu
├── play_ai.py     lancer la meilleure IA
├── window.py      affichage
├── config.txt     configuration du réseau NEAT
├── winner.pkl     meilleur réseau sauvegardé
└── q_table.pkl    table Q sauvegardée

Q_learning/
├── train.py       entrainement Q-Learning from scratch
├── game.py        le jeu
└── play_ai.py     lancer la meilleure IA
```

## Résultats

NEAT converge plus vite mais Q-Learning est entièrement fait main — la logique de récompenses, la table Q, les mises à jour. Plus intéressant à comprendre de l'intérieur.
