# Next.js Kubernetes Deploy - Reference

Complete reference for deploying production-grade Next.js applications to Kubernetes.

## Configuration Options

### CLI Arguments Summary

| Script              | Argument         | Type    | Default          | Description                       |
|---------------------|------------------|---------|------------------|-----------------------------------|
| `generate_pages.py` | `--project-dir`  | string  | `./frontend-app` | Project root directory            |
| `generate_pages.py` | `--pages`        | string  | `dashboard`      | Comma-separated page names        |
| `generate_pages.py` | `--with-monaco`  | flag    | false            | Include Monaco editor component   |
| `generate_pages.py` | `--api-base-url` | string  | `/api`           | API base URL for generated pages  |
| `generate_pages.py` | `--layout`       | string  | `sidebar`        | Layout type: sidebar, topnav, minimal |
| `verify.py`         | `--namespace`    | string  | `frontend`       | Kubernetes namespace              |
| `verify.py`         | `--release`      | string  | `frontend-app`   | Deployment/release name           |
| `verify.py`         | `--port`         | int     | `30080`          | NodePort to verify                |
| `verify.py`         | `--api-url`      | string  | (empty)          | Backend API URL to verify         |
| `verify.py`         | `--timeout`      | int     | `120`            | Verification timeout in seconds   |
| `verify.py`         | `--verbose`      | flag    | false            | Enable detailed output            |

### Environment Variables

| Variable              | Default                    | Used By           | Description                         |
|-----------------------|----------------------------|--------------------|-------------------------------------|
| `PROJECT_NAME`        | `frontend-app`             | init, build        | Project directory name              |
| `PROJECT_DIR`         | `./${PROJECT_NAME}`        | all scripts        | Project root path                   |
| `NODE_ENV`            | `production`               | build, docker      | Node environment                    |
| `NEXT_PUBLIC_API_URL` | `/api`                     | build, deploy      | Public API base URL                 |
| `NAMESPACE`           | `frontend`                 | deploy, verify     | Kubernetes namespace                |
| `RELEASE_NAME`        | `frontend-app`             | deploy, verify     | Deployment name                     |
| `IMAGE_NAME`          | `frontend-app`             | docker, deploy     | Docker image name                   |
| `IMAGE_TAG`           | `latest`                   | docker, deploy     | Docker image tag                    |
| `REGISTRY`            | (empty)                    | docker, deploy     | Container registry prefix           |
| `PLATFORM`            | `linux/amd64`              | docker             | Docker target platform              |
| `REPLICAS`            | `2`                        | deploy             | Pod replica count                   |
| `API_BACKEND_URL`     | `http://api-svc:8000`      | deploy             | Backend service URL in cluster      |
| `PORT`                | `3000`                     | deploy             | Container port                      |
| `NODE_PORT`           | `30080`                    | deploy             | External NodePort                   |
| `CPU_REQUEST`         | `100m`                     | deploy             | CPU request per pod                 |
| `CPU_LIMIT`           | `500m`                     | deploy             | CPU limit per pod                   |
| `MEM_REQUEST`         | `128Mi`                    | deploy             | Memory request per pod              |
| `MEM_LIMIT`           | `512Mi`                    | deploy             | Memory limit per pod                |
| `MAX_RETRIES`         | `3`                        | deploy             | Retry attempts for deployment       |
| `RETRY_BACKOFF`       | `15`                       | deploy             | Seconds between retries             |
| `ANALYZE_BUNDLE`      | `0`                        | build              | Enable webpack bundle analyzer      |
| `DEBUG`               | `0`                        | all                | Enable debug output                 |
| `LOG_FILE`            | `.nextjs-k8s-deploy.log`   | all                | Log file path                       |

## Component Architecture

### Error Boundary

```
ErrorBoundary (class component)
├── Props
│   ├── children: ReactNode
│   ├── fallback?: ReactNode | (error, reset) => ReactNode
│   ├── onError?: (error, errorInfo) => void
│   └── onReset?: () => void
├── State
│   ├── hasError: boolean
│   ├── error: Error | null
│   └── errorInfo: ErrorInfo | null
└── Methods
    ├── getDerivedStateFromError(error) → state
    ├── componentDidCatch(error, errorInfo) → log
    └── resetErrorBoundary() → clear state, call onReset
```

**Default Fallback UI:**
- Error icon with message
- "Try Again" button that calls `resetErrorBoundary()`
- Collapsible stack trace in development mode
- Error details logged to console and optional external service

### Loading Skeleton

```
LoadingSkeleton
├── Variants
│   ├── text: Horizontal bars with varying widths
│   ├── card: Rectangle with header and body placeholders
│   ├── table: Grid of rectangular cells
│   ├── avatar: Circle with text lines
│   └── editor: Code-like lines with syntax coloring hints
├── Props
│   ├── variant: 'text' | 'card' | 'table' | 'avatar' | 'editor'
│   ├── lines?: number (for text variant)
│   ├── count?: number (for repeating)
│   └── className?: string
└── Animation
    └── CSS pulse animation (opacity 0.4 → 1.0, 1.5s)
```

### Monaco Editor Component

```
MonacoEditorWrapper (dynamic import, SSR-disabled)
├── Props
│   ├── value: string
│   ├── language: string ('javascript' | 'typescript' | 'json' | 'python' | 'yaml' | 'sql')
│   ├── theme?: 'vs-dark' | 'vs-light' | 'hc-black'
│   ├── height?: string | number
│   ├── readOnly?: boolean
│   ├── onChange?: (value: string) => void
│   ├── onMount?: (editor, monaco) => void
│   ├── options?: IStandaloneEditorConstructionOptions
│   └── loading?: ReactNode
├── Features
│   ├── Auto-resize to container
│   ├── Keyboard shortcuts (Ctrl+S → save callback)
│   ├── Minimap toggle
│   ├── Word wrap toggle
│   └── Language auto-detection from file extension
└── SSR Safety
    ├── dynamic(() => import(...), { ssr: false })
    └── Fallback to <textarea> if Monaco fails to load
```

### Responsive Layout

```
ResponsiveLayout
├── Breakpoints
│   ├── sm: 640px   (mobile)
│   ├── md: 768px   (tablet)
│   ├── lg: 1024px  (desktop)
│   └── xl: 1280px  (wide desktop)
├── Layout Modes
│   ├── sidebar: Collapsible left sidebar (280px) + main content
│   ├── topnav: Fixed top navbar (64px) + main content
│   └── minimal: Full-width content only
├── Props
│   ├── children: ReactNode
│   ├── sidebar?: ReactNode
│   ├── navbar?: ReactNode
│   ├── footer?: ReactNode
│   ├── mode?: 'sidebar' | 'topnav' | 'minimal'
│   └── sidebarCollapsed?: boolean
└── Responsive Behavior
    ├── < 768px: Sidebar becomes overlay drawer
    ├── 768-1024px: Sidebar collapsed to icons
    └── > 1024px: Full sidebar visible
```

### API Client

```
ApiClient (singleton)
├── Configuration
│   ├── baseURL: string (from NEXT_PUBLIC_API_URL)
│   ├── timeout: number (30000ms)
│   ├── retries: number (3)
│   ├── retryDelay: number (1000ms, exponential backoff)
│   └── headers: Record<string, string>
├── Methods
│   ├── get<T>(path, params?) → Promise<T>
│   ├── post<T>(path, body?) → Promise<T>
│   ├── put<T>(path, body?) → Promise<T>
│   ├── patch<T>(path, body?) → Promise<T>
│   ├── delete<T>(path) → Promise<T>
│   └── upload<T>(path, formData) → Promise<T>
├── Interceptors
│   ├── Request: Add auth token, content-type
│   ├── Response: Parse JSON, extract data
│   └── Error: Map status codes to error types
├── Error Types
│   ├── NetworkError: No response received
│   ├── TimeoutError: Request exceeded timeout
│   ├── AuthError: 401/403 responses
│   ├── ValidationError: 422 with field errors
│   ├── NotFoundError: 404 responses
│   └── ServerError: 500+ responses
└── Retry Logic
    ├── Retries on: NetworkError, TimeoutError, 502, 503, 504
    ├── No retry on: 400, 401, 403, 404, 422
    └── Backoff: delay * 2^attempt (1s, 2s, 4s)
```

### Toast Notification System

```
ToastProvider (Context + Portal)
├── Toast Types
│   ├── success: Green accent, check icon
│   ├── error: Red accent, X icon
│   ├── warning: Yellow accent, alert icon
│   └── info: Blue accent, info icon
├── Props (ToastProvider)
│   ├── children: ReactNode
│   ├── position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
│   ├── maxToasts?: number (default: 5)
│   └── defaultDuration?: number (default: 5000ms)
├── Hook: useToast()
│   ├── toast.success(message, options?)
│   ├── toast.error(message, options?)
│   ├── toast.warning(message, options?)
│   ├── toast.info(message, options?)
│   └── toast.dismiss(id?)
└── Features
    ├── Auto-dismiss with configurable duration
    ├── Manual dismiss with X button
    ├── Stacking with slide-in animation
    ├── Pause auto-dismiss on hover
    └── ARIA live region for accessibility
```

## Docker Build Strategy

### Multi-Stage Build

```dockerfile
# Stage 1: Dependencies (cached layer)
FROM node:18-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build (cached if source unchanged)
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: Production (minimal image)
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

**Image Size Targets:**
- Dependencies stage: ~300MB (cached)
- Builder stage: ~500MB (discarded)
- Production image: ~120-180MB

### Build Optimizations

| Optimization             | Config Location          | Effect                          |
|--------------------------|--------------------------|---------------------------------|
| Standalone output        | `next.config.js`         | Reduces image by ~60%           |
| Image optimization       | `next.config.js`         | WebP/AVIF auto-conversion       |
| SWC minification         | Built-in (Next.js 13+)   | Faster than Terser              |
| Tree shaking             | Built-in                 | Dead code elimination           |
| Code splitting           | Built-in                 | Per-route bundles               |
| CSS modules              | Built-in                 | Scoped CSS, no conflicts        |
| Font optimization        | `next/font`              | Self-hosted, no layout shift    |
| Bundle analysis          | `ANALYZE_BUNDLE=1`       | Visualize bundle composition    |

## Kubernetes Deployment Architecture

### Resources Created

```
Namespace: frontend
├── Deployment: frontend-app
│   ├── replicas: 2
│   ├── strategy: RollingUpdate (maxSurge: 1, maxUnavailable: 0)
│   ├── Pod
│   │   ├── Container: nextjs
│   │   │   ├── image: frontend-app:latest
│   │   │   ├── port: 3000
│   │   │   ├── resources: 100m-500m CPU, 128Mi-512Mi RAM
│   │   │   ├── livenessProbe: /api/health (period: 30s)
│   │   │   ├── readinessProbe: /api/health (period: 10s)
│   │   │   ├── startupProbe: /api/health (period: 5s, failureThreshold: 30)
│   │   │   └── env:
│   │   │       ├── NEXT_PUBLIC_API_URL
│   │   │       ├── API_BACKEND_URL
│   │   │       └── NODE_ENV=production
│   │   └── securityContext:
│   │       ├── runAsNonRoot: true
│   │       ├── runAsUser: 1001
│   │       └── readOnlyRootFilesystem: true
│   └── labels:
│       ├── app: frontend-app
│       └── version: latest
├── Service: frontend-app-svc
│   ├── type: NodePort
│   ├── port: 80 → targetPort: 3000
│   └── nodePort: 30080
├── ConfigMap: frontend-app-config
│   ├── NEXT_PUBLIC_API_URL
│   └── NODE_ENV
└── HorizontalPodAutoscaler (optional)
    ├── minReplicas: 2
    ├── maxReplicas: 10
    ├── targetCPUUtilization: 70%
    └── targetMemoryUtilization: 80%
```

### Health Check Endpoint

The deployment creates a `/api/health` endpoint:

```typescript
// app/api/health/route.ts
export async function GET() {
  return Response.json({
    status: "healthy",
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || "unknown",
    uptime: process.uptime(),
  });
}
```

### Rolling Update Strategy

- **maxSurge: 1** - At most 1 extra pod during update
- **maxUnavailable: 0** - All existing pods stay until new pod is ready
- **minReadySeconds: 5** - Pod must be ready for 5s before considered available
- **progressDeadlineSeconds: 300** - Deployment fails if no progress in 5 min

## Performance Optimization Reference

### Next.js Config Recommendations

```javascript
// next.config.js
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60,
  },
  experimental: {
    optimizeCss: true,
  },
  headers: async () => [
    {
      source: '/:path*',
      headers: [
        { key: 'X-Frame-Options', value: 'DENY' },
        { key: 'X-Content-Type-Options', value: 'nosniff' },
        { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      ],
    },
    {
      source: '/_next/static/:path*',
      headers: [
        { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
      ],
    },
  ],
};
```

### Bundle Size Targets

| Category            | Target   | Warning Threshold |
|---------------------|----------|-------------------|
| First Load JS       | < 100KB  | > 150KB           |
| Per-page JS         | < 50KB   | > 80KB            |
| Monaco Editor chunk | < 2MB    | > 3MB             |
| Total CSS           | < 30KB   | > 50KB            |
| Largest asset       | < 500KB  | > 1MB             |

### Dynamic Import Patterns

```typescript
// Heavy components - load on demand
const MonacoEditor = dynamic(() => import('@/components/MonacoEditor'), {
  ssr: false,
  loading: () => <LoadingSkeleton variant="editor" />,
});

// Route-level code splitting (automatic with App Router)
// Each page in app/ directory is a separate chunk

// Conditional feature loading
const AdminPanel = dynamic(() => import('@/components/AdminPanel'), {
  ssr: false,
});
```

## API Connection Patterns

### Server-Side API Calls (Route Handlers)

```typescript
// app/api/proxy/[...path]/route.ts
// Proxies frontend requests to backend API within the cluster
const API_BACKEND = process.env.API_BACKEND_URL || 'http://api-svc:8000';

export async function GET(request: Request, { params }: { params: { path: string[] } }) {
  const path = params.path.join('/');
  const url = new URL(request.url);

  const response = await fetch(`${API_BACKEND}/${path}${url.search}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(request.headers.get('Authorization')
        ? { Authorization: request.headers.get('Authorization')! }
        : {}),
    },
    next: { revalidate: 0 }, // No caching for API proxy
  });

  return Response.json(await response.json(), { status: response.status });
}
```

### Client-Side API Calls (React Hooks)

```typescript
// hooks/useApi.ts
function useApi<T>(path: string, options?: { enabled?: boolean; refetchInterval?: number }) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<ApiError | null>(null);
  const [loading, setLoading] = useState(true);
  // ... fetch logic with retry, caching, error mapping
}
```

## Troubleshooting

### Build Issues

| Problem                        | Cause                            | Solution                                        |
|--------------------------------|----------------------------------|-------------------------------------------------|
| `Module not found: @monaco-editor` | Missing dependency            | Run `npm install @monaco-editor/react`          |
| Build OOM error                | Large codebase + analyzer        | Increase Node memory: `NODE_OPTIONS=--max-old-space-size=4096` |
| CSS module conflicts           | Duplicate class names            | Use unique module file names                    |
| `window is not defined`        | SSR rendering client code        | Use `dynamic(() => ..., { ssr: false })`        |
| Slow builds                    | No caching                       | Enable `next.config.js` cache, use Docker layer caching |

### Deployment Issues

| Problem                        | Cause                            | Solution                                        |
|--------------------------------|----------------------------------|-------------------------------------------------|
| Pod CrashLoopBackOff           | Missing env vars or OOM          | Check logs: `kubectl logs -n frontend <pod>`    |
| ImagePullBackOff               | Image not found in registry      | Verify image exists: `docker images`            |
| Health check failing           | App not listening on PORT        | Verify `PORT` env var matches container port    |
| 502 Bad Gateway                | Pod not ready                    | Wait for readiness probe or check startup probe |
| API connection refused         | Wrong backend URL                | Verify `API_BACKEND_URL` resolves within cluster |
| CORS errors                    | Missing CORS headers on backend  | Add CORS middleware to backend API              |

### Performance Issues

| Problem                        | Cause                            | Solution                                        |
|--------------------------------|----------------------------------|-------------------------------------------------|
| Large first load               | Heavy dependencies               | Use dynamic imports, check bundle analysis      |
| Slow page transitions          | No prefetching                   | Use `<Link prefetch>` for navigation links      |
| Layout shift (CLS)             | Unoptimized images/fonts         | Use `next/image` and `next/font`                |
| Monaco editor lag              | Loading full editor upfront      | Lazy load with `dynamic`, use `loading` prop    |

## Log Format

All scripts log to `.nextjs-k8s-deploy.log`:

```
[2024-01-15T10:30:00Z] [INFO] Starting Next.js project initialization
[2024-01-15T10:30:01Z] [INFO] Creating project directory: ./frontend-app
[2024-01-15T10:30:15Z] [INFO] npm install completed (14s)
[2024-01-15T10:30:15Z] [DEBUG] Installed 847 packages
[2024-01-15T10:31:45Z] [INFO] Next.js build completed (90s)
[2024-01-15T10:31:45Z] [INFO] Bundle size: First Load JS 87.2KB
[2024-01-15T10:32:10Z] [INFO] Docker build completed (25s, 142MB)
[2024-01-15T10:32:30Z] [INFO] Deployed to namespace frontend (2 replicas)
[2024-01-15T10:33:00Z] [INFO] Health check passed: http://localhost:30080
```

## Security Headers

The deployment automatically configures these security headers:

| Header                    | Value                                      |
|---------------------------|-------------------------------------------|
| X-Frame-Options           | DENY                                      |
| X-Content-Type-Options    | nosniff                                   |
| Referrer-Policy           | strict-origin-when-cross-origin           |
| X-DNS-Prefetch-Control    | on                                        |
| Strict-Transport-Security | max-age=31536000; includeSubDomains       |
| Permissions-Policy        | camera=(), microphone=(), geolocation=()  |

## Integration with Other Skills

### With fastapi-dapr-agent

Set `API_BACKEND_URL` to the FastAPI service:

```bash
API_BACKEND_URL="http://fastapi-svc.default.svc.cluster.local:8000" \
  bash scripts/deploy_k8s.sh
```

### With kafka-k8s-setup

For real-time data, the frontend can use Server-Sent Events (SSE) from a backend that consumes Kafka topics:

```bash
# Backend exposes /api/stream endpoint
NEXT_PUBLIC_API_URL="http://localhost:30080/api" \
  bash scripts/build_frontend.sh
```

### With postgres-k8s-setup

Frontend connects through the API layer. No direct database connection from Next.js:

```
Browser → Next.js (port 30080) → API Proxy → FastAPI (port 8000) → PostgreSQL (port 5432)
```
