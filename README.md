# Cloud Lab 1 — E-commerce REST API

REST API для інтернет-магазину на Flask та MySQL, розгорнутий в AWS за допомогою Docker і Terraform.

## Public URL

http://lab1-alb-1182002950.eu-north-1.elb.amazonaws.com

Health check:

http://lab1-alb-1182002950.eu-north-1.elb.amazonaws.com/health

## Infrastructure

- AWS ECS Fargate
- Amazon ECR
- Amazon RDS MySQL
- Application Load Balancer
- VPC, public/private subnets, Security Groups
- AWS Systems Manager Parameter Store
- Terraform
- GitHub Actions + OIDC

## Project structure

```text
.
├── .github/workflows/
│   └── deploy.yml
├── deploy/aws/terraform/
├── my_project/
├── app.py
├── init.sql
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── README.md
```

## Local run

```bash
docker compose up --build
```

## Deployment

Push у гілку `main` автоматично запускає GitHub Actions workflow, який збирає Docker-образ, публікує його в Amazon ECR з тегом commit SHA та оновлює ECS Service.
