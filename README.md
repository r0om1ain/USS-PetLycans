# USS-PetLycans

Projet Django pour une application fictive de gestion de missions spatiales (vaisseaux et missions).

## Objectif

Mettre en place une API REST avec Django REST Framework et une authentification JWT, ainsi que des vues HTML pour consulter les données.

## Fonctionnalités actuelles

- modèles `Vaisseau` et `Mission` (relation ForeignKey)
- administration Django
- serializers avec validation (mission programmée : date de lancement non passée)
- API REST CRUD (`/api/vaisseaux/`, `/api/missions/`)
- filtre des missions par statut (`?statut=Programmée`)
- authentification JWT (`/token/`, `/token/refresh/`)
- permissions : lecture publique, écriture authentifiée
- vues HTML : accueil, tableau des missions, tableau des vaisseaux
- fichiers de requêtes HTTP pour tester l'API

## Prérequis

- Python 3
- environnement virtuel recommandé

## Installation

```bash
python -m venv .venv
```

Activation :

```bash
# Linux / macOS
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Installation des dépendances :

```bash
pip install -r requirements.txt
```

Migrations et serveur :

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Puis ouvrir [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Structure du projet

```text
USS-PetLycans/
├── http-request/          # Requêtes HTTP de test (REST Client)
│   ├── .env.example
│   └── space-agency.http
├── space_agency/
│   ├── admin.py
│   ├── api_urls.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── migrations/
│   └── templates/
├── uss_petlycans/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

## Modèles

### Vaisseau

| Champ     | Type              | Détail                                      |
|-----------|-------------------|---------------------------------------------|
| `nom`     | CharField         | max 100                                     |
| `type`    | CharField         | Exploration, Cargo, Transport, Combat       |
| `capacite`| PositiveIntegerField |                                          |

### Mission

| Champ            | Type        | Détail                                              |
|------------------|-------------|-----------------------------------------------------|
| `destination`    | CharField   | max 100                                             |
| `date_lancement` | DateField   |                                                     |
| `statut`         | CharField   | Programmée, En cours, Terminée, Annulée (défaut : Programmée) |
| `vaisseau`       | ForeignKey  | lien vers `Vaisseau` (`related_name="missions"`)    |

## Routes

| URL                     | Description                          |
|-------------------------|--------------------------------------|
| `/`                     | Page d'accueil HTML                  |
| `/missions/`            | Tableau HTML des missions            |
| `/vaisseaux/`           | Tableau HTML des vaisseaux           |
| `/admin/`               | Interface d'administration           |
| `/api/vaisseaux/`       | API CRUD vaisseaux                   |
| `/api/missions/`        | API CRUD missions                    |
| `/api/missions/?statut=`| Filtre des missions par statut       |
| `/token/`               | Obtenir un JWT (access + refresh)    |
| `/token/refresh/`       | Rafraîchir le token d'accès          |

## Authentification JWT

1. Créer un utilisateur : `python manage.py createsuperuser`
2. Obtenir un token :

```http
POST /token/
Content-Type: application/json

{
  "username": "votre-username",
  "password": "votre-password"
}
```

3. Utiliser le token pour les écritures API :

```http
Authorization: Bearer <access_token>
```

Les lectures (`GET`) sont publiques. Les `POST`, `PUT`, `PATCH` et `DELETE` nécessitent un JWT valide.

## Tests API avec REST Client

Le dossier `http-request/` contient des exemples de requêtes.

1. Copier `http-request/.env.example` vers `http-request/.env`
2. Renseigner `username` et `password`
3. Ouvrir `http-request/space-agency.http` et exécuter les requêtes (extension REST Client dans VS Code / Cursor)

## Vérification

```bash
python manage.py check
```

## Configuration principale

Dans `uss_petlycans/settings.py` :

- apps : `rest_framework`, `rest_framework_simplejwt`, `space_agency`
- authentification JWT par défaut pour DRF
- langue `fr-fr`, fuseau `Europe/Paris`

## Suite possible

- permissions plus fines par rôle
- pagination / filtres avancés sur l'API
- enrichissement des templates HTML
- tests unitaires automatisés
