"""Migration de la base : crée les tables qui n'existent pas encore.

Lancé UNE fois par déploiement, avant l'API, et non plus à chaque démarrage de l'API :
    python -m app.migrate

Pourquoi un script séparé ?
  - l'API démarre même si la base n'est pas encore prête (la readiness /ready s'en occupe) :
    plus de crash au démarrage ;
  - avec 2 réplicas (ou plus), les pods ne lancent pas tous la même migration en même temps ;
  - dans Kubernetes, c'est un Job (voir k8s/app/30-api.yaml) : s'il échoue, le déploiement
    s'arrête avant de lancer une API qui ne trouverait pas ses tables.

create_all est idempotent : relancé sur une base déjà à jour, il ne fait rien.
(Limite : il crée les tables manquantes mais ne modifie pas une table existante.
Pour faire évoluer un schéma, on utiliserait un outil comme Alembic.)
"""

from . import models  # noqa: F401  (importer les modèles les enregistre dans Base.metadata)
from .db import Base, engine


def migrate():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    migrate()
    print("Migration terminée : tables à jour.")
