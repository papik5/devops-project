#!/bin/bash
# setup-ec2.sh
# Ejecutar en la instancia EC2 después de conectarte por SSH
# Instala Docker, Docker Compose, y clona el proyecto

set -euo pipefail

echo "=== Configurando instancia EC2 para DevOps Project ==="

# 1. Actualizar sistema
sudo apt-get update -y
sudo apt-get upgrade -y

# 2. Instalar Docker
echo "Instalando Docker..."
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3. Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# 4. Habilitar Docker al inicio
sudo systemctl enable docker
sudo systemctl start docker

# 5. Clonar proyecto
echo "Clonando repositorio..."
cd ~
git clone https://github.com/TU_USUARIO/devops-project.git
cd devops-project

# 6. Crear archivo .env
cat > .env << 'EOF'
ENVIRONMENT=production
APP_VERSION=1.0.0
DOCKER_IMAGE=tu-usuario/devops-demo-app
DB_NAME=devopsdb
DB_USER=devopsuser
DB_PASSWORD=CambiaEstoAhora123!
EOF

echo ""
echo "=== Instalación completa ==="
echo "Docker version: $(docker --version)"
echo "Docker Compose version: $(docker compose version)"
echo ""
echo "Próximo paso: ejecuta 'docker compose up -d'"
