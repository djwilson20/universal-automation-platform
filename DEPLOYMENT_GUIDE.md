# Deployment Guide

## Overview

This guide provides instructions for setting up the complete CI/CD pipeline for the Universal AI Automation Platform, including multi-environment deployment to staging and production.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │───▶│     Staging     │───▶│   Production    │
│     (Local)     │    │   (develop)     │    │     (main)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

### GitHub Repository Setup

1. **Repository Secrets** (Settings → Secrets and Variables → Actions):

   ```bash
   # AWS Configuration
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...

   # Container Registry
   GITHUB_TOKEN=ghp_... (automatically provided)

   # Production Load Balancer
   PROD_LISTENER_ARN=arn:aws:elasticloadbalancing:...
   BLUE_TARGET_GROUP_ARN=arn:aws:elasticloadbalancing:...
   GREEN_TARGET_GROUP_ARN=arn:aws:elasticloadbalancing:...

   # Notifications
   SLACK_WEBHOOK=https://hooks.slack.com/services/...
   ```

2. **Environment Protection Rules**:
   - Go to Settings → Environments
   - Create `staging` and `production` environments
   - Add deployment protection rules for production
   - Require reviews for production deployments

### AWS Infrastructure Setup

#### 1. ECS Cluster Creation

```bash
# Create staging cluster
aws ecs create-cluster \
    --cluster-name ai-automation-staging \
    --capacity-providers FARGATE \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1

# Create production cluster
aws ecs create-cluster \
    --cluster-name ai-automation-production \
    --capacity-providers FARGATE \
    --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1
```

#### 2. IAM Roles

```bash
# ECS Task Execution Role
aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://ecs-trust-policy.json

aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# ECS Task Role (for application permissions)
aws iam create-role \
    --role-name ecsTaskRole \
    --assume-role-policy-document file://ecs-trust-policy.json
```

#### 3. CloudWatch Log Groups

```bash
# Create log groups
aws logs create-log-group --log-group-name /ecs/ai-automation-staging
aws logs create-log-group --log-group-name /ecs/ai-automation-production
```

#### 4. Application Load Balancer Setup

```bash
# Create ALB for production (blue-green deployment)
aws elbv2 create-load-balancer \
    --name ai-automation-production \
    --subnets subnet-12345678 subnet-87654321 \
    --security-groups sg-12345678

# Create target groups for blue-green deployment
aws elbv2 create-target-group \
    --name ai-automation-blue \
    --protocol HTTP \
    --port 8501 \
    --vpc-id vpc-12345678 \
    --target-type ip

aws elbv2 create-target-group \
    --name ai-automation-green \
    --protocol HTTP \
    --port 8501 \
    --vpc-id vpc-12345678 \
    --target-type ip
```

## CI/CD Pipeline Workflow

### 1. Continuous Integration (CI)

**Triggers**: Push to any branch, Pull requests to main/develop

**Jobs**:
- **Test**: Run unit tests across Python 3.11-3.13
- **Lint**: Code quality checks (black, isort, flake8, pylint)
- **Security**: Dependency vulnerability scanning
- **Build**: Package creation and verification
- **Integration**: End-to-end workflow testing

### 2. Security Scanning

**Triggers**: Push to main/develop, PRs, Daily scheduled

**Jobs**:
- **CodeQL**: Static analysis for security vulnerabilities
- **Semgrep**: Security pattern matching
- **Bandit**: Python security linting
- **Safety**: Known vulnerability database check
- **Secrets**: Git history scanning for exposed secrets
- **Container**: Docker image vulnerability scanning

### 3. Multi-Environment Deployment

#### Staging Deployment
**Trigger**: Push to `develop` branch

**Process**:
1. Build and push Docker image
2. Update ECS service definition
3. Deploy to staging environment
4. Run health checks and smoke tests
5. Notify team via Slack

#### Production Deployment
**Trigger**: Push to `main` branch or version tags

**Process**:
1. Deploy to green environment
2. Run comprehensive health checks
3. Execute production acceptance tests
4. Switch load balancer traffic to green
5. Monitor metrics for 5 minutes
6. Scale down blue environment
7. Create GitHub release (for tags)

### 4. Release Pipeline

**Trigger**: Version tags (v1.0.0, v1.1.0, etc.)

**Process**:
1. Validate release and run full test suite
2. Build release artifacts (Python packages, Docker images)
3. Security scan release artifacts
4. Create GitHub release with changelog
5. Deploy to production using blue-green strategy
6. Publish documentation

## Environment Configuration

### Development Environment

1. **Local Setup**:
   ```bash
   git clone https://github.com/djwilson20/universal-automation-platform.git
   cd universal-automation-platform

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows

   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt

   # Set up pre-commit hooks
   pre-commit install

   # Copy environment template
   cp .env.example .env
   # Edit .env with your local configuration
   ```

2. **Run locally**:
   ```bash
   streamlit run app.py
   ```

### Staging Environment

- **URL**: https://staging.ai-automation-platform.com
- **Branch**: `develop`
- **Auto-deployment**: Yes
- **Purpose**: Integration testing, stakeholder reviews

**Configuration**:
- Reduced resource allocation (512 CPU, 1GB RAM)
- Debug logging enabled
- Non-production database
- Relaxed security policies for testing

### Production Environment

- **URL**: https://ai-automation-platform.com
- **Branch**: `main`
- **Deployment**: Blue-green with manual approval
- **Purpose**: Live user traffic

**Configuration**:
- Full resource allocation (1024 CPU, 2GB RAM)
- INFO level logging
- Production database with backups
- Full security hardening
- Performance monitoring

## Monitoring and Observability

### Health Checks

The platform includes comprehensive health checking:

```python
# Health check endpoint implementation
GET /health
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "database": true,
  "cache": true,
  "storage": true,
  "api": true
}
```

### Metrics Monitoring

Key metrics tracked:
- **Performance**: Response time, throughput, error rate
- **Infrastructure**: CPU, memory, disk usage
- **Business**: Classification accuracy, user engagement
- **Security**: Failed authentication attempts, suspicious activity

### Alerting

Alerts configured for:
- Application errors (>1% error rate)
- High response times (>2s average)
- Infrastructure issues (>80% resource utilization)
- Security events (failed authentications, suspicious patterns)

## Security Considerations

### Secrets Management

1. **GitHub Secrets**: Store all sensitive configuration
2. **AWS Parameter Store**: Runtime secrets for applications
3. **Environment Variables**: Non-sensitive configuration

### Security Scanning

- **Daily vulnerability scans** of dependencies
- **Container image scanning** before deployment
- **Static code analysis** on every commit
- **Secrets detection** in git history

### Network Security

- **VPC isolation** for production workloads
- **Security groups** restricting network access
- **WAF protection** for web applications
- **SSL/TLS encryption** for all communications

## Troubleshooting

### Common Deployment Issues

1. **Build Failures**:
   ```bash
   # Check logs in GitHub Actions
   # Common issues: dependency conflicts, test failures

   # Fix locally and test:
   pytest tests/
   black --check src/
   flake8 src/
   ```

2. **Deployment Failures**:
   ```bash
   # Check ECS service events
   aws ecs describe-services --cluster ai-automation-production --services ai-automation-service

   # Check CloudWatch logs
   aws logs tail /ecs/ai-automation-production --follow
   ```

3. **Health Check Failures**:
   ```bash
   # Test health endpoint directly
   curl -f https://ai-automation-platform.com/health

   # Check application metrics
   python scripts/check_metrics.py --environment=production
   ```

### Rollback Procedures

1. **Automated Rollback**: Triggered automatically on deployment failure
2. **Manual Rollback**:
   ```bash
   # Switch load balancer back to blue environment
   aws elbv2 modify-listener \
     --listener-arn $PROD_LISTENER_ARN \
     --default-actions Type=forward,TargetGroupArn=$BLUE_TARGET_GROUP_ARN
   ```

## Maintenance

### Regular Tasks

1. **Weekly**:
   - Review security scan results
   - Update dependencies if needed
   - Monitor performance metrics

2. **Monthly**:
   - Rotate secrets and API keys
   - Review and update documentation
   - Analyze usage patterns and costs

3. **Quarterly**:
   - Disaster recovery testing
   - Security audit and penetration testing
   - Performance optimization review

## Support and Contact

- **Documentation**: https://ai-automation-platform.readthedocs.io
- **Issues**: https://github.com/djwilson20/universal-automation-platform/issues
- **Slack**: #ai-automation-platform
- **On-call**: PagerDuty integration for production alerts