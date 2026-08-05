import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# URL del key vault in cloud
vault_url = "https://ai-kv-001.vault.azure.net/"

# Autenticazione sicura (usa l'identità di Azure, senza chiavi!)
credential = DefaultAzureCredential()
client = SecretClient(vault_url, credential)

# Recupero dinamico a runtime
db_secret = client.get_secret("DBPassword")

db_password = db_secret.value

# LOG non conformativo per la sicurezza, ma utile per il debug
print("Connessione stabilita con successo! Chiave segreta recuperata:", db_password)

