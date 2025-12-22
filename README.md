# 📚 Comparateur de Prix de Livres - Web Scraping Project

Ce projet est un comparateur de prix de livres automatisé. Il utilise **Python** et le framework **Scrapy** pour extraire des données de plusieurs librairies en ligne (Decitre, Eyrolles, Mollat, etc.), les nettoie et les stocke dans une base de données **MySQL**.

L'ensemble de l'architecture est conteneurisé avec **Docker** pour un déploiement facile et reproductible.

## 🚀 Fonctionnalités

* **Extraction de données (Scraping) :** Récupération automatique du titre, du prix et du lien des livres.
* **Multi-sites :** Architecture capable de gérer plusieurs sites web via des "Spiders" dédiés (ex: `produits_decitre.py`, `eyrolles.py`).
* **Nettoyage de données (Pipeline) :** Conversion des prix (chaînes de caractères vers flottants), suppression des symboles devises, etc.
* **Stockage Persistant :** Sauvegarde automatique dans une base de données MySQL.
* **Interface d'administration :** Visualisation des données via PhpMyAdmin.
* **Infrastructure Docker :** Lancement de la BDD, du Scraper et de l'interface Admin en une seule commande.

## 🛠️ Technologies utilisées

* **Langage :** Python 3.9+
* **Framework de Scraping :** Scrapy
* **Base de données :** MySQL 5.7
* **Connecteur :** mysql-connector-python
* **Administration BDD :** PhpMyAdmin
* **Conteneurisation :** Docker & Docker Compose

## 📂 Structure du Projet

```text
.
├── docker-compose.yml      # Orchestration des conteneurs (DB, Scraper, Admin)
├── db/
│   ├── Dockerfile          # Configuration de l'image MySQL
│   └── creation.sql        # Script d'initialisation de la table 'Livre'
├── scraper/
│   ├── Dockerfile          # Configuration de l'image Python/Scrapy
│   ├── requirements.txt    # Dépendances Python
│   ├── scrapy.cfg          # Config globale Scrapy
│   └── comparateur/        # Code source du Scrapy
│       ├── items.py        # Définition de la structure des données
│       ├── pipelines.py    # Traitement et insertion SQL
│       ├── settings.py     # Réglages du robot (User-Agent, délais...)
│       └── spiders/        # Les robots (un fichier par site)
│           ├── produits_decitre.py
│           ├── produits_eyrolles.py
│           └── produits_mollat.py

```

## 📋 Prérequis

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé sur votre machine.
* Git (pour cloner le projet).

## ⚙️ Installation et Lancement

1. **Cloner le dépôt :**
```bash
git clone [https://github.com/FaridaSintondji/webscraping.git](https://github.com/FaridaSintondji/webscraping.git)
cd webscraping

```


2. **Lancer l'application :**
Cette commande construit les images et lance les conteneurs en arrière-plan.
```bash
docker compose up --build -d

```


3. **Vérifier le fonctionnement :**
Le scraper se lance automatiquement au démarrage. Vous pouvez suivre sa progression avec :
```bash
docker compose logs -f scraper

```


4. **Voir les données (PhpMyAdmin) :**
Ouvrez votre navigateur et allez sur :
👉 **http://localhost:8081**
* **Serveur :** db
* **Utilisateur :** toto
* **Mot de passe :** toto
* **Base de données :** Produits -> Table `Livre`



## 🛑 Commandes Utiles

* **Arrêter les conteneurs :**
```bash
docker compose down

```


* **Réinitialiser la base de données (Grand nettoyage) :**
Si vous avez modifié la structure de la table ou si vous voulez effacer toutes les données pour repartir de zéro :
```bash
docker compose down -v  # Le -v supprime le volume de données
docker compose up --build -d

```


* **Relancer uniquement le scraper (sans éteindre la BDD) :**
```bash
docker compose restart scraper

```



## 📝 Schéma de la Base de Données

La table `Livre` est structurée comme suit :

| Colonne | Type | Description |
| --- | --- | --- |
| id | INT (PK) | Identifiant unique (Auto-inc) |
| titre | TEXT | Titre du livre |
| prix | FLOAT | Prix du livre (ex: 19.50) |
| url | TEXT | Lien vers la page produit |
| site | VARCHAR(50) | Source (ex: "Decitre", "Eyrolles") |

## 👥 Auteurs

Ce projet a été réalisé dans le cadre du cours de Web Scraping & NoSQL.

* **Farida SINTONDJI**
* **Aïda DIARRASSOUBA**
* **Yomn GERALDO ASSANI**

---

*Dernière mise à jour : Décembre 2025*

```


C'est du très bon travail d'être arrivée jusqu'au bout de ce projet avec Docker et Scrapy ! 👏

```
