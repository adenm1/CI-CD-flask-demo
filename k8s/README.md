# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the CI/CD Flask Demo application.

## Prerequisites

- Kubernetes cluster (v1.25+)
- `kubectl` configured to access your cluster
- Container registry with your Docker images
- (Optional) Ingress controller (nginx-ingress)
- (Optional) Cert-manager for SSL certificates

## Quick Start

### 1. Create Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Create Secrets

**IMPORTANT**: Never commit actual secrets to git!

```bash
# Create secrets from command line
kubectl create secret generic backend-secrets \
  --from-literal=SECRET_KEY='your-secret-key' \
  --from-literal=PASSWORD_PEPPER='your-pepper' \
  --from-literal=GITHUB_WEBHOOK_SECRET='your-webhook-secret' \
  --from-literal=POSTGRES_USER='postgres' \
  --from-literal=POSTGRES_PASSWORD='your-postgres-password' \
  --from-literal=DATABASE_URL='postgresql+psycopg2://postgres:password@postgres:5432/learning_env' \
  --namespace=ci-cd-demo

# Or use sealed-secrets or external secrets operator in production
```

### 3. Apply ConfigMap

```bash
kubectl apply -f configmap.yaml
```

### 4. Deploy Database & Cache

```bash
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f redis-deployment.yaml
```

Wait for services to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=postgres --namespace=ci-cd-demo --timeout=300s
kubectl wait --for=condition=ready pod -l app=redis --namespace=ci-cd-demo --timeout=300s
```

### 5. Deploy Backend

```bash
kubectl apply -f backend-deployment.yaml
```

### 6. Configure Ingress (Optional)

Update `ingress.yaml` with your domain:

```bash
# Edit ingress.yaml and replace 'yourdomain.com' with your actual domain
kubectl apply -f ingress.yaml
```

## Deployment Order

1. namespace.yaml
2. secrets (manually created)
3. configmap.yaml
4. postgres-statefulset.yaml
5. redis-deployment.yaml
6. backend-deployment.yaml
7. ingress.yaml (optional)

## Verification

### Check All Resources

```bash
kubectl get all -n ci-cd-demo
```

### Check Pods

```bash
kubectl get pods -n ci-cd-demo
```

### Check Services

```bash
kubectl get svc -n ci-cd-demo
```

### Check HPA Status

```bash
kubectl get hpa -n ci-cd-demo
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n ci-cd-demo

# Postgres logs
kubectl logs -f statefulset/postgres -n ci-cd-demo

# Redis logs
kubectl logs -f deployment/redis -n ci-cd-demo
```

## Health Check

```bash
# Port forward to test locally
kubectl port-forward -n ci-cd-demo svc/backend 8000:8000

# Test health endpoint
curl http://localhost:8000/health
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment backend --replicas=5 -n ci-cd-demo
```

### Auto-scaling

The HPA is configured to scale between 2-10 replicas based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

Monitor auto-scaling:

```bash
kubectl get hpa backend-hpa -n ci-cd-demo --watch
```

## Rolling Updates

```bash
# Update image
kubectl set image deployment/backend backend=your-registry/flask-backend:v2 -n ci-cd-demo

# Check rollout status
kubectl rollout status deployment/backend -n ci-cd-demo

# Rollback if needed
kubectl rollout undo deployment/backend -n ci-cd-demo
```

## Monitoring

### Prometheus & Grafana

Deploy monitoring stack:

```bash
# Using Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n ci-cd-demo

# Access Grafana
kubectl port-forward -n ci-cd-demo svc/prometheus-grafana 3000:80
# Default credentials: admin/prom-operator
```

### Application Metrics

Metrics are exposed at `/metrics` endpoint on the backend service.

## Troubleshooting

### Pod not starting

```bash
kubectl describe pod <pod-name> -n ci-cd-demo
kubectl logs <pod-name> -n ci-cd-demo --previous
```

### Database connection issues

```bash
# Check if database is ready
kubectl exec -it statefulset/postgres -n ci-cd-demo -- psql -U postgres -d learning_env -c "\l"

# Test connectivity from backend
kubectl exec -it deployment/backend -n ci-cd-demo -- curl postgres:5432
```

### Redis connection issues

```bash
# Test Redis
kubectl exec -it deployment/redis -n ci-cd-demo -- redis-cli ping
```

## Production Considerations

### Security

1. **Use Secret Management**: Consider using:
   - Sealed Secrets
   - External Secrets Operator
   - HashiCorp Vault
   - Cloud provider secret managers (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)

2. **Network Policies**: Implement network policies to restrict traffic

3. **Pod Security Standards**: Apply pod security policies/standards

4. **RBAC**: Configure proper role-based access control

### High Availability

1. **Multi-zone deployment**: Spread pods across availability zones
2. **Database replication**: Use PostgreSQL replication or managed database
3. **Redis clustering**: Consider Redis Cluster for HA
4. **Backup strategy**: Implement automated backups for PostgreSQL

### Performance

1. **Resource limits**: Tune resource requests/limits based on load testing
2. **HPA tuning**: Adjust HPA thresholds based on actual metrics
3. **Connection pooling**: Configure database connection pool size
4. **Caching**: Optimize Redis caching strategy

## Cleanup

```bash
# Delete all resources
kubectl delete -f ingress.yaml
kubectl delete -f backend-deployment.yaml
kubectl delete -f redis-deployment.yaml
kubectl delete -f postgres-statefulset.yaml
kubectl delete -f configmap.yaml
kubectl delete secret backend-secrets -n ci-cd-demo
kubectl delete -f namespace.yaml
```

## Next Steps

- Set up CI/CD pipeline for automated deployments
- Configure monitoring and alerting
- Implement backup and disaster recovery
- Set up log aggregation (ELK, Loki, etc.)
- Implement GitOps with ArgoCD or FluxCD
