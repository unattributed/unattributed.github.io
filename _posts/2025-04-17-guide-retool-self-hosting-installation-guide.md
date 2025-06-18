---
layout: post
title: "Retool Self-Hosting Installation Guide"
date: 2025-04-17
author: unattributed
categories: [self-hosting]
tags: [self-hosting-apps]
---

# Retool Self-Hosting Installation Guide for Ubuntu 24.04 LTS  
**Using Docker, NGINX, and EASY-RSA for HTTPS Certificate Management**  

## 1. Introduction  
This guide provides step-by-step instructions for self-hosting Retool on **Ubuntu 24.04 LTS** using Docker, NGINX, and **EASY-RSA** for certificate management. It addresses gaps in the official Retool documentation for environments where HTTPS certificates are generated via EASY-RSA rather than Let's Encrypt or commercial CAs.  

Covered topics:  
- **Initial Ubuntu setup** (updates, time sync, dependencies)  
- **Retool Docker installation & configuration**  
- **Private Key & CSR generation**  
- **NGINX reverse proxy setup**  
- **EASY-RSA PKI setup & certificate signing**  
- **Browser trust configuration**  

---

## 2. Reference Documents  
<table style="border-collapse: collapse; width: 100%; border: 1px solid lightgrey;">
    <thead>
        <tr style="border: 1px solid lightgrey;">
            <th style="border: 1px solid lightgrey; padding: 8px;">Document</th>
            <th style="border: 1px solid lightgrey; padding: 8px;">Link</th>
        </tr>
    </thead>
    <tbody>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">Ubuntu 24.04 LTS (Azure Marketplace)</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Azure Marketplace</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool Docker Deployment</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool Docker Docs</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool Azure VM Deployment</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool Azure Docs</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool SSL Configuration</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Retool SSL Docs</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">NGINX Docker Image</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Docker Hub</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">NGINX HTTPS Configuration</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">NGINX Docs</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">OpenSSL CSR Generation</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">OpenSSL Docs</td>
        </tr>
        <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey; padding: 8px;">EASY-RSA Setup</td>
            <td style="border: 1px solid lightgrey; padding: 8px;">Gentoo Wiki</td>
        </tr>
    </tbody>
</table>

---

## 3. Assumptions  

### Assumption 1: VM Build  
- Ubuntu 22.04 or later.  
- x86 architecture.  
- 16GiB memory, 8x vCPUs, 60GiB storage.  
- `curl` and `unzip` installed.  

### Assumption 2: Hostname and Domain  
- Fully Qualified Domain Name (FQDN) required (e.g., `retooltest.unattributed.blog`).  

### Assumption 3: Internet Access  
- Required for:  
  - Retool installation files.  
  - Docker images.  
  - Ubuntu package updates.  

---

## 4. Modifications to Ubuntu LTS  

### Step 1: Update System Packages  
```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Essential Packages  
```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common joe ntp systemd-timesyncd
```

### Step 3: Configure Time Synchronization  
```bash
sudo timedatectl set-timezone Africa/Timbuktu
sudo systemctl restart systemd-timesyncd
sudo timedatectl set-ntp on
timedatectl  # Verify NTP sync
```

---

## 5. Initial Retool Installation  

### Step 1: Clone Retool Repository  
```bash
git clone https://github.com/tryretool/retool-oppremise.git ~/retool-oppremise
```

### Step 2: Run Install Script  
```bash
cd ~/retool-oppremise
sudo ./install.sh
```
- Enter **FQDN** (e.g., `retooltest.unattributed.blog`).  

### Step 3: Backup Encryption Key  
```bash
cat ~/retool-ompremise/docker.env | grep ENCRYPTION_KEY >> docker.env.encryption_key_backup
```

---

## 6. Retool Docker Modifications  

### Step 1: Modify Dockerfile  
```bash
sed -i 's/tryretool\backend:X.Y.Z/tryretool\backend:latest/' Dockerfile
```

### Step 2: Modify CodeExecutor.Dockerfile  
```bash
sed -i 's/tryretool\code-executor-service:X.Y.Z/tryretool\code-executor-service:latest/' Codefxecutor.Dockerfile
```

### Step 3: Update `docker.env`  
- Set:  
  ```env
  LICENSE_KEY="your_license_key"
  COOKIE_INSECURE="true"
  DOMAINS="retooltest.unattributed.blog"
  ```

### Step 4: Replace NGINX Configuration  
```yaml
nginx:
    image: nginx:latest
    ports:
        - "80:80"
        - "443:443"
    command: [nginx-debug, "-g", "daemon off;"]
    volumes:
        - ./nginx:/etc/nginx/conf.d
        - ./certs:/etc/nginx/certs
    links:
        - api
    restart: always
    depends_on:
        - api
    env_file: ./docker.env
    environment:
        STAGE: "production"
        CLIENT_MAX_BODY_SIZE: 40M
        KEEPALIVE_TIMEOUT: 605
        PROXY_CONNECT_TIMEOUT: 600
        PROXY_SEND_TIMEOUT: 600
        PROXY_READ_TIMEOUT: 600
    networks:
        - frontend-network
```

---

## 7. SSL Private Key and CSR Generation  

### Step 1: Generate Private Key  
```bash
cd ~/retool-onpremise/certs
openssl genssa -out retooltest.unattributed.blog.key 4096
```

### Step 2: Generate CSR  
### Step 2: Generate CSR  
```bash
openssl req -new -newkey rsa:2048 -nodes -keyout retooltest.unattributed.blog.key -out \
retooltest.unattributed.blog.csr -subj "/C=CA/ST=Mail/L=Timbuktu/O=ACME Sprockets/OU=IT Department/CN=retooltest.unattributed.blog" \
-config <(cat /etc/ssl/openssl.cnf <(printf "[req]\ndistinguished_name=dn\n[dn] 
\n[ext]\nsubjectAltName=DNS:retooltest.unattributed.blog,IP:10.10.10.10\nbasicConstraints=critical,
CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth")) -reqexts ext
```

---

## 8. NGINX Configuration  

### Step 1: Create `nginx.conf`  
```nginx
server {
    listen 80;
    server_name retooltest.unattributed.blog;
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;
    server_name retooltest.unattributed.blog;
    ssl_certificate /etc/nginx/certs/retooltest.unattributed.blog.crt;
    ssl_certificate_key /etc/nginx/certs/retooltest.unattributed.blog.key;
    ssl_client_certificate /etc/nginx/certs/ca.crt;

    location / {
        proxy_set_header Host $host;
        proxy_pass http://api:3000;
    }
}
```

---

## 9. EASY-RSA Installation & Certificate Generation  

### Step 1: Install EASY-RSA  
```bash
sudo apt install easy-rsa  
mkdir -p ~/easy-rsa/tmp  
ln -s /usr/share/easy-rsa/* ~/easy-rsa/
```

### Step 2: Initialize PKI  
```bash
cd ~/easy-rsa  
./easyrsa init-pki
```

### Step 3: Configure `vars` File  
```bash
cp vars.example vars
```
Edit `vars` with:  
```bash
set_var EASYRSA_REQ_COUNTRY "CA"  
set_var EASYRSA_REQ_PROVINCE "Mail"  
set_var EASYRSA_REQ_CITY "Timbuktu"  
set_var EASYRSA_REQ_ORG "ACME Sprockets"  
set_var EASYRSA_REQ_EMAIL "support@unattributed.blog"  
set_var EASYRSA_REQ_OU "IT Support"  
set_var EASYRSA_NO_PASS 1  
set_var EASYRSA_KEY_SIZE 4096
```

### Step 4: Build CA & Sign Certificates  
```bash
./easyrsa build-ca  
./easyrsa import-req ~/easy-rsa/tmp/retooltest.unattributed.blog.csr retooltest  
./easyrsa sign-req server retooltest
```

### Step 5: Copy Certificates to NGINX  
```bash
cp ~/easy-rsa/issued/retooltest.crt ~/retool-ompremise/certs/
cp ~/easy-rsa/pki/ca.crt ~/retool-ompremise/certs/
```

---

## 10. Browser Configuration  

### Step 1: Import CA Certificate (Windows/macOS)  
- **Windows**: `certmgr.msc` → Import into **Trusted Root CAs**.  
- **macOS**: Keychain Access → Import into **System Keychain**.  

### Step 2: Import CA Certificate (Linux)  
```bash
sudo cp ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

### Step 3: Firefox (Manual Import)  
- Settings → Privacy & Security → Certificates → Import → Select `ca.crt`.  

---

## Conclusion  
This guide ensures a secure, self-hosted Retool deployment with EASY-RSA PKI, NGINX reverse proxy, and Docker. Verify services (`docker-compose ps`) and test HTTPS access.  

[Back to Top](#1-introduction)