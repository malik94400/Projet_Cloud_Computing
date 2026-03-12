# Projet Cloud Computing - Déploiement d'une infrastructure Azure avec Terraform

## Description
Ce projet a pour objectif de déployer et automatiser une infrastructure cloud sur Microsoft Azure avec Terraform.

Le projet comprend :
- un backend Flask
- une base de données SQLite
- un stockage Azure Blob Storage
- une infrastructure Azure automatisée avec Terraform

L’application permet :
- de gérer des fichiers avec un CRUD simple
- d’uploader des fichiers dans Azure Blob Storage
- de stocker les métadonnées des fichiers dans une base SQLite

---

## Technologies utilisées
- Python 3
- Flask
- Flask-SQLAlchemy
- Azure Blob Storage
- Terraform
- Azure CLI
- SQLite

---

## Structure du projet

```text
Projet_Cloud_Computing/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env
│   └── instance/
│       └── files.db
├── terraform/
│   ├── provider.tf
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   └── .terraform.lock.hcl
├── .gitignore
└── README.md
```


# Backend Flask

## Installation
Se placer dans le dossier backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
---

## Configuration .env
Créer un fichier .env dans le dossier backend avec :
```env
AZURE_STORAGE_ACCOUNT=malikblob2026efr
AZURE_STORAGE_KEY=VOTRE_CLE_AZURE
AZURE_CONTAINER_NAME=files
```

---

## Lancement de l’application
```bash
python3 app.py
```

Le serveur Flask sera accessible à l’adresse http://localhost:5001

---

# Endpoints API

## Accueil
- GET /

## Lire tous les fichiers
- GET /files

## Ajouter un fichier en base de données 
- POST /files 

Exemple de payload JSON :
```json
{
    "filename": "example.txt"
}
```

## Modifier un fichier en base de données
- PUT /files/<id>

Exemple de payload JSON :
```json
{
    "filename": "updated_file.txt"
}
```

## Supprimer un fichier en base de données
- DELETE /files/<id>

## Uploader un fichier dans Azure Blob Storage
- POST /upload

## Lister les blobs dans Azure Blob Storage
- GET /blobs

---

# Terraform
Terraform est utilisé pour automatiser la création de l’infrastructure Azure.
Il permet de créer et détruire les ressources cloud de manière reproductible.

## Installation
```bash
cd terraform
terraform init
```

## Voir les pland d'exécution
```bash
terraform plan
``` 

## Créer les ressources Azure
```bash
terraform apply
```

## Détruire les ressources Azure
```bash
terraform destroy
``` 

---

# Ressources créées
- Un groupe de ressources Azure
- Un compte de stockage Azure Blob Storage
- Un conteneur dans Azure Blob Storage

---

# Tests réalisés
- test du backend Flask local
- test des endpoints CRUD avec curl
- test de l’upload d’un fichier avec /upload
- test de lecture des blobs avec /blobs
- test de création d’infrastructure avec terraform apply
- test de suppression d’infrastructure avec terraform destroy
