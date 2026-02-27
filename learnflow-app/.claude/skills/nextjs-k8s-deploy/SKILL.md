---
name: nextjs-k8s-deploy
description: "Deploy production-grade Next.js frontend to Kubernetes with build optimization, Monaco editor integration, responsive design, error boundaries, and API connection patterns."
version: 1.0.0
allowed-tools:
  - Bash(npm*)
  - Bash(npx*)
  - Bash(node*)
  - Bash(kubectl*)
  - Bash(helm*)
  - Bash(docker*)
  - Bash(python*)
  - Bash(bash*)
  - Bash(curl*)
  - Bash(pip*)
  - Read
  - Write
---

# nextjs_k8s_deploy

Deploy a production-grade Next.js frontend application to Kubernetes with optimized builds, Monaco editor integration, responsive design patterns, error boundaries, loading states, and API connection patterns.

## When to Use

- Deploying a Next.js frontend to a Kubernetes cluster
- Setting up a production-grade React/Next.js application with proper component architecture
- Integrating Monaco editor into a web application
- Building a frontend that connects to backend APIs running in Kubernetes
- Creating responsive, accessible web applications with proper error handling

## Prerequisites

| Tool       | Min Version | Check Command              |
|------------|-------------|----------------------------|
| Node.js    | 18.0.0      | `node --version`           |
| npm        | 9.0.0       | `npm --version`            |
| Docker     | 20.0.0      | `docker --version`         |
| kubectl    | 1.25.0      | `kubectl version --client` |
| Python     | 3.9+        | `python --version`         |
| Kubernetes | 1.25+       | `kubectl cluster-info`     |

## Instructions

### Step 1: Initialize Next.js Project

```bash
bash skills-library/.claude/skills/nextjs-k8s-deploy/scripts/init_nextjs.sh
```

**Environment Variables:**

| Variable       | Default         | Description                     |
|----------------|-----------------|---------------------------------|
| `PROJECT_NAME` | `frontend-app`  | Next.js project directory name  |
| `PROJECT_DIR`  | `./{PROJECT_NAME}` | Target directory             |
| `NODE_ENV`     | `development`   | Node environment                |

### Step 2: Set Up Components

```bash
bash skills-library/.claude/skills/nextjs-k8s-deploy/scripts/setup_components.sh
```

Generates production-grade components:
- Error boundaries with recovery UI
- Loading skeletons and suspense wrappers
- Monaco editor integration component
- Responsive layout system
- API client with retry logic
- Toast notification system

### Step 3: Generate Pages

```bash
python skills-library/.claude/skills/nextjs-k8s-deploy/scripts/generate_pages.py \
  --project-dir ./{PROJECT_NAME} \
  --pages dashboard,settings,editor
```

**Options:**

| Flag             | Default     | Description                        |
|------------------|-------------|------------------------------------|
| `--project-dir`  | `./frontend-app` | Project root directory        |
| `--pages`        | `dashboard` | Comma-separated page names         |
| `--with-monaco`  | (flag)      | Include Monaco editor on pages     |
| `--api-base-url` | `/api`      | Base URL for API connections       |

### Step 4: Build Frontend

```bash
bash skills-library/.claude/skills/nextjs-k8s-deploy/scripts/build_frontend.sh
```

**Environment Variables:**

| Variable              | Default        | Description                        |
|-----------------------|----------------|------------------------------------|
| `PROJECT_DIR`         | `./frontend-app` | Project root directory          |
| `NEXT_PUBLIC_API_URL` | `/api`         | Public API base URL                |
| `ANALYZE_BUNDLE`      | `0`            | Set to `1` to generate bundle analysis |
| `NODE_ENV`            | `production`   | Build environment                  |

### Step 5: Build Docker Image

```bash
bash skills-library/.claude/skills/nextjs-k8s-deploy/scripts/build_docker.sh
```

**Environment Variables:**

| Variable         | Default            | Description                    |
|------------------|--------------------|--------------------------------|
| `PROJECT_DIR`    | `./frontend-app`   | Project root directory         |
| `IMAGE_NAME`     | `frontend-app`     | Docker image name              |
| `IMAGE_TAG`      | `latest`           | Docker image tag               |
| `REGISTRY`       | (empty)            | Container registry prefix      |
| `PLATFORM`       | `linux/amd64`      | Target platform                |

### Step 6: Deploy to Kubernetes

```bash
bash skills-library/.claude/skills/nextjs-k8s-deploy/scripts/deploy_k8s.sh
```

**Environment Variables:**

| Variable         | Default            | Description                    |
|------------------|--------------------|--------------------------------|
| `NAMESPACE`      | `frontend`         | Kubernetes namespace           |
| `RELEASE_NAME`   | `frontend-app`     | Helm release / deployment name |
| `IMAGE_NAME`     | `frontend-app`     | Docker image name              |
| `IMAGE_TAG`      | `latest`           | Docker image tag               |
| `REPLICAS`       | `2`                | Number of pod replicas         |
| `API_BACKEND_URL`| `http://api-svc:8000` | Backend API service URL     |
| `PORT`           | `3000`             | Container port                 |
| `NODE_PORT`      | `30080`            | NodePort for external access   |
| `CPU_REQUEST`    | `100m`             | CPU request per pod            |
| `CPU_LIMIT`      | `500m`             | CPU limit per pod              |
| `MEM_REQUEST`    | `128Mi`            | Memory request per pod         |
| `MEM_LIMIT`      | `512Mi`            | Memory limit per pod           |
| `MAX_RETRIES`    | `3`                | Deployment retry attempts      |
| `RETRY_BACKOFF`  | `15`               | Seconds between retries        |

### Step 7: Verify Deployment

```bash
pip install -r skills-library/.claude/skills/nextjs-k8s-deploy/scripts/requirements.txt
python skills-library/.claude/skills/nextjs-k8s-deploy/scripts/verify.py \
  --namespace frontend \
  --release frontend-app \
  --port 30080
```

**Options:**

| Flag            | Default         | Description                    |
|-----------------|-----------------|--------------------------------|
| `--namespace`   | `frontend`      | Kubernetes namespace           |
| `--release`     | `frontend-app`  | Deployment/release name        |
| `--port`        | `30080`         | NodePort to verify             |
| `--api-url`     | (empty)         | Backend API URL to verify      |
| `--timeout`     | `120`           | Max wait time in seconds       |
| `--verbose`     | (flag)          | Enable verbose output          |

## Component Specifications

| Component        | Pattern               | Key Features                          |
|------------------|-----------------------|---------------------------------------|
| ErrorBoundary    | Class component       | Fallback UI, retry, error reporting   |
| LoadingSkeleton  | Suspense wrapper      | Pulse animation, content-aware shapes |
| MonacoEditor     | Dynamic import        | SSR-safe, theme support, languages    |
| ResponsiveLayout | CSS Grid + Flexbox    | Breakpoints, sidebar collapse, mobile |
| ApiClient        | Fetch + retry         | Interceptors, auth, error mapping     |
| ToastProvider    | Context + portal      | Auto-dismiss, stacking, accessibility |

## Validation Checklist

Before running deployment:

- [ ] Node.js >= 18 installed and accessible
- [ ] npm >= 9 installed and accessible
- [ ] Docker daemon running
- [ ] Kubernetes cluster accessible via kubectl
- [ ] Namespace exists or will be created
- [ ] Container registry accessible (if using remote registry)
- [ ] Backend API URL is reachable from cluster network
- [ ] Sufficient cluster resources for requested CPU/memory

## Success Criteria

```
[OK] Next.js project initialized (frontend-app)
[OK] Components generated (6 components)
[OK] Pages generated (dashboard, settings, editor)
[OK] Frontend build completed (2.1MB bundle)
[OK] Docker image built (frontend-app:latest, 142MB)
[OK] Deployed to Kubernetes (frontend/frontend-app, 2 replicas)
[OK] Health check passed (http://localhost:30080)
[OK] API connectivity verified (http://api-svc:8000/health)
```

## Exit Codes

| Code | Meaning                                      |
|------|----------------------------------------------|
| 0    | Success - deployment complete and verified    |
| 1    | Fatal error - build failure, deploy failure   |
| 2    | Prerequisites not met (retryable)             |
| 3    | Build optimization warning (non-fatal)        |
| 4    | Health check timeout (deployment may be slow) |

## Timing Specifications

| Operation             | Timeout  | Retries | Backoff |
|-----------------------|----------|---------|---------|
| npm install           | 300s     | 2       | 15s     |
| Next.js build         | 600s     | 1       | 30s     |
| Docker build          | 600s     | 2       | 15s     |
| K8s deployment        | 180s     | 3       | 15s     |
| Pod readiness         | 120s     | -       | -       |
| Health check          | 30s      | 5       | 5s      |
| API connectivity      | 15s      | 3       | 5s      |

## Token Efficiency

All heavy operations are handled by external scripts. Final output is a single summary line per step. Use `DEBUG=1` or `--verbose` for detailed output. Logs are written to `.nextjs-k8s-deploy.log` in the project directory.

## Integration Requirements

This skill integrates with:
- **kafka-k8s-setup**: Frontend can consume real-time events via WebSocket bridge
- **postgres-k8s-setup**: Frontend connects to APIs backed by PostgreSQL
- **fastapi-dapr-agent**: Frontend connects to FastAPI microservices as backend API

Set `API_BACKEND_URL` to point to the backend service URL within the cluster (e.g., `http://fastapi-svc.default.svc.cluster.local:8000`).
