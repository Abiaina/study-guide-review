---
title: Security & Compliance
---

# Security & Compliance

## 1. HIPAA Compliance

### Protected Health Information (PHI)
- **Definition**: Individually identifiable health information
- **Examples**: Names, addresses, dates, medical records, insurance info
- **Storage**: Must be encrypted at rest and in transit

### Business Associate Agreement (BAA)
- **Required**: When sharing PHI with third-party services
- **Coverage**: Data processing, storage, transmission
- **Penalties**: Up to $50,000 per violation

### Technical Safeguards
- **Access Control**: Unique user identification, automatic logoff
- **Audit Controls**: Record and examine access to PHI
- **Integrity**: Ensure PHI is not altered or destroyed
- **Transmission Security**: Encrypt PHI in transit

### Physical Safeguards
- **Facility Access**: Control physical access to facilities
- **Workstation Security**: Secure workstations and devices
- **Media Controls**: Control access to media containing PHI

---

## 2. Security Patterns

### Authentication
- **Multi-Factor Authentication (MFA)**: Something you know, have, are
- **OAuth 2.0**: Authorization framework for third-party access
- **JWT Tokens**: Stateless authentication with expiration
- **Session Management**: Secure session creation and termination

### Authorization
- **Role-Based Access Control (RBAC)**: Assign permissions to roles
- **Attribute-Based Access Control (ABAC)**: Dynamic access based on attributes
- **Principle of Least Privilege**: Minimum access necessary
- **Just-In-Time Access**: Temporary elevated permissions

### Encryption
- **At Rest**: AES-256 for stored data
- **In Transit**: TLS 1.3 for network communication
- **Key Management**: Hardware Security Modules (HSM)
- **Data Classification**: Different encryption levels for different data types

---

## 3. Common Security Vulnerabilities

### OWASP Top 10
1. **Injection**: SQL, NoSQL, OS command injection
2. **Broken Authentication**: Weak passwords, session fixation
3. **Sensitive Data Exposure**: Unencrypted data, weak algorithms
4. **XML External Entities**: XXE attacks on XML processors
5. **Broken Access Control**: Insecure direct object references
6. **Security Misconfiguration**: Default settings, unnecessary features
7. **Cross-Site Scripting (XSS)**: Stored, reflected, DOM-based
8. **Insecure Deserialization**: Object injection attacks
9. **Using Components with Known Vulnerabilities**: Outdated libraries
10. **Insufficient Logging & Monitoring**: Lack of security visibility

### Prevention Strategies
- **Input Validation**: Sanitize all user inputs
- **Output Encoding**: Encode data before sending to browser
- **Security Headers**: CSP, HSTS, X-Frame-Options
- **Regular Updates**: Keep dependencies and systems updated

---

## 4. Security Implementation Examples

### Secure Password Storage
```python
import bcrypt
import secrets

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_secure_token():
    return secrets.token_urlsafe(32)
```

### JWT Implementation
```python
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"

def create_token(user_id, expires_in=3600):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
```

### Rate Limiting
```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id):
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove old requests outside window
        client_requests[:] = [req_time for req_time in client_requests 
                            if now - req_time < self.window_seconds]
        
        if len(client_requests) >= self.max_requests:
            return False
        
        client_requests.append(now)
        return True

# Usage
limiter = RateLimiter(max_requests=100, window_seconds=60)
if limiter.is_allowed("user123"):
    # Process request
    pass
else:
    # Rate limit exceeded
    pass
```

---

## 5. HTTPS & Transport Layer Security

### How HTTPS Works
HTTPS (HTTP Secure) combines HTTP with TLS/SSL encryption to provide:
- **Confidentiality**: Data is encrypted and cannot be read by interceptors
- **Integrity**: Data cannot be modified without detection
- **Authentication**: Verifies the server's identity

### TLS Handshake Process
```
1. Client Hello
   ├── Supported TLS versions
   ├── Supported cipher suites
   ├── Random number
   └── Session ID (if resuming)

2. Server Hello
   ├── Chosen TLS version
   ├── Chosen cipher suite
   ├── Random number
   ├── Session ID
   └── Digital certificate

3. Certificate Verification
   ├── Client verifies server certificate
   ├── Checks certificate chain
   └── Validates domain name

4. Key Exchange
   ├── Client generates pre-master secret
   ├── Encrypts with server's public key
   └── Both sides derive master secret

5. Finished
   ├── Both sides verify handshake
   ├── Switch to encrypted communication
   └── Application data exchange begins
```

### SSL/TLS Configuration
```nginx
# Nginx HTTPS configuration
server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL certificate and key
    ssl_certificate /etc/ssl/certs/example.com.crt;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/ssl/certs/chain.crt;
}
```

### Certificate Management
```bash
# Generate private key
openssl genrsa -out private.key 2048

# Generate CSR (Certificate Signing Request)
openssl req -new -key private.key -out request.csr

# Generate self-signed certificate (for testing)
openssl req -x509 -new -nodes -key private.key -sha256 -days 365 -out certificate.crt

# Check certificate details
openssl x509 -in certificate.crt -text -noout

# Convert between formats
openssl x509 -in certificate.crt -outform DER -out certificate.der
```

---

## 6. Essential Security Libraries & Tools

### Python Security Libraries
```python
# Cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Secure random generation
import secrets
import os

# Password hashing
import bcrypt
import passlib.hash

# JWT handling
import PyJWT

# Input validation
import validators
import bleach

# Security headers
from flask_talisman import Talisman
```

### Security Headers Implementation
```python
from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)

# Configure security headers
Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline'",
        'style-src': "'self' 'unsafe-inline'",
        'img-src': "'self' data: https:",
        'font-src': "'self'",
        'connect-src': "'self'",
        'frame-ancestors': "'none'"
    },
    force_https=True,
    strict_transport_security=True,
    session_cookie_secure=True
)

@app.route('/')
def index():
    return 'Secure Flask App'
```

### Input Sanitization
```python
import bleach
import validators
from urllib.parse import urlparse

def sanitize_html(html_content):
    """Remove potentially dangerous HTML"""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
    allowed_attributes = {}
    
    return bleach.clean(html_content, 
                        tags=allowed_tags, 
                        attributes=allowed_attributes,
                        strip=True)

def validate_url(url):
    """Validate and sanitize URLs"""
    if not validators.url(url):
        return None
    
    parsed = urlparse(url)
    if parsed.scheme not in ['http', 'https']:
        return None
    
    return url

def sanitize_filename(filename):
    """Remove dangerous characters from filenames"""
    import re
    # Remove or replace dangerous characters
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return safe_filename[:255]  # Limit length
```

### Secure File Upload
```python
import os
import hashlib
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_upload(file, upload_folder):
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Generate unique filename to prevent conflicts
        file_hash = hashlib.md5(file.read()).hexdigest()
        file.seek(0)  # Reset file pointer
        
        # Create safe filename with hash
        safe_filename = f"{file_hash}_{filename}"
        filepath = os.path.join(upload_folder, safe_filename)
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            raise ValueError("File too large")
        
        # Save file
        file.save(filepath)
        return safe_filename
    
    raise ValueError("Invalid file type or no file provided")
```

---

## 7. Security Best Practices

### Development Security
- **Secure by Default**: Deny access unless explicitly allowed
- **Input Validation**: Validate and sanitize all inputs
- **Output Encoding**: Encode data before sending to clients
- **Error Handling**: Don't expose sensitive information in errors
- **Logging**: Log security events without sensitive data

### Production Security
- **Regular Updates**: Keep systems and dependencies updated
- **Access Control**: Implement least privilege access
- **Monitoring**: Monitor for suspicious activities
- **Backup Security**: Encrypt backups and test restoration
- **Incident Response**: Have a plan for security incidents

### Security Testing
- **Static Analysis**: Use tools like Bandit, Semgrep
- **Dynamic Testing**: Regular penetration testing
- **Dependency Scanning**: Check for known vulnerabilities
- **Code Reviews**: Security-focused code reviews
- **Automated Testing**: Security tests in CI/CD pipeline

### Compliance Checklist
- [ ] Data encryption at rest and in transit
- [ ] Access controls and authentication
- [ ] Audit logging and monitoring
- [ ] Regular security assessments
- [ ] Employee security training
- [ ] Incident response procedures
- [ ] Data backup and recovery
- [ ] Vendor security assessments
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.JWTError:
        raise Exception("Invalid token")
```

### Rate Limiting
```python
import redis
import time

class RateLimiter:
    def __init__(self, redis_client, max_requests, window_seconds):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_allowed(self, key):
        current = int(time.time())
        window_start = current - self.window_seconds
        
        # Remove expired entries
        self.redis.zremrangebyscore(key, 0, window_start)
        
        # Count current requests
        current_requests = self.redis.zcard(key)
        
        if current_requests < self.max_requests:
            self.redis.zadd(key, {current: current})
            self.redis.expire(key, self.window_seconds)
            return True
        
        return False
```

---

## 5. Compliance Checklists

### HIPAA Technical Safeguards
- [ ] Unique user identification implemented
- [ ] Automatic logoff configured
- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled
- [ ] Audit logging configured
- [ ] Access controls implemented
- [ ] Integrity controls in place

### HIPAA Audit Preparation & Process
**What HIPAA Auditors Look For:**

1. **Administrative Safeguards**
   - [ ] Security officer designated and trained
   - [ ] Workforce security policies documented
   - [ ] Information access management procedures
   - [ ] Security incident procedures documented
   - [ ] Contingency plan tested annually
   - [ ] Business associate agreements (BAAs) in place

2. **Physical Safeguards**
   - [ ] Facility access controls implemented
   - [ ] Workstation use policies documented
   - [ ] Workstation security measures in place
   - [ ] Device and media controls established
   - [ ] Media disposal procedures documented

3. **Technical Safeguards**
   - [ ] Access control implementation verified
   - [ ] Audit logs enabled and monitored
   - [ ] Integrity controls implemented
   - [ ] Person/entity authentication verified
   - [ ] Transmission security measures in place

**Common HIPAA Compliance Gaps:**
- Missing or outdated BAAs with vendors
- Inadequate audit logging and monitoring
- Insufficient encryption key management
- Lack of regular security assessments
- Missing incident response documentation
- Incomplete workforce training records

**Audit Preparation Checklist:**
- [ ] Review all policies and procedures
- [ ] Verify BAA compliance with vendors
- [ ] Test backup and recovery procedures
- [ ] Review access control logs
- [ ] Verify encryption implementation
- [ ] Prepare workforce training records
- [ ] Review incident response procedures
- [ ] Test contingency plan procedures

### Security Algorithm Deep Dive

#### JWT Signing Algorithms Comparison

**HS256 (HMAC with SHA-256)**
- **Type**: Symmetric (same key for signing and verification)
- **Security**: High when using strong secret keys
- **Use Case**: Single-party applications, internal services
- **Pros**: Fast, simple key management
- **Cons**: Key must be shared securely, can't verify origin

**RS256 (RSA with SHA-256)**
- **Type**: Asymmetric (public/private key pair)
- **Security**: Very high, industry standard
- **Use Case**: Multi-party applications, public APIs
- **Pros**: Can verify token origin, private key never shared
- **Cons**: Slower than HS256, more complex key management

**ES256 (ECDSA with SHA-256)**
- **Type**: Asymmetric (elliptic curve)
- **Security**: Very high, smaller key sizes
- **Use Case**: Resource-constrained environments
- **Pros**: Fast verification, small key sizes
- **Cons**: More complex implementation, newer standard

**Algorithm Selection Guide:**
```python
# For internal services (single organization)
ALGORITHM = "HS256"  # Use strong secret key (32+ bytes)

# For public APIs or multi-tenant systems
ALGORITHM = "RS256"  # Use RSA key pair

# For IoT or mobile applications
ALGORITHM = "ES256"  # Use ECDSA for efficiency

# Implementation example with algorithm selection
def create_token_with_algorithm(data: dict, algorithm: str = "HS256"):
    if algorithm == "HS256":
        return jwt.encode(data, SECRET_KEY, algorithm=algorithm)
    elif algorithm == "RS256":
        return jwt.encode(data, PRIVATE_KEY, algorithm=algorithm)
    elif algorithm == "ES256":
        return jwt.encode(data, ECDSA_PRIVATE_KEY, algorithm=algorithm)
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
```

#### Encryption Key Management Best Practices

**Key Rotation Strategy:**
- **HS256**: Rotate secret keys every 90 days
- **RS256/ES256**: Rotate private keys every 1-2 years
- **Public keys**: Can be published and shared freely

**Key Storage Security:**
```python
# Secure key storage examples
import os
from cryptography.fernet import Fernet

# Environment variable (for development)
SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

# AWS KMS (for production)
import boto3
kms = boto3.client('kms')
response = kms.decrypt(CiphertextBlob=encrypted_key)
SECRET_KEY = response['Plaintext']

# HashiCorp Vault (enterprise)
import hvac
client = hvac.Client(url='https://vault.example.com')
SECRET_KEY = client.secrets.kv.v2.read_secret_version(path='jwt-secret')['data']['data']['key']
```

### General Security Checklist
- [ ] MFA enabled for all users
- [ ] Regular security training conducted
- [ ] Vulnerability scanning scheduled
- [ ] Incident response plan documented
- [ ] Backup and recovery tested
- [ ] Security monitoring active
- [ ] Access reviews conducted quarterly

### Data Protection Checklist
- [ ] Data classification completed
- [ ] Encryption policies defined
- [ ] Key management procedures documented
- [ ] Data retention policies established
- [ ] Privacy impact assessments completed
- [ ] Consent mechanisms implemented
- [ ] Data breach response plan ready

---

## 6. Security Monitoring

### Log Management
- **Centralized Logging**: Aggregate logs from all systems
- **Log Analysis**: Use SIEM tools for correlation
- **Retention Policies**: Keep logs for compliance requirements
- **Access Controls**: Restrict log access to security team

### Incident Response
- **Detection**: Automated alerts for suspicious activity
- **Response**: Documented procedures for different incident types
- **Recovery**: Steps to restore normal operations
- **Post-Incident**: Lessons learned and process improvements

### Security Metrics
- **Mean Time to Detection (MTTD)**: How quickly threats are identified
- **Mean Time to Response (MTTR)**: How quickly threats are contained
- **False Positive Rate**: Accuracy of security alerts
- **Vulnerability Remediation Time**: Speed of patch deployment

---

## 7. Cloud Security

### AWS Security Best Practices
- **IAM**: Use least privilege, enable MFA
- **VPC**: Isolate resources, use security groups
- **Encryption**: Enable encryption for S3, RDS, EBS
- **Monitoring**: Use CloudTrail, CloudWatch, GuardDuty

### Azure Security Best Practices
- **Azure AD**: Implement conditional access policies
- **Network Security**: Use NSGs, Azure Firewall
- **Data Protection**: Enable encryption, use Key Vault
- **Monitoring**: Use Azure Security Center, Sentinel

### GCP Security Best Practices
- **IAM**: Use custom roles, enable MFA
- **VPC**: Use firewall rules, enable flow logs
- **Encryption**: Enable customer-managed encryption keys
- **Monitoring**: Use Security Command Center

---

## 8. Security Tools

### Static Analysis
- **SonarQube**: Code quality and security analysis
- **Snyk**: Dependency vulnerability scanning
- **Bandit**: Python security linter
- **ESLint**: JavaScript security rules

### Dynamic Analysis
- **OWASP ZAP**: Web application security testing
- **Burp Suite**: Web application security testing
- **Nmap**: Network security scanning
- **Metasploit**: Penetration testing framework

### Monitoring Tools
- **ELK Stack**: Log aggregation and analysis
- **Splunk**: Security information and event management
- **Wireshark**: Network protocol analyzer
- **Snort**: Intrusion detection system

---

## 9. Security Training

### Developer Security
- **Secure Coding**: Input validation, output encoding
- **Authentication**: Secure session management
- **Authorization**: Access control implementation
- **Data Protection**: Encryption and key management

### Operations Security
- **System Hardening**: Remove unnecessary services
- **Patch Management**: Regular security updates
- **Network Security**: Firewall configuration
- **Incident Response**: Security event handling

### Compliance Training
- **HIPAA Requirements**: PHI protection guidelines
- **Data Privacy**: GDPR, CCPA compliance
- **Security Policies**: Company security procedures
- **Reporting Procedures**: Security incident reporting
