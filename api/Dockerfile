# Image de base : Python officiel, variante "slim" (plus légère)
FROM python:3.14-slim

# Pas de fichiers .pyc, et logs affichés immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# On copie d'abord uniquement requirements.txt : tant qu'il ne change pas,
# Docker réutilise cette couche en cache et ne réinstalle pas les dépendances.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Puis le code (change souvent → couche reconstruite à chaque modif)
COPY app ./app

# Bonne pratique : ne pas tourner en root dans le conteneur.
# appuser peut écrire dans le dossier /app (pour le fichier SQLite par défaut),
# mais les fichiers de code restent à root : l'appli ne peut pas modifier son propre code.
RUN useradd --create-home appuser && chown appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
