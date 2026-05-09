---
layout: post
title: "Primer - OSINT Guide"
date: 2025-05-12
author: unattributed
categories: [osint]
tags: [osint, kali, parrotos]
---

# **The OSINT Guide for Penetration Testers**: 
*Mapping ACME Corporation*  

---

## **Table of Contents**  
- [\*\*The OSINT Guide for Penetration Testers:](#the-osint-guide-for-penetration-testers)
  - [**Table of Contents**](#table-of-contents)
  - [**1. Introduction**](#1-introduction)
  - [**2. Corporate Reconnaissance**](#2-corporate-reconnaissance)
    - [**a) Domain \& Subdomain Enumeration**](#a-domain--subdomain-enumeration)
      - [**Example: Passive Enumeration (`theHarvester`)**](#example-passive-enumeration-theharvester)
      - [**Example: Active Bruteforcing (`Amass`)**](#example-active-bruteforcing-amass)
    - [**b) Shodan for Exposed Services**](#b-shodan-for-exposed-services)
  - [**3. People Discovery**](#3-people-discovery)
    - [**a) LinkedIn Scraping**](#a-linkedin-scraping)
    - [**b) Email Verification (`holehe`)**](#b-email-verification-holehe)
  - [**4. Product \& Technology Intelligence**](#4-product--technology-intelligence)
    - [**a) Wappalyzer \& BuiltWith**](#a-wappalyzer--builtwith)
    - [**b) CVE Search (`searchsploit`)**](#b-cve-search-searchsploit)
  - [**5. Social Media \& Customer Intelligence**](#5-social-media--customer-intelligence)
    - [**a) Twitter/X Scraping (`twint`)**](#a-twitterx-scraping-twint)
    - [**b) Instagram OSINT (`Osintgram`)**](#b-instagram-osint-osintgram)
  - [**6. Automating OSINT with Frameworks**](#6-automating-osint-with-frameworks)
    - [**a) SpiderFoot**](#a-spiderfoot)
    - [**b) recon-ng**](#b-recon-ng)
    - [**c) Maltego**](#c-maltego)
  - [**7. Commercial OSINT Providers**](#7-commercial-osint-providers)
  - [**8. OSINT Framework Categories**](#8-osint-framework-categories)
  - [**9. Conclusion**](#9-conclusion)

---

## **1. Introduction**  
Open-Source Intelligence (OSINT) is the foundation of effective penetration testing, red teaming, and vulnerability assessments. This guide demonstrates how to use **Kali Linux**, **Parrot OS**, and the **[OSINT Framework](https://www.osintframework.com/)** to gather intelligence on **ACME Corporation** (`www.acme.io`), a fictional company with:  
- **100 employees** (LinkedIn, Facebook, Instagram, X/Twitter, Bluesky, TikTok)  
- **Multiple products & web services**  
- **Public cloud infrastructure**  


We’ll cover:  
✔ **Corporate reconnaissance** (domains, IPs, cloud assets)  
✔ **People discovery** (employees, credentials, social media)  
✔ **Technology stack analysis** (CMS, APIs, CVEs)  
✔ **Automation with OSINT frameworks** (SpiderFoot, recon-ng, Maltego)  
✔ **Commercial OSINT tools** (Recorded Future, ZeroFOX)  

---

## **2. Corporate Reconnaissance**  

### **a) Domain & Subdomain Enumeration**  
**Tools:** `theHarvester`, `Amass`, `gobuster`  

#### **Example: Passive Enumeration (`theHarvester`)**  
```bash
theHarvester -d acme.io -b google,linkedin,duckduckgo -l 1000 -f acme_report.html
```  
**Output:**  
```plaintext
[*] Emails found: admin@acme.io, j.doe@acme.io  
[*] Subdomains: dev.acme.io, vpn.acme.io  
```  

#### **Example: Active Bruteforcing (`Amass`)**  
```bash
amass enum -d acme.io -brute -w /usr/share/wordlists/dns/all.txt
```  
**Findings:**  
- `legacy.acme.io` → Outdated web app (potential XSS)  
- `staging.acme.io` → Pre-production credentials  

---

### **b) Shodan for Exposed Services**  
**Tool:** `shodan-cli`  
```bash
shodan search org:"ACME Corporation" http.title:"login"
```  
**Findings:**  
- `104.21.33.72` → Exposed Admin Panel  
- `172.67.141.89` → Jenkins CI (default creds?)  

---

## **3. People Discovery**  

### **a) LinkedIn Scraping**  
**Tool:** `linkedin2username`  
```bash
python3 linkedin2username.py -c "ACME Corporation" -o employees.txt
```  
**Output (`employees.txt`):**  
```plaintext
jdoe  
ssmith  
```  

### **b) Email Verification (`holehe`)**  
```bash
holehe j.doe@acme.io
```  
**Findings:**  
- `j.doe@acme.io` leaked in LinkedIn breach (Password: `P@ssw0rd2021`)  

---

## **4. Product & Technology Intelligence**  

### **a) Wappalyzer & BuiltWith**  
**Findings:**  
- `www.acme.io` → WordPress 6.2 (CVE-2023-1234)  
- `api.acme.io` → Node.js/Express  

### **b) CVE Search (`searchsploit`)**  
```bash
searchsploit "WordPress 6.2"
```  
**Output:**  
```plaintext
WordPress 6.2 - XSS (CVE-2023-1234)  
```  

---

## **5. Social Media & Customer Intelligence**  

### **a) Twitter/X Scraping (`twint`)**  
```bash
twint -u @ACME_Corp --since 2024-01-01 -o tweets.csv
```  
**Findings:**  
- Employee tweet: "New API at `api.acme.io/v2`" → Attack surface  

### **b) Instagram OSINT (`Osintgram`)**  
```bash
python3 osintgram.py jdoe
```  
**Findings:**  
- Employee posts work laptop model (`Dell XPS 13`) → Spear phishing bait  

---

## **6. Automating OSINT with Frameworks**  

### **a) SpiderFoot**  
```bash
spiderfoot -l 127.0.0.1:5001  # Web UI scan for acme.io
```  
**Findings:**  
- Subdomains, emails, IP ranges  

### **b) recon-ng**  
```bash
recon-ng  
use recon/profiles-profiles/linkedin  
set SOURCE acme.io  
run  
```  
**Output:**  
```plaintext
[*] j.doe - Software Engineer @ ACME  
```  

### **c) Maltego**  
- Visual link analysis between domains, IPs, employees  

---

## **7. Commercial OSINT Providers**  

<table border="1">
    <thead>
        <tr>
            <th>Tool</th>
            <th>Use Case</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Recorded Future</strong></td>
            <td>Real-time threat intelligence</td>
        </tr>
        <tr>
            <td><strong>ZeroFOX</strong></td>
            <td>Social media threat detection</td>
        </tr>
        <tr>
            <td><strong>Intelligence X</strong></td>
            <td>Archived/deep web data</td>
        </tr>
    </tbody>
</table>

---

## **8. OSINT Framework Categories**  

<table border="1">  
  <thead>  
    <tr>  
      <th><strong>Category</strong></th>  
      <th><strong>Tools</strong></th>  
      <th><strong>Example Use</strong></th>  
    </tr>  
  </thead>  
  <tbody>  
    <tr><td>Email & Usernames</td><td>holehe, hunter.io</td><td>Find breached creds</td></tr>  
    <tr><td>Social Media</td><td>sherlock, twint</td><td>Scrape employee profiles</td></tr>  
    <!-- Full table in original content -->  
  </tbody>  
</table>  

---

## **9. Conclusion**  
This guide covered:  
- **Corporate footprinting** (domains, IPs, cloud)  
- **People discovery** (emails, social media, credentials)  
- **Automation with SpiderFoot/recon-ng/Maltego**  
- **Commercial tools (Recorded Future, ZeroFOX)**  

**Next Steps:**  
- Automate scans with cron jobs.  
- Correlate data in Maltego for attack paths.  

<span style="color:yellow;">
    This document will be expanded in subsequent posts to provide detailed demonstrations of OSINT data collection using open-source tools. It will also evaluate the effectiveness of various tools within the OSINT Framework.
</span>

--- 

[↑ Back to Top](#the-osint-guide-for-penetration-testers)