# Gabon GeoAI Lab

**Observer · Comprendre · Prédire · Simuler**

Gabon GeoAI Lab est une plateforme expérimentale d’intelligence géospatiale consacrée au Gabon. Le projet est actuellement en phase de recherche et de conception.

Cette première version fournit uniquement une fondation technique et une page d’accueil Streamlit. Aucune fonctionnalité métier n’est encore implémentée.

## Orientations du projet

Les étapes futures pourront couvrir :

- l’exploration territoriale ;
- la visualisation de données géospatiales ;
- l’analyse d’images satellite ;
- la détection des changements ;
- la recherche de similarités géospatiales ;
- la prévision de transformations territoriales ;
- l’expérimentation avec des modèles d’apprentissage automatique et des modèles de fondation GeoAI.

## Installation et démarrage

Python **3.12** est la version de référence. Exécuter les commandes depuis la racine du dépôt.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Sous Windows, créer l’environnement avec `py -3.12 -m venv .venv`, puis l’activer dans PowerShell avec `.venv\Scripts\Activate.ps1`.

L’application est accessible à l’adresse locale affichée par Streamlit, généralement `http://localhost:8501`.

## Configuration

Aucun secret ni service externe n’est nécessaire au démarrage. Les constantes générales et les chemins des données sont définis dans `src/config.py`.

La variable d’environnement optionnelle `GABON_GEOAI_DATA_DIR` permet de choisir un autre dossier de données. Un chemin relatif est résolu depuis la racine du projet. Par défaut, le dossier `data/` est utilisé.

`.env.example` documente cette variable. L’application ne charge pas automatiquement les fichiers `.env`. Définir la variable dans le terminal avant de démarrer Streamlit, par exemple :

```bash
export GABON_GEOAI_DATA_DIR=/chemin/vers/les/donnees
python -m streamlit run app.py
```

Sous PowerShell, utiliser `$env:GABON_GEOAI_DATA_DIR = "C:\chemin\vers\les\donnees"`.

Ne jamais versionner de secrets. Les fichiers `.env` et les secrets Streamlit sont ignorés par Git.

## Structure du dépôt

```text
.
|-- README.md
|-- .gitignore
|-- .env.example
|-- requirements.txt
|-- requirements-dev.txt
|-- app.py
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- data/
|   |   |-- __init__.py
|   |   |-- ingestion.py
|   |   |-- preparation.py
|   |   `-- quality.py
|   |-- geo/__init__.py
|   |-- features/__init__.py
|   |-- models/
|   |   |-- __init__.py
|   |   |-- training.py
|   |   |-- prediction.py
|   |   `-- evaluation.py
|   |-- services/__init__.py
|   `-- components/__init__.py
|-- data/
|   |-- raw/.gitkeep
|   |-- interim/.gitkeep
|   `-- processed/.gitkeep
|-- notebooks/
|   |-- .gitkeep
|   `-- README.md
|-- tests/
|   |-- .gitkeep
|   |-- test_config.py
|   `-- fixtures/.gitkeep
`-- docs/data_sources.md
```

- `app.py` : point d’entrée et page d’accueil Streamlit.
- `src/config.py` : configuration générale et chemins, sans création automatique de dossiers.
- `src/data/` : future acquisition et préparation des données.
- `src/geo/` : futurs traitements géospatiaux.
- `src/features/` : création des variables destinées aux analyses et aux modèles.
- `src/models/` : emplacements distincts pour l’entraînement, la prédiction et l’évaluation, sans logique ML.
- `src/services/` : future orchestration applicative réutilisable par Streamlit ou une API.
- `src/components/` : futurs composants d’interface Streamlit.
- `data/raw/` : données sources conservées sans modification.
- `data/interim/` : résultats intermédiaires des traitements.
- `data/processed/` : données préparées pour les analyses.
- `notebooks/` : expérimentations et exploration.
- `tests/` : tests de configuration et futures données synthétiques de test.
- `docs/data_sources.md` : provenance, licences et limites des futures sources.

Les modules métier contiennent uniquement des descriptions de rôle. Seules la configuration et la page d’accueil minimale sont fonctionnelles. Aucun cadre supplémentaire, conteneur, base de données, service cloud ou chaîne d’intégration continue n’est ajouté.

## Dépendances

Streamlit est la seule dépendance directe de l’application. `requirements-dev.txt` ajoute pytest pour les contrôles de développement. Les bibliothèques géospatiales, d’analyse et d’apprentissage automatique seront ajoutées lorsque les premiers usages les justifieront. La plage de versions dans `requirements.txt` limite les mises à jour à la version majeure 1 ; elle ne constitue pas un verrouillage complet des dépendances transitives.

## Données et expérimentations

Tout le contenu de `data/` est ignoré, à l’exception des fichiers `.gitkeep`. Les principaux formats de données géospatiales, d’archives et de modèles sont également ignorés dans le reste du dépôt. Ne pas forcer leur ajout avec Git sans évaluer leur taille et leur pertinence.

Les notebooks peuvent être versionnés. Retirer leurs sorties volumineuses et toute information sensible avant de les ajouter ; leurs dossiers de sauvegarde automatique sont ignorés.

## Vérifications de la fondation

Après installation, vérifier la cohérence des dépendances et la syntaxe Python :

```bash
python -m pip check
python -m compileall -q app.py src
```

Le démarrage avec `python -m streamlit run app.py` doit afficher le titre, la devise et le message de recherche et de conception. Pour vérifier la configuration, installer les dépendances de développement et exécuter les tests :

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Vérifier également les exclusions et le contenu préparé pour commit :

```bash
git check-ignore .env .venv/exemple data/raw/exemple.csv artifacts/exemple.bin
git status --short
git diff --cached --check
```

La première commande doit afficher les quatre chemins ignorés. `.env.example` et les fichiers `.gitkeep` doivent rester versionnables. `.gitignore` ne bloque pas les fichiers déjà suivis ni les ajouts forcés et ne filtre pas selon la taille : relire la liste des fichiers avant tout commit. Conserver les artefacts dans les dossiers ignorés et ne jamais ajouter de secrets.

Aucun commit n’est nécessaire pour effectuer ces contrôles.
