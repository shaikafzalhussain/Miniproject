# 🚀 End-to-End DevOps Project — Flask App CI/CD Pipeline

This project demonstrates a **complete DevOps lifecycle** for a Python Flask web application — from **infrastructure provisioning** to **automated deployment** using **Terraform, Jenkins, SonarQube, Docker, and AWS EC2**.  

---

## 🧠 Project Overview

The main goal of this project was to build a **fully automated CI/CD pipeline** that:
- Builds and tests the code automatically using Jenkins  
- Analyzes code quality with SonarQube  
- Builds and pushes Docker images to DockerHub  
- Deploys the container automatically on an EC2 instance  

This entire setup runs **end-to-end from GitHub → Jenkins → SonarQube → DockerHub → AWS**.

---

## ⚙️ Tools and Technologies Used

| Category | Tool/Service | Purpose |
|-----------|---------------|----------|
| **Infrastructure as Code** | Terraform | Provision AWS EC2 instance automatically |
| **Configuration & Automation** | Bash (Shell scripting) | Install & configure DevOps tools (Jenkins, Docker, SonarQube) |
| **CI/CD Orchestration** | Jenkins | Automate build, test, and deploy |
| **Code Quality** | SonarQube | Static code analysis |
| **Containerization** | Docker | Build & run the Flask application |
| **Registry** | DockerHub | Store and manage Docker images |
| **Hosting** | AWS EC2 | Host Jenkins, SonarQube, and deployed container |
| **Application** | Python Flask | Web application backend |

---

## 🧩 Project Architecture

GitHub → Jenkins → SonarQube → DockerHub → AWS EC2

markdown
Copy code

### Pipeline Flow:
1. **GitHub:** Source code & Jenkinsfile stored here  
2. **Jenkins:** Clones repo, triggers SonarQube scan  
3. **SonarQube:** Performs code quality analysis  
4. **Docker:** Builds and tags the app image  
5. **DockerHub:** Pushes the image to your registry  
6. **AWS EC2:** Runs the container automatically  

---

## 📁 Project Structure

<img width="524" height="420" alt="tree1" src="https://github.com/user-attachments/assets/3c92a3dd-85d7-4682-b18e-d20ef186123d" />

yaml
Copy code

---

## 🧰 Setup Instructions

### 1️⃣ Infrastructure Setup (Terraform)
```bash
terraform init
terraform plan
terraform apply -auto-approve
This will create the EC2 instance and networking setup.

2️⃣ Connect to EC2
bash
Copy code
ssh -i your-key.pem ec2-user@<EC2-Public-IP>
3️⃣ Run the Bash Setup Script
bash
Copy code
sudo chmod +x install_devops_tools.sh
sudo ./install_devops_tools.sh
This script installs and configures Jenkins, Docker, and SonarQube automatically.

4️⃣ Configure Jenkins
Add your GitHub repo URL in Jenkins

Create credentials for:

DockerHub username & password

SonarQube token

Install required Jenkins plugins:

Git

Docker

SonarQube Scanner

Pipeline

5️⃣ Run Jenkins Pipeline
Once triggered, Jenkins will:

Clone the repo

Analyze code in SonarQube

Build Docker image

Push to DockerHub

Deploy container on EC2

🌐 Access Points
Service	URL Example
Jenkins	http://<EC2-IP>:8080
SonarQube	http://<EC2-IP>:9000
Flask App (Deployed)	http://<EC2-IP>:5000 or :5001

🧾 Jenkinsfile (Pipeline Summary)
The Jenkins pipeline automates:

Code checkout from GitHub

SonarQube analysis

Docker image build & push

Automatic container deployment

📦 Dockerfile
A lightweight production-ready Dockerfile using Gunicorn:

dockerfile
Copy code
FROM python:3.9-slim
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "2"]
💡 Learning Highlights
✅ Automated CI/CD pipeline
✅ Infrastructure as Code with Terraform
✅ Code analysis with SonarQube
✅ Containerization & deployment automation
✅ Real-time DevOps workflow on AWS

📎 Repository
👉 GitHub: shaikafzalhussain/Miniproject
✨ “It’s just a beginning, still there is more.”
<img width="1435" height="776" alt="webpage" src="https://github.com/user-attachments/assets/fad7ed79-78f5-451f-989a-444d358b53f4" />
<img width="1427" height="777" alt="sonarqube1" src="https://github.com/user-attachments/assets/a0c06020-de56-4d09-a60c-b5a487d2a3df" />
<img width="1436" height="765" alt="dockerhub" src="https://github.com/user-attachments/assets/e5c1809c-2563-4203-a659-828ad5e3ab61" />


🏷️ Tags
#DevOps #Terraform #Jenkins #SonarQube #Docker #AWS #CICD #Flask #Python #Automation #Bash #CloudComputing

