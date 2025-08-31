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

**What this file provisions:**
- **Remote State Storage**: Configuration for storing Terraform state files in S3
- **State Locking**: DynamoDB table to prevent multiple people from modifying infrastructure simultaneously
- **Encryption**: Ensures state files are encrypted for security

**Why this matters:**
- **Team Collaboration**: Multiple team members can work on the same infrastructure
- **State Persistence**: State files are stored safely and backed up
- **Security**: Prevents accidental infrastructure changes and protects sensitive information
- **Audit Trail**: Keeps track of who made changes and when

```bash
bucket         = "my-tf-state-bucket"    # S3 bucket to store Terraform state
key            = "envs/dev/terraform.tfstate"  # Path within bucket for this environment
region         = "us-west-2"             # AWS region for the backend
dynamodb_table = "my-tf-locks"           # DynamoDB table for state locking (prevents concurrent modifications)
encrypt        = true                    # Encrypt state files at rest
```

**main.tf** (provider and version configuration)

**What this file provisions:**
- **Terraform Configuration**: Sets version requirements and backend configuration
- **AWS Provider**: Connects Terraform to AWS services
- **Backend Configuration**: Specifies where to store Terraform state files

**Why this matters:**
- **Version Control**: Ensures consistent Terraform behavior across team members
- **Provider Management**: Connects to AWS APIs to create and manage resources
- **State Management**: Backend configuration enables team collaboration and state persistence

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

**What this file provisions:**
- **VPC**: A private, isolated network environment in AWS
- **Public Subnet**: A network segment where resources can have public IP addresses
- **Internet Gateway**: A connection point between your VPC and the internet

**Why this matters:**
- **Network Isolation**: Keeps your resources separate from other AWS customers
- **Internet Access**: Allows your web servers to be accessible from the internet
- **Security**: Provides a foundation for implementing network security controls

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

**What this file provisions:**
- **Security Group**: A virtual firewall that controls inbound and outbound traffic to your EC2 instances
- **EC2 Instance**: A virtual server running Amazon Linux with Apache web server
- **AMI Data Source**: Dynamically finds the latest Amazon Linux operating system image

**Why this matters:**
- **Security**: Controls who can access your web server (SSH and HTTP)
- **Compute**: Provides the actual server to run your web application
- **Automation**: Automatically installs and configures the web server software

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

**What this file provisions:**
- **S3 Bucket**: A scalable object storage service for storing files, images, and static content
- **Bucket Versioning**: Keeps multiple versions of files, protecting against accidental deletion

**Why this matters:**
- **Scalability**: Can store unlimited amounts of data with high availability
- **Cost-Effective**: Pay only for what you store, no upfront infrastructure costs
- **Data Protection**: Versioning helps recover from accidental deletions or overwrites
- **Static Hosting**: Can serve static websites or store application assets

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

**What this file provisions:**
- **Input Variables**: Configurable parameters that can be set when running Terraform
- **Default Values**: Predefined values for common settings like AWS region

**Why this matters:**
- **Flexibility**: Allows the same Terraform code to be used in different environments
- **Reusability**: Variables make your Terraform modules reusable across projects
- **Environment Management**: Different values can be set for dev, staging, and production

```bash
variable "region"      { type = string, default = "us-west-2" }  # AWS region with default
variable "bucket_name" { type = string }                         # Required: S3 bucket name
```

**outputs.tf** (return values)

**What this file provisions:**
- **Output Values**: Information that Terraform displays after creating resources
- **Resource References**: Values that can be used by other Terraform modules or external systems

**Why this matters:**
- **Visibility**: Shows important information like IP addresses and resource names
- **Integration**: Outputs can be used by other tools or scripts
- **Documentation**: Provides a clear summary of what was created
- **Troubleshooting**: Helps verify that resources were created correctly

```bash
output "ec2_public_ip" { value = aws_instance.web.public_ip }   # Public IP of web server
output "s3_bucket"     { value = aws_s3_bucket.assets.bucket }  # Name of S3 bucket
```

**CLI Commands** (deployment workflow)

**What these commands do:**
- **terraform init**: Sets up the working directory and downloads required providers
- **terraform plan**: Shows what changes Terraform will make without actually applying them
- **terraform apply**: Creates, modifies, or destroys infrastructure based on your configuration

**Why this workflow matters:**
- **Safety**: Plan command lets you review changes before they happen
- **Reproducibility**: Same commands work consistently across different environments
- **Automation**: These commands can be integrated into CI/CD pipelines
- **Version Control**: Infrastructure changes are tracked and can be rolled back

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

**What this pattern provides:**
- **Environment Isolation**: Separate state files for different environments (dev, staging, prod)
- **State Management**: Each workspace maintains its own infrastructure state
- **Variable Files**: Environment-specific configurations stored in separate files

**Why this matters:**
- **Risk Mitigation**: Changes in dev don't affect production infrastructure
- **Testing**: Can test infrastructure changes safely in isolated environments
- **Team Workflow**: Different teams can work on different environments simultaneously
- **Cost Control**: Prevents accidental resource creation in production

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

---

## Server Provisioning with Terraform

### What "Server Provisioning" Really Means

**Server provisioning** is everything needed to turn "I need a server/app" into a running, reachable, monitored machine/service.

**The layers you usually provision:**

1. **Compute**: VM/instance, autoscaling group, or node pool
2. **Network**: VPC/VNet, subnets, routes, NAT/IGW, security groups/firewalls
3. **Identity & Access**: IAM roles, instance profiles, KMS keys
4. **Storage**: disks/volumes, buckets, database instances
5. **Connectivity**: load balancers, DNS records, TLS certs
6. **Base Software**: OS image, hardening, runtime (containerd/Docker), agents (telemetry, backups)
7. **Bootstrapping**: cloud-init/user-data to configure on first boot
8. **Observability**: logs/metrics/traces shipping (e.g., OpenTelemetry, CloudWatch/Stackdriver)
9. **Compliance**: tags, cost centers, encryption, backups, retention policies

### Two Philosophies of Server Management

**Mutable Servers ("Pets")**: 
- Create a VM and install stuff on it over time
- **Pros**: Familiar, easy to debug, incremental changes
- **Cons**: Configuration drift, hard to reproduce, manual maintenance

**Immutable Servers ("Cattle")**: 
- Bake a machine image (AMI/Image) with Packer, boot it, never change in place
- **Pros**: Consistent, reproducible, easy to scale, no drift
- **Cons**: More complex tooling, longer deployment times

### Declarative vs. Imperative (Why IaC Matters)

**Imperative Approach**: 
- "Click this, run that script on host X"
- **Problems**: Easy to drift, hard to reproduce, manual errors

**Declarative (IaC)**: 
- "The desired state is: 3 subnets, 2 web VMs, 1 LB"
- **Benefits**: A tool computes the diff and applies changes idempotently, reproducible, reviewable, testable

---

### Terraform in Depth

**What Terraform Does:**
- Talks to cloud/provider APIs (AWS/GCP/Azure, Cloudflare, Datadog, GitHub, Kubernetes, etc.)
- Creates/updates/destroys resources to match your **desired state** written in HCL files
- Tracks reality in **state** so it knows what exists

**Core Concepts:**

- **Provider**: Plugin that knows how to manage a platform (e.g., `hashicorp/aws`)
- **Resource**: A thing to create (e.g., `aws_instance`, `google_compute_network`)
- **Data Source**: Read-only lookup (e.g., latest Ubuntu AMI)
- **Module**: A reusable bundle of resources (your own or from the Registry)
- **Variables/Outputs/Locals**: Inputs, exported values, and computed helpers
- **State**: A JSON map of what Terraform created (store remotely with locking for teams)
- **Plan → Apply**: `terraform plan` shows the diff; `terraform apply` executes it
- **Lifecycle & Meta-args**: `depends_on`, `count`/`for_each`, `lifecycle` hooks

### Typical Workflow (GitOps-friendly)

1. **Author** HCL in a repo (one directory per module/env)
2. **Init** providers/backends: `terraform init`
3. **Validate & Format**: `terraform fmt -check`, `terraform validate`
4. **Plan** in CI, post the diff in PR for review
5. **Apply** after approval from CI (with remote state & locking)
6. **Tag & Document** the change; add runbooks/links to dashboards

### Common Patterns You'll Use

- **Remote Backend** with encryption + locking
- **Separate State Per Environment** (e.g., dev/stage/prod) rather than relying on workspaces alone
- **Module Per Concern**: network, cluster, database, app perimeter, etc.
- **Image Baking** (Packer) + **user_data/cloud-init** for first-boot
- **No or Minimal Provisioners** (use them only when unavoidable)
- **Secrets** via cloud secret managers (don't put them in state)

---

### Technical Terms Explained

**VPC (Virtual Private Cloud)**: A logically isolated section of the cloud where you can launch resources in a virtual network you define.

**Subnet**: A subdivision of your VPC that allows you to group resources and control network access.

**CIDR Block**: A way to specify IP address ranges (e.g., 10.0.0.0/16 means 10.0.0.0 to 10.0.255.255).

**Security Group**: A virtual firewall that controls inbound and outbound traffic to your resources.

**Internet Gateway**: A connection point between your VPC and the internet.

**Route Table**: A set of rules that determine where network traffic is directed.

**AMI (Amazon Machine Image)**: A template that contains the software configuration required to launch an instance.

**Instance Profile**: A container for an IAM role that you can use to pass role information to an EC2 instance when the instance starts.

**Load Balancer**: A device that distributes incoming network traffic across multiple targets.

**DNS (Domain Name System)**: A system that translates human-readable domain names into IP addresses.

**TLS (Transport Layer Security)**: A protocol that provides secure communication over a computer network.

**Autoscaling Group**: A collection of EC2 instances that automatically scales based on demand.

**Node Pool**: A group of nodes within a Kubernetes cluster that share the same configuration.

---

### Technology Distinctions

#### **Terraform vs. Kubernetes vs. Docker**

**Terraform**:
- **Purpose**: Infrastructure as Code tool
- **What it manages**: Cloud resources (VMs, networks, databases, load balancers)
- **When to use**: Setting up the foundation that your applications run on
- **Think of it as**: The "construction crew" that builds your data center

**Kubernetes (K8s)**:
- **Purpose**: Container orchestration platform
- **What it manages**: Containerized applications, their deployment, scaling, and networking
- **When to use**: Managing applications once the infrastructure exists
- **Think of it as**: The "traffic controller" that manages your running applications

**Docker**:
- **Purpose**: Containerization platform
- **What it manages**: Packaging applications and their dependencies into containers
- **When to use**: Creating portable, consistent application packages
- **Think of it as**: The "packaging system" that wraps your applications

#### **Server vs. Microservice**

**Traditional Server**:
- **Architecture**: Monolithic application running on a single server
- **Scaling**: Scale vertically (bigger server) or horizontally (more servers)
- **Deployment**: Deploy entire application at once
- **Example**: A web application with frontend, backend, and database all on one server

**Microservice**:
- **Architecture**: Application broken into small, independent services
- **Scaling**: Scale individual services independently based on demand
- **Deployment**: Deploy services independently
- **Example**: Separate services for user authentication, product catalog, and order processing

---

### End-to-End Example (Concise but Realistic)

Below is a minimal slice of what provisioning with Terraform can look like on AWS: build a tiny network, a security group, and an EC2 instance that installs Docker via cloud-init and serves traffic behind a public IP.

```hcl
terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {
    bucket         = "my-tfstate"
    key            = "dev/web.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" { region = "us-west-2" }

resource "aws_vpc" "main" { cidr_block = "10.0.0.0/16" }

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" { vpc_id = aws_vpc.main.id }

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route { cidr_block = "0.0.0.0/0", gateway_id = aws_internet_gateway.igw.id }
}

resource "aws_route_table_association" "pub_a" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "web" {
  name   = "web-sg"
  vpc_id = aws_vpc.main.id
  ingress { from_port = 80 to_port = 80 protocol = "tcp" cidr_blocks = ["0.0.0.0/0"] }
  egress  { from_port = 0  to_port = 0  protocol = "-1"   cidr_blocks = ["0.0.0.0/0"] }
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter { name = "name", values = ["ubuntu/images/hvm-ssd/ubuntu-*-amd64-server-*"] }
}

resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.web.id]
  user_data = <<-CLOUD
  #cloud-config
  packages: [docker.io]
  runcmd:
    - systemctl enable --now docker
    - docker run -d -p 80:80 --name hello nginx
  CLOUD
  tags = { Name = "web1" }
}

output "public_ip" { value = aws_instance.web.public_ip }
```

**What this does:**

- Provisions **networking** + a **public subnet** + **routing**
- Opens port **80**
- Boots an **Ubuntu** VM and uses **cloud-init** to install Docker and start **nginx**
- Prints the server's **public IP** so you can test it

**From here you'd usually add:**

- An **ALB** and a **DNS record** (Route53) → users hit `https://app.example.com`
- **TLS cert** (ACM)
- **Autoscaling group** (immutable AMIs baked with Packer)
- **Logging/metrics** pipelines
- Later, swap VMs for a **Kubernetes cluster** (EKS managed by Terraform) and deploy apps as containers

---

### Terraform vs. Configuration Management (Ansible/Chef/etc.)

**Terraform**: Creates cloud resources (VMs, networks, LB, DBs). Think **outside** the box.

**Ansible** (or cloud-init/Packer): Configures what's **inside** the box (packages, files, services).

**Many teams bake images with Packer, provision infra with Terraform, and do in-cluster app deploys with GitOps (Argo CD/Flux).**

---

### Provisioning in a Kubernetes World

**Use Terraform to create the cluster (EKS/GKE/AKS), node groups, VPC/ILB/ALB, IAM, external-dns, ingress controllers, cert-manager scaffolding.**

**Then deploy app manifests/Helm with a GitOps controller. Terraform can still manage certain infra-level K8s objects that must exist early (e.g., storage classes, cluster-wide RBAC), but avoid mixing app lifecycle with infra in the same state to keep blast radius small.**

---

### Good Practices (Battle-tested)

- Remote, locked, encrypted **state** per env (e.g., `dev`, `stage`, `prod`)
- **Small modules** with clear inputs/outputs. Version them
- **Tag everything** (owner, app, env, cost center)
- **Least-privilege IAM** for Terraform and your workloads
- **Policy as code** (OPA/Conftest, Terraform Cloud/Enterprise/Spacelift policies) to prevent risky plans
- **Cost guardrails** (budgets/alerts, quotas)
- **Runbooks & dashboards** linked from your repo

---

### Common Pitfalls

- Manually tweaking resources in the console → **drift** surprises in the next plan
- Renaming resources without `moved {}` or `terraform import` → accidental **destroy/recreate**
- Storing secrets in variables/state → leaks. Use a secret manager
- Overusing `null_resource` and provisioners → fragile. Prefer images/cloud-init/CM tools
- One giant state for everything → slow plans, big blast radius. Split by domain/env

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
