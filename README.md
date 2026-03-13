# Projet Cloud Computing - Déploiement d'une infrastructure Azure avec Terraform

## Description
Ce projet a pour objectif de déployer et automatiser une infrastructure cloud sur Microsoft Azure avec Terraform.

Le projet comprend :
- un backend Flask
- une base de données SQLite
- un stockage Azure Blob Storage
- une infrastructure Azure automatisée avec Terraform
- une machine virtuelle Ubuntu sur Azure
- un déploiement automatique du backend sur la VM

L’application permet :
- de gérer des fichiers avec un CRUD simple
- d’uploader des fichiers dans Azure Blob Storage
- de stocker les métadonnées des fichiers dans une base SQLite
- d’exposer l’API Flask sur une machine virtuelle Azure

---

## Technologies utilisées
- Python 3
- Flask
- Flask-SQLAlchemy
- Azure Blob Storage
- Terraform
- Azure CLI
- SQLite
- systemd
- Ubuntu Server

---

## Structure du projet

```text
Projet_Cloud_Computing/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── terraform/
│   ├── provider.tf
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars.example
│   └── .terraform.lock.hcl
├── scripts/
│   └── bootstrap.sh
├── .gitignore
└── README.md
```

---

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
- Un réseau virtuel Azure
- Un sous réseau
- Une adresse IP publique
- Une interface réseau
- Un groupe de sécurité réseau
- Une machine virtuelle Ubuntu Server
- Un compte de stockage Azure Blob Storage
- Un conteneur dans Azure Blob Storage

---

# Déploiement automatique de la VM
Le déploiement automatique de l’application sur la VM est réalisé grâce au fichier :
- scripts/bootstrap.sh

Ce script est injecté dans la machine virtuelle via Terraform avec custom_data.

Il permet automatiquement de :
- mettre à jour la machine
- installer Python, pip, venv et git
- cloner le dépôt GitHub
- installer les dépendances Python
- créer le fichier .env
- créer un service systemd flaskapp
- démarrer automatiquement l’application Flask

---

# Accès à la VM

Une fois l’infrastructure créée, l’adresse IP publique de la VM peut être récupérée avec :
```bash
terraform output -raw vm_public_ip
```
Connexion SSH :
```bash
ssh -i ~/.ssh/azure_vm_key azureuser@IP_DE_LA_VM
```

---

# Déploiement et test sur la VM
L’application Flask est automatiquement déployée sur la VM et lancée comme service systemd.

Vérifier le service :
```bash
sudo systemctl status flaskapp --no-pager
```

Tester localement sur la VM :
```bash
curl http://127.0.0.1:5001/
```

Tester depuis la machine locale :
```bash
curl http://IP_DE_LA_VM:5001/
curl http://IP_DE_LA_VM:5001/files
curl http://IP_DE_LA_VM:5001/blobs
```

---

# Tests réalisés
- test du backend Flask en local
- test de l’upload d’un fichier avec /upload
- test de lecture des blobs avec /blobs
- test de création d’infrastructure avec terraform apply
- test de suppression d’infrastructure avec terraform destroy
- test de connexion SSH à la VM
- test du déploiement automatique du backend sur la VM
- test d’accès à l’application Flask via l’IP publique de la VM
