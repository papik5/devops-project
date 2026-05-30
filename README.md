# DevOps Demo Project

Infraestructura moderna en la nube con CI/CD, contenedores y orquestación.

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Cloud | AWS EC2 (Free Tier) |
| Contenedores | Docker + Docker Compose |
| Orquestación | Docker Swarm |
| CI/CD | GitHub Actions |
| App | Python Flask |
| Proxy / LB | Nginx |
| Base de datos | PostgreSQL |
| Control de versiones | GitHub |

## Arquitectura

```
Internet
   │
   ▼
[EC2 Instance - AWS]
   │
[Nginx :80] ──── Load Balancer / Reverse Proxy
   │
[Flask App :5000] ──── Aplicación containerizada
   │
[PostgreSQL :5432] ──── Base de datos
```

## CI/CD Pipeline

```
Git Push → GitHub Actions
              │
              ├── [CI] Checkout → Install deps → Tests → Build Docker → Test container
              │
              └── [CD] Push DockerHub → SSH a EC2 → docker compose down/up → Health check
```

## Estructura del Repositorio

```
devops-project/
├── app/
│   ├── app.py              # Aplicación Flask
│   ├── requirements.txt    # Dependencias Python
│   └── Dockerfile          # Imagen Docker (multi-stage)
├── nginx/
│   └── nginx.conf          # Configuración Nginx
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # Pipeline GitHub Actions
├── docker-compose.yml      # Stack local y producción
├── swarm-stack.yml         # Docker Swarm (orquestación)
├── deploy.sh               # Script de despliegue
├── setup-ec2.sh            # Configuración inicial EC2
├── .env.example            # Variables de entorno (plantilla)
└── README.md
```

## Despliegue Local (Desarrollo)

```bash
# 1. Clonar repositorio
git clone https://github.com/TU_USUARIO/devops-project.git
cd devops-project

# 2. Configurar variables
cp .env.example .env
# Editar .env con tus valores

# 3. Levantar servicios
docker compose up -d

# 4. Verificar
curl http://localhost/health
# Abrir http://localhost en el navegador
```

## Despliegue en AWS EC2

### Prerrequisitos
- Cuenta AWS Free Tier
- Instancia EC2 t2.micro con Ubuntu 22.04
- Par de claves SSH
- Puerto 80 y 22 abiertos en Security Group

```bash
# En tu máquina local
ssh -i tu-clave.pem ubuntu@TU_IP_EC2

# En la instancia EC2
wget https://raw.githubusercontent.com/TU_USUARIO/devops-project/main/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh
```

## Secrets de GitHub Actions requeridos

| Secret | Descripción |
|---|---|
| `DOCKERHUB_USERNAME` | Tu usuario de DockerHub |
| `DOCKERHUB_TOKEN` | Token de acceso DockerHub |
| `EC2_HOST` | IP pública de tu instancia EC2 |
| `EC2_SSH_KEY` | Contenido de tu archivo .pem |

## Endpoints

| Endpoint | Descripción |
|---|---|
| `GET /` | Página principal con info del sistema |
| `GET /health` | Health check (retorna JSON) |
| `GET /api/info` | Información detallada (JSON) |

## Comandos Útiles

```bash
# Ver logs
docker compose logs -f app

# Ver estado de contenedores
docker compose ps

# Reiniciar solo la app
docker compose restart app

# Docker Swarm - inicializar
docker swarm init
docker stack deploy -c swarm-stack.yml devops

# Ver servicios en Swarm
docker service ls
docker service ps devops_app
```
