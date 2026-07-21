# 1. Creazione della cassaforte (Key Vault) 
az keyvault create --name "ai-kv-001" --resource-group "ai-workshop-rg" --location "westeurope" 

# 2. Creazione del primo segreto 
az keyvault secret set --vault-name "ai-kv-001" --name "DBPassword" --value "SuperP@ssword2026!"
