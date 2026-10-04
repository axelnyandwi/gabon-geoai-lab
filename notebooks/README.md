# Expérimentations

Ce dossier accueillera les notebooks d’exploration et d’expérimentation.

- Utiliser des noms descriptifs précédés d’un numéro, par exemple `01_exploration_sources.ipynb`.
- Documenter les sources, les paramètres et l’ordre d’exécution.
- Utiliser l’environnement Python du projet (3.12 de référence ; 3.10.11 compatible pour ce notebook) ; ajouter les outils de notebooks lorsque la première expérience les nécessite.
- Réutiliser le code de `src/` et y transférer les traitements devenus stables.
- Retirer les sorties volumineuses et les informations sensibles avant de versionner un notebook.

## Première exploration

`01_sentinel2_discovery.ipynb` interroge les métadonnées publiques Sentinel-2 L2A du catalogue STAC Copernicus autour de Libreville, sans authentification ni téléchargement d’image.

Installer les dépendances avec `python -m pip install -r requirements-dev.txt`, sélectionner le noyau `.venv` Python 3.10.11 ou 3.12 dans VS Code, puis exécuter les cellules dans l’ordre. Les extensions VS Code Python et Jupyter permettent d’ouvrir et d’exécuter le notebook.

`requests` est déclaré explicitement pour les appels HTTP et `ipykernel` fournit le noyau d’exécution. Les paramètres de zone, de période et de seuil nuageux sont modifiables dans le notebook. Aucun jeu de données n’est fourni.
