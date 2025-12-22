# MicroLearn - Réalisé par: Rim EL ABBASSI, Brahim EL MAJDAOUI, Badr ICAME, Taha NACIRI

MicroLearn est une plateforme **AutoML modulaire** basée sur des microservices.  
Elle permet de **préparer des données**, **sélectionner des modèles**, **entraîner**, **évaluer**, **optimiser** et **déployer** des modèles de Machine Learning via des API REST.  
Un **Dashboard** permet de suivre les métriques et comparer les expériences.

---

## 🎯 Objectifs

- Créer des **pipelines AutoML composables** via API ou fichiers YAML.
- Permettre des **entraînements parallèles** et le suivi des expériences.
- Être **réplicable** et **documenté**, prêt pour une évaluation académique ou SoftwareX.
- Respecter la traçabilité et la reproductibilité (FAIR ML).

---

## ⚙️ Microservices

| Microservice      | Port  | Fonction |
|------------------|-------|----------|
| DataPreparer      | 8001  | Nettoyage et prétraitement des données |
| ModelSelector     | 8002  | Sélection automatique des modèles ML |
| Trainer           | 8003  | Entraînement des modèles choisis |
| Evaluator         | 8004  | Évaluation des métriques (accuracy, F1…) |
| HyperOpt          | 8005  | Optimisation des hyperparamètres |
| Deployer          | 8006  | Déploiement des modèles via REST |
| Orchestrator      | 8000  | Coordination des pipelines |
| Dashboard         | 3000  | Interface utilisateur pour suivre les expériences |

---

## 🛠️ Technologies utilisées

### Backend
- Python 3.9+
- FastAPI
- PyTorch / Scikit-learn
- Ray (entraînements parallèles)
- Optuna (Hyperparameter Optimization)

### Frontend
- React
- Chart.js / D3.js

### Infrastructure
- Docker & Docker Compose
- PostgreSQL
- Redis
- MinIO (artefacts & modèles)

---

## 🏗️ Prérequis

Avant de lancer le projet, assure-toi d’avoir :

- **Docker Desktop**
- **Docker Compose**
- **Python 3.9+**
- **Node.js 18+** (pour le dashboard)
- **Git**

---


```bash
docker-compose up --build
