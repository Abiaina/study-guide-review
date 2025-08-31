---
title: DevOps
---

# DevOps & Cloud — Worked Examples

The goal here is to be able to “drop in” a minimal but realistic setup during interviews or when spinning up a demo.

## 1) Terraform mini-project (AWS VPC + EC2 + S3, remote state)

### Key Infrastructure Concepts

#### **VPC (Virtual Private Cloud)**
A **VPC** is a logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network that you define. Think of it as your own private data center in the cloud.

**What it provides:**
- **Network isolation** from other AWS customers
- **Custom IP address ranges** (CIDR blocks like 10.0.0.0/16)
- **Subnet configuration** for organizing resources
- **Route tables** for controlling traffic flow
- **Security groups** and **Network ACLs** for access control
- **Internet connectivity** control (public vs private subnets)

**Why it matters:**
- **Security**: Isolates your resources from other AWS customers
- **Compliance**: Required for HIPAA, SOC2, and other security standards
- **Cost control**: Prevents unauthorized resource creation
- **Network design**: Allows you to design your network architecture

#### **Subnets**
**Subnets** are subdivisions of your VPC that allow you to group resources and control network access. They're like different floors or sections in a building.

**Types of Subnets:**
- **Public Subnets**: 
  - Resources can have public IP addresses
  - Direct internet access through Internet Gateway
  - Used for load balancers, bastion hosts
  - **Security risk**: More exposed to internet threats
  
- **Private Subnets**:
  - No public IP addresses assigned
  - Internet access through NAT Gateway (controlled)
  - Used for application servers, databases
  - **Security benefit**: Protected from direct internet access

**Subnet Design Best Practices:**
- **Availability Zones**: Distribute subnets across multiple AZs for high availability
- **CIDR Planning**: Use non-overlapping IP ranges (e.g., 10.0.1.0/24, 10.0.2.0/24)
- **Resource Grouping**: Group similar resources in the same subnet
- **Security**: Use private subnets for sensitive resources

#### **Spot Instances**
**Spot Instances** are AWS EC2 instances that you can bid on and use for up to 90% off the On-Demand price. AWS sells unused capacity at a discount.

**How Spot Instances Work:**
- **Bidding**: You set a maximum price you're willing to pay
- **Availability**: AWS fills your request if spot price ≤ your bid
- **Interruption**: AWS can terminate your instance with 2-minute notice if:
  - Spot price exceeds your bid
  - AWS needs the capacity back
  - Spot capacity is no longer available

**Use Cases:**
- **Batch processing**: Data analysis, video encoding, scientific computing
- **Testing/Development**: Non-critical workloads
- **Cost optimization**: Up to 90% savings vs On-Demand
- **Fault-tolerant applications**: Can handle interruptions

**Spot Instance Strategies:**
- **Diversification**: Use multiple instance types and AZs
- **Bid strategy**: Set bid at On-Demand price for better availability
- **Interruption handling**: Implement graceful shutdown and recovery
- **Fallback**: Use On-Demand instances as backup

#### **Incident Severity Levels (SEV 1-4)**

**SEV-1 (Critical) - "All Hands on Deck"**
- **Definition**: Service completely down, data loss, security breach
- **Response Time**: Immediate (within 5 minutes)
- **Communication**: All stakeholders, status page updates, executive notification
- **Resolution Target**: 1 hour
- **Examples**: 
  - Database corruption
  - Complete service outage
  - Customer data breach
  - Payment system failure

**SEV-2 (High) - "Urgent Response Required"**
- **Definition**: Major feature broken, significant performance degradation
- **Response Time**: Within 15 minutes
- **Communication**: Engineering team, product managers, customer support
- **Resolution Target**: 4 hours
- **Examples**:
  - Core feature unavailable
  - 50%+ performance degradation
  - Multiple customers affected
  - Revenue-impacting issues

**SEV-3 (Medium) - "Normal Priority"**
- **Definition**: Minor feature broken, slight performance impact
- **Response Time**: Within 1 hour
- **Communication**: Engineering team, internal stakeholders
- **Resolution Target**: 24 hours
- **Examples**:
  - Non-critical feature broken
  - Minor performance issues
  - Limited customer impact
  - Cosmetic bugs

**SEV-4 (Low) - "Business Hours"**
- **Definition**: Cosmetic issues, minor bugs, enhancement requests
- **Response Time**: Within 4 hours
- **Communication**: Engineering team
- **Resolution Target**: 1 week
- **Examples**:
  - UI text typos
  - Minor styling issues
  - Enhancement requests
  - Documentation updates

### Multi-Environment Setup
This example shows how to structure Terraform for multiple environments (dev, staging, prod) with shared modules.

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

**backend.hcl** (remote state configuration)
```bash
bucket         = "my-tf-state-bucket"    # S3 bucket to store Terraform state
key            = "envs/dev/terraform.tfstate"  # Path within bucket for this environment
region         = "us-west-2"             # AWS region for the backend
dynamodb_table = "my-tf-locks"           # DynamoDB table for state locking (prevents concurrent modifications)
encrypt        = true                    # Encrypt state files at rest
```

**main.tf** (provider and version configuration)
```bash
terraform {
  required_version = ">= 1.6.0"         # Minimum Terraform version required
  backend "s3" {}                       # Use S3 backend for remote state (configured via backend.hcl at init-time)
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }  # AWS provider with version constraint
  }
}

provider "aws" {
  region = var.region                    # AWS region for all resources
}
```

**vpc.tf** (networking infrastructure)
```bash
# Virtual Private Cloud - isolated network environment
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"           # Private IP range: 10.0.0.0 to 10.0.255.255
  tags = { Name = "demo-vpc" }          # Resource tagging for cost tracking and organization
}

# Public subnet in availability zone 'a' - accessible from internet
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.main.id                    # Associate with our VPC
  cidr_block              = "10.0.1.0/24"                     # Subnet range: 10.0.1.0 to 10.0.1.255
  map_public_ip_on_launch = true                               # Auto-assign public IPs to instances
  availability_zone       = "${var.region}a"                   # Place in first AZ (e.g., us-west-2a)
}

# Internet Gateway - allows VPC to communicate with internet
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id              # Attach to our VPC
}
```

**ec2.tf** (compute and security)
```bash
# Security Group - firewall rules for EC2 instances
resource "aws_security_group" "web" {
  name   = "web-sg"                     # Security group name
  vpc_id = aws_vpc.main.id             # Associate with our VPC

  # Allow SSH access from anywhere (0.0.0.0/0 = all IPs)
  ingress {
    from_port = 22                      # SSH port
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]        # WARNING: In production, restrict to specific IPs
  }
  
  # Allow HTTP access from anywhere (for web traffic)
  ingress {
    from_port = 80                      # HTTP port
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]        # WARNING: In production, restrict to specific IPs
  }
  
  # Allow all outbound traffic (instances can reach internet)
  egress {
    from_port = 0                       # All ports
    to_port   = 0
    protocol  = "-1"                    # All protocols
    cidr_blocks = ["0.0.0.0/0"]        # All destinations
  }
}

# Data source to get latest Amazon Linux AMI
data "aws_ami" "amazon_linux" {
  most_recent = true                    # Get the newest available
  owners = ["amazon"]                   # Official Amazon AMIs
  filter {
    name = "name"                       # Filter by AMI name
    values = ["al2023-ami-*-x86_64"]   # Amazon Linux 2023, 64-bit
  }
}
```

resource "aws_instance" "web" {
  ami                    = data.aws_ami.amazon_linux.id    # Use the AMI we found earlier
  instance_type          = "t3.micro"                      # Small instance type (1 vCPU, 1 GB RAM)
  subnet_id              = aws_subnet.public_a.id          # Place in our public subnet
  vpc_security_group_ids = [aws_security_group.web.id]     # Apply our security group rules
  
  # User data script runs when instance first boots
  user_data = <<-EOF
              #!/bin/bash
              yum install -y httpd                          # Install Apache web server
              systemctl enable httpd                        # Start Apache on boot
              systemctl start httpd                         # Start Apache now
              echo "hello from terraform" > /var/www/html/index.html  # Create simple webpage
              EOF
  
  tags = { Name = "web" }                                  # Resource tagging
}
```

**s3.tf** (object storage)
```bash
# S3 bucket for storing static assets (images, CSS, JS files)
resource "aws_s3_bucket" "assets" {
  bucket = var.bucket_name                                 # Bucket name from variable
  tags = { Name = "assets" }                               # Resource tagging
}

# Enable versioning to keep multiple versions of objects
resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id                         # Reference to our bucket
  versioning_configuration {
    status = "Enabled"                                      # Turn on versioning
  }
}
```

**variables.tf** (input parameters)
```bash
variable "region"      { type = string, default = "us-west-2" }  # AWS region with default
variable "bucket_name" { type = string }                         # Required: S3 bucket name
```

**outputs.tf** (return values)
```bash
output "ec2_public_ip" { value = aws_instance.web.public_ip }   # Public IP of web server
output "s3_bucket"     { value = aws_s3_bucket.assets.bucket }  # Name of S3 bucket
```

**CLI Commands** (deployment workflow)
```bash
# Initialize Terraform and configure backend
terraform init -backend-config=backend.hcl

# Preview changes before applying
terraform plan -var="bucket_name=my-artifacts-bucket"

# Apply changes and create infrastructure
terraform apply -auto-approve -var="bucket_name=my-artifacts-bucket"
```

### Advanced Terraform Patterns

#### Workspace-based Environment Management
```bash
# Create and switch to dev workspace (isolates state for different environments)
terraform workspace new dev
terraform workspace select dev

# Apply with environment-specific variables
terraform apply -var-file="dev.tfvars"

# Switch to prod workspace (different state, different environment)
terraform workspace select prod
terraform apply -var-file="prod.tfvars"
```

#### Module-based Architecture
```hcl
# modules/vpc/main.tf - Reusable VPC module
module "vpc" {
  source = "../../modules/vpc"                              # Path to module source
  
  environment = var.environment                             # Pass environment name
  vpc_cidr   = var.vpc_cidr                                # Pass VPC CIDR block
  azs         = var.azs                                     # Pass availability zones
}

# modules/vpc/variables.tf - Module input variables
variable "environment" {
  description = "Environment name (dev, staging, prod)"     # Variable documentation
  type        = string                                      # Variable type
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
}

variable "azs" {
  description = "Availability zones"
  type        = list(string)
}
```

#### Security Best Practices
```hcl
# Enable VPC Flow Logs
resource "aws_flow_log" "vpc_flow_log" {
  iam_role_arn    = aws_iam_role.vpc_flow_log_role.arn
  log_destination = aws_cloudwatch_log_group.vpc_flow_log_group.arn
  traffic_type    = "ALL"
  vpc_id          = aws_vpc.main.id
}

# Enable VPC Endpoints for private subnets
resource "aws_vpc_endpoint" "s3" {
  vpc_id       = aws_vpc.main.id
  service_name = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [aws_route_table.private.id]
}
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
            limits: { cpu: "500m", memory: "256Mi" }
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
