---
layout: post
title: "Primer - Bypassing Cloudflare Protection in Red Team Engagements"
date: 2025-06-18
author: unattributed
categories: [redteaming, cobalt-strike, cloudflare]
tags: [redteaming, cobalt-strike,cloudflare]
---


### **Bypassing Cloudflare Protection in Red Team Engagements**  
Cloudflare is a common obstacle for red teams because it hides the real IP of a target, provides WAF (Web Application Firewall) protection, and can block malicious traffic. To simulate a real-world attack, you’ll need to bypass Cloudflare to reach the actual infrastructure.  

---

## **1. Identify the Real Server IP (Behind Cloudflare)**  
Cloudflare acts as a reverse proxy, so the first step is finding the **origin server’s true IP**.  

### **Methods to Unmask the Real IP**  
#### **A. Historical DNS Records**  
- Check if the domain ever pointed directly to the origin IP before Cloudflare was enabled.  
- Tools:  
  - **SecurityTrails** ([securitytrails.com](https://securitytrails.com/))  
  - **DNSDumpster** ([dnsdumpster.com](https://dnsdumpster.com/))  
  - **WHOIS Lookup** (e.g., `whois example.com`)  

#### **B. Subdomain Enumeration**  
- Some subdomains (e.g., `direct.example.com`, `origin.example.com`) may bypass Cloudflare.  
- Tools:  
  - **Amass** (`amass enum -d example.com`)  
  - **Sublist3r** (`sublist3r -d example.com`)  
  - **Censys/Shodan** (search for SSL certs tied to the real IP)  

#### **C. Misconfigured Services**  
- **Email Servers** (MX records sometimes point to the real IP).  
- **FTP/SSH/SMTP** (these services may not be proxied).  
- **Old Database Leaks** (check breaches for exposed server info).  

#### **D. Cloudflare Bypass via Vulnerabilities**  
- **Server Status Leaks** (e.g., `server-status` pages on Apache).  
- **Cloudflare Cache Poisoning** (if misconfigured).  
- **SSRF (Server-Side Request Forgery)** (if an internal service leaks the IP).  

---

## **2. Bypassing Cloudflare WAF (Web Application Firewall)**  
If you can’t find the real IP, you may need to bypass Cloudflare’s WAF to reach the backend.  

### **A. Obfuscate Attack Payloads**  
- **Case Switching**: `SeLeCt` instead of `SELECT` (SQLi).  
- **URL Encoding**: `%27` instead of `'` (SQLi).  
- **Comment Injection**: `/*!50000SELECT*/` (SQLi).  
- **Header Manipulation**: Fake `X-Forwarded-For` or `User-Agent`.  

### **B. Slowloris/DOS Evasion**  
- Cloudflare may throttle aggressive scans. Slow down requests:  
  - **Burp Suite Intruder** (set delays between requests).  
  - **Nikto** (`-delay 1`).  

### **C. Use Alternate Protocols**  
- If HTTP(S) is blocked, try:  
  - **DNS Exfiltration** (if allowed).  
  - **WebSockets** (if not WAF-protected).  

---

## **3. Redirector Setup (Evading Cloudflare Detection)**  
If you’re the attacker (red team) and want to **hide your C2 server** behind Cloudflare:  

### **A. Legitimate-Looking Redirectors**  
1. **Register a Clean Domain** (e.g., `cdn-service[.]net`).  
2. **Point to Cloudflare** (enable proxy in DNS settings).  
3. **Forward Traffic to Team Server** (using reverse proxy rules).  

### **B. Mod_Rewrite (Apache) Example**  
```apache
RewriteEngine On
RewriteCond %{REQUEST_URI} ^/api/collect [NC]  
RewriteRule ^(.*)$ http://TEAM_SERVER_IP:80/$1 [P]  
```
- Only forward specific paths (e.g., `/api/collect`) to avoid suspicion.  

### **C. Domain Fronting (If Still Possible)**  
- Use a trusted CDN (e.g., Azure, AWS) to mask traffic.  
- **Note**: Major providers have patched this, but some edge cases may work.  

---

## **4. Post-Exploitation (If You Reach the Real Server)**  
Once you bypass Cloudflare:  
- **Scan for Open Ports** (avoid Cloudflare’s filtered ones).  
- **Exploit Directly** (e.g., SSH brute-force, unpatched web apps).  
- **Pivot Inside** (if it’s an internal asset).  

---

### **OPSEC Considerations**  
- **Avoid Aggressive Scans** (Cloudflare may blacklist your IP).  
- **Use Residential Proxies** (to blend in with legit traffic).  
- **Log Cleanup** (if you breach the backend, erase traces).  

---

### **Final Thoughts**  
Bypassing Cloudflare requires **patience, OSINT, and creative evasion techniques**. For red team engagements, document each step to show the client how an attacker could slip past their defenses.  


