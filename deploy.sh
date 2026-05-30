#!/bin/bash
# deploy.sh – Script de despliegue en EC2
# Uso: ./deploy.sh [version]

set -euo pipefail

VERSION=${1:-latest}
IMAGE="${DOCKER_IMAGE:-tu-usuario/devops-demo-app}"
PROJECT_DIR="$HOME/devops-project"

echo "======================================"
echo "  DevOps Deploy Script"
echo "  Version: $VERSION"
echo "  $(date)"
echo "======================================"

# Pull imagen nueva
echo "[1/4] Pulling Docker image..."
docker pull "$IMAGE:$VERSION"

# Ir al directorio del proyecto
cd "$PROJECT_DIR"

# Actualizar variable de versión
export APP_VERSION="$VERSION"
export DOCKER_IMAGE="$IMAGE"

# Bajar servicios actuales
echo "[2/4] Stopping current services..."
docker compose down --remove-orphans

# Levantar servicios nuevos
echo "[3/4] Starting new services..."
docker compose up -d

# Esperar a que levanten
echo "[4/4] Waiting for health check..."
sleep 10

# Verificar salud
if curl -sf http://localhost/health > /dev/null; then
    echo ""
    echo "✓ Deploy exitoso – versión $VERSION corriendo"
    docker compose ps
else
    echo ""
    echo "✗ Health check falló – haciendo rollback..."
    docker compose logs app
    exit 1
fi
