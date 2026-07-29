# USS-PetLycans

Projet Django pour une application fictive de gestion de missions spatiales.

## Objectif du projet

Mettre en place une base Django avec Django REST Framework et une authentification JWT pour une future application de gestion de vaisseaux et de missions spatiales.

## Point realise pour l'instant

Le projet couvre actuellement la partie **Initialisation et Configuration** :

- creation d'un environnement virtuel Python
- installation de `django`
- installation de `djangorestframework`
- installation de `djangorestframework-simplejwt`
- initialisation du projet Django `uss_petlycans`
- creation de l'application `space_agency`
- configuration de `REST Framework`
- configuration de l'authentification JWT par defaut

## Structure actuelle

```text
USS-PetLycans/
├── .venv/
├── manage.py
├── space_agency/
└── uss_petlycans/
```

## Commandes utilisees

### 1. Creation et activation du venv

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installation des dependances

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

### 3. Initialisation du projet Django

```bash
django-admin startproject uss_petlycans .
```

### 4. Creation de l'application Django

```bash
python manage.py startapp space_agency
```

## Configuration dans settings.py

Dans `uss_petlycans/settings.py`, les applications suivantes ont ete ajoutees :

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "space_agency",
]
```

Configuration de REST Framework pour JWT :

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}
```

## Verification

Pour verifier que la configuration Django est correcte :

```bash
python manage.py check
```

## Lancement du projet

```bash
source .venv/bin/activate
python manage.py runserver
```

Puis ouvrir :

```text
http://127.0.0.1:8000/
```

## Etat actuel

Le projet est pret pour commencer la suite :

- creation des modeles
- migrations
- administration Django
- serializers
- vues API et HTML
