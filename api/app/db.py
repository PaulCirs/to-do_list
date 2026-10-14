import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# L'adresse de la base vient d'une variable d'environnement.
# En local : SQLite (un simple fichier). Avec Docker/Kubernetes : PostgreSQL.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """Ouvre une session de base de données par requête, puis la ferme."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
