# 🚀 Qdrant GCP VM Deployment Guide
gcloud compute addresses list
## ✅ 1. One-Time Setup

### 🔐 Authenticate & Set Project
"gcloud auth login"  
"gcloud config set project serene-craft-464519-j1"

### 🌐 Reserve Static IP
"gcloud compute addresses create qdrant-static-ip --region=asia-southeast1"

### 🖥️ Create VM with Docker-Ready Image
"gcloud compute instances create qdrant-vm --zone=asia-southeast1-a --image-family=debian-11 --image-project=debian-cloud --boot-disk-size=10GB --tags=qdrant"

### 🌍 Assign Static IP to VM
"gcloud compute instances add-access-config qdrant-vm --zone=asia-southeast1-a --address=ip_static_url"

### 🔓 Open Firewall for Port 6333
"gcloud compute firewall-rules create allow-qdrant --allow=tcp:6333 --target-tags=qdrant --description='Allow Qdrant access' --direction=INGRESS --priority=1000 --network=default"

---

## ✅ 2. Inside the VM – First Time

### 🔗 SSH into VM
"gcloud compute ssh qdrant-vm --zone=asia-southeast1-a"
gcloud compute instances stop qdrant-vm --zone=asia-southeast1-a
gcloud compute instances start qdrant-vm --zone=asia-southeast1-a

### 🐳 Install Docker and Configure Permissions
"sudo apt update && sudo apt install docker.io -y"  
"sudo usermod -aG docker $USER"  
"exit"

### 🔁 Reconnect via SSH
"gcloud compute ssh qdrant-vm --zone=asia-southeast1-a"

### 🚀 Run Qdrant with Persistent Restart Policy
"docker run -d --restart unless-stopped -p 6333:6333 -v /home/$USER/qdrant_data:/qdrant/storage qdrant/qdrant"

---

## ✅ 3. Every Time You Reboot VM

### 🔗 SSH again:
"gcloud compute ssh qdrant-vm --zone=asia-southeast1-a"

### 🔎 Check Qdrant is running:
"docker ps"

### 🔁 If needed, restart Qdrant:
"docker run -d --restart unless-stopped -p 6333:6333 -v /home/$USER/qdrant_data:/qdrant/storage qdrant/qdrant"

---

## ✅ 4. Health Check

### Inside VM:
"curl http://localhost:6333"

### From local machine:
"curl PATH_uri"

### Or browser:
PATH_uri

Expected output:
```json
{"status":"ok"}
```
## Auto script sh
gcloud compute scp "path to file.sh" qdrant-vm:/home/Admin/restart_qdrant.sh
gcloud compute ssh qdrant-vm --zone=asia-southeast1-a
bash ~/restart_qdrant.sh

# Neo4j GCP VM Deployment Guide
### Common syntax
gcloud compute scp "path/to/restart_neo4j.sh" neo4j-vm:/home/Admin/restart_neo4j.sh --zone=asia-southeast1-a
gcloud compute instances start neo4j-vm --zone=asia-southeast1-a
gcloud compute ssh neo4j-vm --zone=asia-southeast1-a 
bash ~/restart_neo4j.sh
gcloud compute instances stop neo4j-vm --zone=asia-southeast1-a

gcloud compute firewall-rules create allow-neo4j `
  --allow="tcp:7474,tcp:7687" `
  --target-tags=neo4j `
  --description="Allow Neo4j Browser and Bolt access" `
  --direction=INGRESS `
  --priority=1000 `
  --network=default

gcloud compute instances add-tags neo4j-vm `
  --tags=neo4j `
  --zone=asia-southeast1-a


### From local machine:
"curl PATH_uri"

### Or browser:
PATH_uri


# MLflow GCP VM Deployment Guide
gcloud compute ssh mlflow-vm --zone=asia-southeast1-a
gcloud compute scp "path to restart_mlflow.sh" mlflow-vm:/home/Admin/restart_mlflow.sh --zone=asia-southeast1-a

bash ~/restart_mlflow.sh
gcloud compute scp "C:\Users\Admin\Data\MultimodalRag_Web_app\scripts\deploy\gcp_cloudbuild\restart_mlflow.sh" mlflow-vm:/home/Admin/restart_mlflow.sh --zone=asia-southeast1-a


gcloud compute ssh langfuse-vm --zone=asia-southeast1-a 
 gcloud compute scp "C:\Users\Admin\Data\MultimodalRag_Web_app\scripts\deploy\gcp_cloudbuild\restart_langfuse.sh" langfuse-vm:/home/Admin/restart_langfuse.sh --zone=asia-southeast1-a