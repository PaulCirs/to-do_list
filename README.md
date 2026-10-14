# To-do list — projet d'apprentissage DevOps

Une to-do list volontairement simple, en 3 parties, qui sert de support pour apprendre
Docker, la CI/CD avec GitHub Actions et Kubernetes.

```
navigateur ──► frontend (HTML/JS, servi par nginx) ──► api (FastAPI) ──► base PostgreSQL
```

## Organisation

| Dossier              | Contenu                                              |
|----------------------|------------------------------------------------------|
| `api/`               | API Python (FastAPI + SQLAlchemy) et ses tests       |
| `frontend/`          | Page web statique (HTML, CSS, JavaScript)            |
| `k8s/`               | Manifests Kubernetes (étape 4)                       |
| `.github/workflows/` | Pipelines GitHub Actions (étape 3)                   |

## Lancer en local (étape 1)

En local, l'API utilise SQLite (un simple fichier) : pas besoin de PostgreSQL.

**Terminal 1 — l'API**

```powershell
cd api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

Documentation interactive de l'API : http://localhost:8000/docs

**Terminal 2 — le front**

```powershell
cd frontend
python -m http.server 5500
```

Puis ouvrir http://localhost:5500

**Lancer les tests**

```powershell
cd api
pytest
```

## Feuille de route

- [x] 0. Dépôt GitHub et structure
- [x] 1. Appli fonctionnelle en local
- [ ] 2. Docker : Dockerfiles + docker-compose (avec PostgreSQL)
- [ ] 3. CI : GitHub Actions (tests, build, push sur ghcr.io)
- [ ] 4. Kubernetes local avec kind
- [ ] 5. CD : GitOps avec Argo CD
- [ ] 6. Bonus : Helm, probes, HPA, Job de migration
