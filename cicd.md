# DevOps & Cloud — Worked Examples

The goal here is to be able to “drop in” a minimal but realistic setup during interviews or when spinning up a demo.

## 1) Terraform mini-project (AWS VPC + EC2 + S3, remote state)

**Layout**

```
terraform/
  main.tf
  vpc.tf
  ec2.tf
  s3.tf
  variables.tf
  outputs.tf
  backend.hcl
```

**backend.hcl** (remote state)

```hcl
bucket         = "my-tf-state-bucket"
key            = "envs/dev/terraform.tfstate"
region         = "us-west-2"
dynamodb_table = "my-tf-locks"
encrypt        = true
```

**main.tf**

```hcl
terraform {
  required_version = ">= 1.6.0"
  backend "s3" {}          # configured via backend.hcl at init-time
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
}

provider "aws" {
  region = var.region
}
```

**vpc.tf** (very minimal)

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "demo-vpc" }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.region}a"
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}
```

**ec2.tf**

```hcl
resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners = ["amazon"]
  filter {
    name = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public_a.id
  vpc_security_group_ids = [aws_security_group.web.id]
  user_data = <<-EOF
              #!/bin/bash
              yum install -y httpd
              systemctl enable httpd
              systemctl start httpd
              echo "hello from terraform" > /var/www/html/index.html
              EOF
  tags = { Name = "web" }
}
```

**s3.tf**

```hcl
resource "aws_s3_bucket" "assets" {
  bucket = var.bucket_name
  tags = { Name = "assets" }
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}
```

**variables.tf**

```hcl
variable "region"      { type = string, default = "us-west-2" }
variable "bucket_name" { type = string }
```

**outputs.tf**

```hcl
output "ec2_public_ip" { value = aws_instance.web.public_ip }
output "s3_bucket"     { value = aws_s3_bucket.assets.bucket }
```

**CLI**

```bash
terraform init -backend-config=backend.hcl
terraform plan -var="bucket_name=my-artifacts-bucket"
terraform apply -auto-approve -var="bucket_name=my-artifacts-bucket"
```

---

## 2) Jenkinsfile (build → test → Docker → push → deploy to K8s)

```groovy
pipeline {
  agent any
  environment {
    APP_NAME = 'example-svc'
    AWS_REGION = 'us-west-2'
    ECR_REPO = "123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com/${APP_NAME}"
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Test') {
      steps {
        sh 'python -m pip install -r requirements.txt'
        sh 'pytest -q'
      }
    }
    stage('Build Image') {
      steps {
        sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
      }
    }
    stage('Login ECR & Push') {
      steps {
        sh 'aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin 123456789012.dkr.ecr.${AWS_REGION}.amazonaws.com'
        sh 'docker tag ${APP_NAME}:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}'
        sh 'docker push ${ECR_REPO}:${BUILD_NUMBER}'
      }
    }
    stage('Deploy to K8s') {
      steps {
        sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${ECR_REPO}:${BUILD_NUMBER} --record'
      }
    }
  }
}
```

---

## 3) Kubernetes Manifests (Deployment + Service + Ingress)

**deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: example-svc
  labels:
    app: example-svc
spec:
  replicas: 2
  selector:
    matchLabels:
      app: example-svc
  template:
    metadata:
      labels:
        app: example-svc
    spec:
      containers:
      - name: example-svc
        image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/example-svc:latest
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet: { path: /healthz, port: 8080 }
          initialDelaySeconds: 3
        livenessProbe:
          httpGet: { path: /livez, port: 8080 }
          initialDelaySeconds: 5
        resources:
          requests: { cpu: "100m", memory: "128Mi" }
          limits:   { cpu: "500m", memory: "256Mi" }
```

**service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: example-svc
spec:
  selector:
    app: example-svc
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
```

**ingress.yaml** (requires ingress controller)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-svc
spec:
  rules:
  - host: example.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: example-svc
            port:
              number: 80
```

**Apply**

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

---

## 4) Prometheus Alerting Rules (examples)

**alert-rules.yaml**

```yaml
groups:
- name: app.rules
  rules:
  - alert: HighCPU
    expr: avg(rate(container_cpu_usage_seconds_total{container!="",pod=~"example-svc.*"}[5m])) > 0.8
    for: 5m
    labels: { severity: warning }
    annotations:
      summary: "High CPU usage on example-svc"
      description: "CPU > 80% for 5m"

  - alert: HighErrorRate
    expr: rate(http_requests_total{job="example-svc",code=~"5.."}[5m]) / rate(http_requests_total{job="example-svc"}[5m]) > 0.05
    for: 10m
    labels: { severity: critical }
    annotations:
      summary: "High 5xx error rate"
      description: ">5% 5xx over 10m"

  - alert: CrashLooping
    expr: increase(kube_pod_container_status_restarts_total{pod=~"example-svc.*"}[10m]) > 3
    for: 10m
    labels: { severity: warning }
    annotations:
      summary: "Pod restarting frequently"
      description: "More than 3 restarts in 10 minutes"
```

> Wire this into Prometheus via `rule_files` and configure Alertmanager receivers (email/Slack/PagerDuty).

---

