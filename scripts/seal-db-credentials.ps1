# Génère un nouveau mot de passe Postgres aléatoire et le chiffre avec kubeseal.
# Affiche le bloc "encryptedData" à coller dans k8s/charts/todo/values.yaml (db.credentials).
#
#   .\scripts\seal-db-credentials.ps1
#
# Le mot de passe en clair n'est jamais affiché ni écrit sur le disque : il n'existe que
# chiffré (dans Git) et déchiffré dans le cluster (Secret créé par le contrôleur).
# Pour le lire dans le cluster si besoin :
#   kubectl get secret db-credentials-v2 -n todo -o jsonpath="{.data.POSTGRES_PASSWORD}"  (base64)
#
# Prérequis : kubectl pointé sur le cluster, et le contrôleur Sealed Secrets installé
# (k8s/argocd/sealed-secrets.yaml) : kubeseal lui demande sa clé publique.
#
# À relancer si le cluster est recréé (nouvelle clé → les anciens SealedSecrets ne se
# déchiffrent plus). Changer le mot de passe d'une base EXISTANTE demande aussi un
# "ALTER USER" dans Postgres : la variable POSTGRES_PASSWORD ne sert qu'à la création de la base.
param(
    [string]$Namespace = "todo",
    [string]$SecretName = "db-credentials-v2",   # doit correspondre à db.credentials.secretName
    [string]$User = "todo",
    [string]$Database = "todo"
)
$ErrorActionPreference = "Stop"

# 32 caractères tirés au hasard par un générateur cryptographique. Lettres et chiffres
# seulement : le mot de passe est aussi placé dans une URL (DATABASE_URL), où des caractères
# comme @ : / devraient être échappés.
$alphabet = [char[]]"abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
$password = -join ($bytes | ForEach-Object { $alphabet[$_ % $alphabet.Length] })

# 1. kubectl fabrique le Secret en local (--dry-run=client : rien n'est envoyé au cluster)
$secret = kubectl create secret generic $SecretName --namespace $Namespace `
    --from-literal=POSTGRES_PASSWORD=$password `
    --from-literal=DATABASE_URL="postgresql+psycopg://${User}:${password}@db:5432/$Database" `
    --dry-run=client -o json

# 2. kubeseal le chiffre avec la clé publique du cluster. Le chiffrement est lié au nom et
#    au namespace du Secret : copié sous un autre nom, il ne se déchiffrerait pas.
$sealed = ($secret | kubeseal --format json) | Out-String | ConvertFrom-Json

# 3. Affiche le bloc à coller dans values.yaml
"    encryptedData:"
foreach ($key in $sealed.spec.encryptedData.PSObject.Properties) {
    "      $($key.Name): $($key.Value)"
}
