# Readwise Light

Une version allégée de Readwise permettant aux utilisateurs de télécharger des documents et de recevoir des résumés et extractions de mots-clés automatiques.

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Structure du projet](#-structure-du-projet)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Documentation API](#-documentation-api)
- [Déploiement](#-déploiement)
- [Développement](#-développement)
- [Dépannage](#-dépannage)

## ✨ Fonctionnalités

- **Upload de fichiers** : Support des formats `.txt`, `.rtf`, `.docx`, `.odt`, `.md`
- **Extraction de texte** : Traitement automatique de différents formats de documents
- **Résumé automatique** : Génération de résumés via LLM (Large Language Model)
- **Extraction de mots-clés** : Identification automatique des termes importants
- **Recherche** : Recherche par mots-clés dans le contenu et les métadonnées
- **Téléchargement** : Accès aux fichiers originaux
- **Interface moderne** : Interface utilisateur responsive avec TailwindCSS

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│    Frontend     │◄──►│     Backend     │◄──►│    Database     │
│   (React/Vite)  │    │   (FastAPI)     │    │   (AlloyDB)     │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
   Port 5173               Port 8000               Port 5432
```

### Composants principaux

- **Frontend** : Application React avec Vite pour le développement rapide
- **Backend** : API REST FastAPI avec intégration LLM
- **Base de données** : AlloyDB (compatible PostgreSQL) pour le stockage des documents
- **Docker** : Containerisation pour un déploiement simplifié

## 📁 Structure du projet

```
readwise_light/
├── 📄 README.md                    # Documentation principale
├── 📄 docker-compose.yml           # Configuration Docker Compose
├── 📄 Dockerfile.backend           # Image Docker backend
├── 📄 Dockerfile.frontend          # Image Docker frontend
├── 📄 .gitignore                   # Fichiers ignorés par Git
│
├── 📁 backend/                     # Application backend
│   ├── 📄 requirements.txt         # Dépendances Python
│   ├── 📁 app/                     # Code source backend
│   │   ├── 📄 main.py              # Point d'entrée FastAPI
│   │   ├── 📄 models.py            # Modèles de données SQLModel
│   │   ├── 📄 crud.py              # Opérations base de données
│   │   ├── 📄 db.py                # Configuration base de données
│   │   ├── 📄 text_extractor.py    # Extraction de texte
│   │   └── 📄 llm.py               # Intégration LLM
│   └── 📁 uploads/                 # Stockage des fichiers uploadés
│       └── 📄 README.md
│
└── 📁 frontend/                    # Application frontend
    ├── 📄 package.json             # Dépendances Node.js
    ├── 📄 vite.config.js           # Configuration Vite
    ├── 📄 tailwind.config.js       # Configuration TailwindCSS
    ├── 📄 postcss.config.js        # Configuration PostCSS
    ├── 📄 eslint.config.js         # Configuration ESLint
    ├── 📄 index.html               # Template HTML principal
    ├── 📁 src/                     # Code source frontend
    │   ├── 📄 main.jsx             # Point d'entrée React
    │   ├── 📄 App.jsx              # Composant principal
    │   ├── 📄 App.css              # Styles spécifiques
    │   ├── 📄 index.css            # Styles globaux
    │   └── 📁 assets/              # Ressources statiques
    └── 📁 public/                  # Fichiers publics
        └── 📄 vite.svg
```

## 🔧 Prérequis

### Pour le développement local
- **Python** 3.8+ avec pip
- **Node.js** 16+ avec npm
- **PostgreSQL** 13+ (ou Docker pour AlloyDB)

### Pour le déploiement Docker
- **Docker** 20.10+
- **Docker Compose** 2.0+

## 🚀 Installation

### Option 1 : Développement local

1. **Cloner le repository**
   ```bash
   git clone <repository-url>
   cd readwise_light
   ```

2. **Configuration de l'environnement**
   ```bash
   cp .env.sample .env
   # Éditer le fichier .env avec vos configurations
   ```

3. **Installation du backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Installation du frontend**
   ```bash
   cd frontend
   npm install
   ```

5. **Démarrage des services**
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

### Option 2 : Docker (Recommandé)

1. **Cloner et configurer**
   ```bash
   git clone <repository-url>
   cd readwise_light
   cp .env.sample .env
   # Éditer le fichier .env
   ```

2. **Démarrer avec Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Accéder à l'application**
   - Frontend : http://localhost:5173
   - Backend API : http://localhost:8000
   - Documentation API : http://localhost:8000/docs

## ⚙️ Configuration

### Variables d'environnement (.env)

```bash
# Base de données
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=readwise

# LLM Configuration
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-3.5-turbo

# Application
DEBUG=true
UPLOAD_MAX_SIZE=10485760  # 10MB en bytes
```

### Configuration de la base de données

Le projet utilise AlloyDB (compatible PostgreSQL). La base de données est automatiquement initialisée au démarrage.

## 📖 Utilisation

### Interface utilisateur

1. **Upload de documents**
   - Cliquez sur "Choisir un fichier"
   - Sélectionnez un document (.txt, .rtf, .docx, .odt, .md)
   - Cliquez sur "Upload"

2. **Visualisation des documents**
   - Les documents apparaissent avec leur résumé
   - Les mots-clés sont affichés sous forme de badges
   - Cliquez sur "Download" pour télécharger le fichier original

3. **Recherche**
   - Utilisez la barre de recherche pour trouver des documents
   - La recherche porte sur le contenu et les mots-clés

## 📚 Documentation API

### Endpoints principaux

#### `GET /health`
Vérification de l'état du service
```bash
curl http://localhost:8000/health
```
**Réponse :**
```json
{"status": "ok"}
```

#### `POST /upload/`
Upload et traitement d'un document
```bash
curl -X POST "http://localhost:8000/upload/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@document.txt"
```
**Réponse :**
```json
{
  "id": 1,
  "filename": "document.txt",
  "content": "Contenu du document...",
  "summary": "Résumé généré...",
  "keywords": "[\"mot-clé1\", \"mot-clé2\"]"
}
```

#### `GET /documents/`
Liste tous les documents
```bash
curl http://localhost:8000/documents/
```

#### `GET /documents/{doc_id}`
Récupère un document spécifique
```bash
curl http://localhost:8000/documents/1
```

#### `GET /download/{doc_id}`
Télécharge le fichier original
```bash
curl http://localhost:8000/download/1 -o document.txt
```

#### `GET /search/?query={query}`
Recherche dans les documents
```bash
curl "http://localhost:8000/search/?query=mot-clé"
```

### Documentation interactive

Accédez à la documentation Swagger à l'adresse : http://localhost:8000/docs

## 🐳 Déploiement

### Docker Compose (Production)

1. **Préparer l'environnement**
   ```bash
   cp .env.sample .env.prod
   # Configurer les variables pour la production
   ```

2. **Déployer**
   ```bash
   docker-compose -f docker-compose.yml --env-file .env.prod up -d
   ```

### Services individuels

```bash
# Backend seulement
docker build -f Dockerfile.backend -t readwise-backend .
docker run -p 8000:8000 readwise-backend

# Frontend seulement
docker build -f Dockerfile.frontend -t readwise-frontend .
docker run -p 5173:5173 readwise-frontend
```

## 👨‍💻 Développement

### Structure du code

#### Backend (FastAPI)
- **main.py** : Configuration FastAPI et routes principales
- **models.py** : Modèles de données avec SQLModel
- **crud.py** : Opérations CRUD pour la base de données
- **text_extractor.py** : Extraction de texte des différents formats
- **llm.py** : Intégration avec les services LLM

#### Frontend (React)
- **App.jsx** : Composant principal avec logique métier
- **main.jsx** : Point d'entrée React
- Configuration Vite pour le développement rapide

### Ajout de nouvelles fonctionnalités

1. **Nouveau format de fichier**
   - Modifier `text_extractor.py`
   - Ajouter la dépendance dans `requirements.txt`

2. **Nouveau endpoint API**
   - Ajouter la route dans `main.py`
   - Créer les fonctions CRUD si nécessaire

3. **Nouvelle fonctionnalité frontend**
   - Modifier `App.jsx`
   - Ajouter les styles TailwindCSS

### Tests

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm test
```

## 🔧 Dépannage

### Problèmes courants

#### Erreur de connexion à la base de données
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Solution :**
- Vérifier que PostgreSQL/AlloyDB est démarré
- Contrôler les variables d'environnement DB_*
- Attendre que le service de base de données soit prêt

#### Erreur LLM
```
Error parsing LLM response
```
**Solution :**
- Vérifier la clé API OpenAI dans .env
- Contrôler la connectivité internet
- Vérifier les quotas API

#### Erreur d'upload de fichier
```
HTTPException: 400 - Unsupported file format
```
**Solution :**
- Vérifier que le format de fichier est supporté
- Contrôler la taille du fichier (limite : 10MB par défaut)

#### Port déjà utilisé
```
Error: Port 8000 is already in use
```
**Solution :**
```bash
# Trouver le processus utilisant le port
lsof -i :8000
# Arrêter le processus ou changer le port dans docker-compose.yml
```

### Logs et debugging

```bash
# Logs Docker Compose
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend

# Mode debug backend
DEBUG=true uvicorn app.main:app --reload
```

### Support

Pour toute question ou problème :
1. Vérifier cette documentation
2. Consulter les logs d'erreur
3. Créer une issue sur le repository

---

## 🛠️ Tech Stack détaillé

### Backend
- **FastAPI** : Framework web moderne et rapide
- **SQLModel** : ORM moderne basé sur Pydantic et SQLAlchemy
- **Uvicorn** : Serveur ASGI haute performance
- **OpenAI** : Intégration LLM pour résumés et mots-clés
- **python-docx, odfpy, striprtf** : Extraction de texte multi-format

### Frontend
- **React 19** : Bibliothèque UI moderne
- **Vite** : Build tool rapide pour le développement
- **TailwindCSS** : Framework CSS utility-first
- **Axios** : Client HTTP pour les appels API

### Base de données
- **AlloyDB** : Base de données PostgreSQL-compatible de Google Cloud
- **Alembic** : Migrations de base de données

### DevOps
- **Docker & Docker Compose** : Containerisation et orchestration
- **ESLint** : Linting JavaScript/React
- **PostCSS & Autoprefixer** : Traitement CSS
