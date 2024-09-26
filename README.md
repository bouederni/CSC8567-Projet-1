# CSC-8567 - Projet Django & Docker

Ce projet a été réalisé dans le cadre du module d'enseignement "Architectures distribuées et Applications Web" dans le cadre de mon année de 2A - Cycle Ingénieur Informatique & Réseaux par apprentissage à Télécom SudParis.

Il s'agit d'un site Web réalisé sous Django, containerisé à l'aide de Docker. 

Diagramme de classes :
![alt text](/misc/Diagramme de classes.png)

Diagramme du réseau virtuel :
![alt text](/misc/Diagramme de classes.png)

# - Liste des chemins URL
- "`/`" : Page principale
- "`/api`" : API
- "`/admin`" : Interface admin Django

# Questions

## Fonctionnement de Django

### 1. Affichage d'index.html

*Vous disposez d'un projet Django dans lequel une application public a été créée. Décrivez la suite de requêtes et d'exécutions permettant l'affichage d'une page HTML index.html à l'URL global / via une application public, ne nécessitant pas de contexte de données. Vous décrirez la position exacte dans l'arborescence des répertoires des différents fichiers utiles à cette exécution.*

Il suffit d'utiliser `python manage.py runserver`. Les fichiers à modifier dans l'arborescence sont les suivants : 
```
 <project_name>/
         ├── <project_name>/
         │   └── urls.py/
         └── public/
             ├── views.py
             ├── urls.py
             └── templates/
                 └── public/
                     └── index.html
```

- Le fichier `<project_name>/urls.py` :
```
from django.urls import path
from .views import index

urlpatterns = [
    path('', include('public.urls')),
]
```

- Le fichier `public/urls.py` : 
```
from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
]
```

- Un exemple simple pour `public/views.py` :
```
from django.shortcuts import render

def index(request):
    return render(request, 'public/index.html')
```

- **Fonctionnement** : 
    - Le fichier `<project_name>/urls.py` est parcouru en 1er pour reconnaître l'URL `/index.html`. Vu que le seul chemin est le chemin vide (ligne `path('', include('public.urls'))`), c'est lui qui est sélectionné, et le fichier `public/urls.py` est parcouru ensuite.
    - Celui-ci ne possède aussi qu'un seul chemin étant le chemin vide (`path('', index, name='index')`). Le fichier `views.index` est donc parcouru ensuite.
    - Dans le fichier `public/views.py`, la page `public/index.html` est renvoyée pour être affichée. 


### 2. Configuration de la base de données
*Dans quelle(s) section(s) de quel(s) fichier(s) peut-on configurer la base de données que l'on souhaite utiliser pour un projet Django ?*

Cela se fait dans le fichier `<project_name>/settings.py`, et plus spécifiquement dans la section DATABASES. Voici celle de mon projet : 
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "database",
        "USER": "admin",
        "PASSWORD": "admin",
        "HOST": "db",
        "PORT": "5432",
    }
}
```
(oui, pas très safe le login admin/admin... :P)

### Question 3 - Configuration du fichier de paramètres
*Dans quel(s) fichier(s) peut-on configurer le fichier de paramètres que l'on souhaite faire utiliser par le projet Django ? Si plusieurs fichers sont à mentionner, expliquez le rôle de chaque fichier.*

Cette configuration s'effectue dans le fichier `/manage.py`, présent dans le root du projet Django. Dans ce fichier est présente la ligne suivante : 
```
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<project_name>.settings")
```
Cette ligne définit le fichier `<project_name>/settings.py` en tant que fichier de paramétrage du projet Django. 

### Question 4 - Effet des commandes `makemigrations` et `migrate`

*Nous nous plaçons à la racine de votre projet Django. Quel effet a l'exécution `python manage.py makemigrations` ? Et l'exécution `python manage.py migrate` ? Quel(s) fichier(s) sont mis en oeuvre pendant ces exécutions ?*

- `python manage.py makemigrations` Génère des fichiers contenant les instructions pour appliquer les modifications appliquées aux modèles à la base de données existante.
    - Les fichiers concernés sont des dossiers `migrations` créés (ici) dans chaque application, avec des fichiers de migration à l'intérieur.

- `python manage.py migrate` applique les migrations à la base de données. Cette commande crée/modifie/supprime les tables/colonnes en fonction de ce qui a été modifié dans le `models.py` de l'application correspondante.
    - Les fichiers concernés sont les fichiers de migration, ainsi que `settings.py` (là où la base de données est configurée).

## Fonctionnement de Docker

### 1. Effet & syntaxe de certaines commandes

- `FROM` : Indique l'image de base à partir de laquelle construire le conteneur. 
```
FROM <image>[:<tag>]
```
- `RUN` : Exécute des commandes dans le conteneur pendant le processus de construction. 
```
RUN <command>
```
- `WORKDIR` : Définit le répertoire de travail pour les instructions suivantes.
```
WORKDIR <path>
```
- `EXPOSE` : Indique que le conteneur écoute les requêtes sur le port spécifié.
```
EXPOSE <port> [<port>/<protocol>...]
```
- `CMD` : Définit la commande par défaut à exécuter lorsque le conteneur démarre. 
```
CMD ["executable","param1","param2"]
```

### 2. Effet de certaines mentions dans `docker-compose.yml`

- ```
    ports:
        - "80:80"
    ```
    - Associe le port 80 de l'hôte au port 80 du conteneur.
- ```
    build: 
        context: .
        dockerfile: Dockerfile.api
    ```
    - `context: .` définit le contexte de construction (`.` se réfère au chemin du fichier dans lequel `docker-compose.yml` est présent)
    - `dockerfile: Dockerfile.api` spécifie le nom du fichier `Dockerfile` à utiliser par le service contenant ces instructions.
- ```
    depends_on:
        - web
        - api
    ```
    - Définit les dépendences du service concerné. Docker démarre les services en fonction de leur "hiérarchie" de dépendences.
- ```
    environment:
        POSTGRES_DB: ${POSTGRES_DB}
        POSTGRES_USER: ${POSTGRES_USER}
        POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ```
    - Définit les variables d'environnement pour le conteneur. Ici, ces variables spécifient la base de données Postgres utilisée, ainsi que ses identifiants. 

### 3. Méthode pour définir des variables d'environnement dans un conteneur

Cela se fait dans le `docker-compose.yml`, c'est la méthode `environment`, comme mentionné juste au-dessus de cette question.

### 4. Accès à un serveur Web dans un réseau Docker

*Dans un même réseau Docker, nous disposons d'un conteneur `nginx` (utilisant l'image `nginx:latest`) et d'un conteneur `web` (utilisant une image contenant un projet web Django, ayant la commande `python manage.py runserver 0.0.0.0:8000` de lancée au démarrage du conteneur). Comment adresser le serveur web tournant dans le conteneur `web` depuis le conteneur `nginx`, sans utiliser les adresses IP des conteneurs ?*

```
server {
    listen 80;
    location / {
        proxy_pass http://web:8000;  # "web" est le nom du service
    }
}
```



