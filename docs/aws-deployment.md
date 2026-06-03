# AWS Deployment

Recommended production-style path:

1. Build backend and frontend container images.
2. Push images to Amazon ECR.
3. Run backend on ECS Fargate or AWS App Runner.
4. Serve frontend through S3/CloudFront or a containerized web service.
5. Run PostgreSQL on Amazon RDS with pgvector support where available.
6. Store secrets in AWS Secrets Manager.
7. Add CloudWatch metrics, logs, alarms, and autoscaling policies.

This repo is a portfolio MVP. A real healthcare deployment also requires HIPAA controls, security review, BAAs, authentication, authorization, audit logging, encryption, and compliance approval.
