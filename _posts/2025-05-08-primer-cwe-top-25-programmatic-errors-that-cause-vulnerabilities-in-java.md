---
layout: post
title: "CWE Top 25: Programmatic Errors That Cause Vulnerabilities in Java"
date: 2025-05-08
author: unattributed
categories: [java]
tags: [cwe, java, secure-code, sast, dast, code-review]
---

# CWE Top 25 
**How they manifest in Java applications**

## Overview

This document explores the CWE Top 25 Most Dangerous Software Weaknesses, focusing on how they manifest in Java applications. It's tailored for senior software developers and cybersecurity contractors engaged in secure software development, static application security testing (SAST), and dynamic application security testing (DAST).

We provide examples, detection strategies, and remediation recommendations using both open-source and commercial tools, including Burp Suite Professional.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Tools Overview](#tools-overview)
3. [CWE Top 25 in Java: Examples, Detection, and Remediation](#cwe-top-25-in-java)
4. [Conclusion](#conclusion)

---

## Introduction

The CWE Top 25 is published annually by MITRE and highlights the most prevalent and impactful software weaknesses. In Java, many of these weaknesses result from improper input handling, insecure object manipulation, and flawed logic that can be exploited.

---

## Tools Overview

### Open-Source SAST Tools

* **SpotBugs with FindSecBugs plugin**
* **PMD Security Rules**
* **OWASP Dependency-Check**

### Commercial SAST Tools

* **Checkmarx**
* **Fortify Static Code Analyzer**
* **Veracode Static Analysis**

### Open-Source DAST Tools

* **OWASP ZAP**

### Commercial DAST Tools

* **Burp Suite Professional**
* **Acunetix**
* **AppScan**

---

## CWE Top 25 in Java

Below are selected CWEs from the Top 25 with Java-specific insights.

### CWE-79: Improper Neutralization of Input During Web Page Generation (XSS)

**Java Example:**

```java
out.println("<div>" + request.getParameter("user") + "</div>");
```

**Detection:**

* **SAST:** SpotBugs with FindSecBugs will flag unencoded output.
* **DAST:** Burp Suite Pro's Active Scan will detect reflected and stored XSS.

**Remediation:**

* Use output encoding with libraries like OWASP Java Encoder.

```java
out.println("<div>" + Encode.forHtml(request.getParameter("user")) + "</div>");
```

---

### CWE-89: SQL Injection

**Java Example:**

```java
String query = "SELECT * FROM users WHERE username='" + user + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

**Detection:**

* **SAST:** Checkmarx and Fortify detect string concatenation in SQL.
* **DAST:** Burp Suite Pro can detect SQL injection through automated payloads.

**Remediation:**

* Use Prepared Statements:

```java
PreparedStatement ps = connection.prepareStatement("SELECT * FROM users WHERE username=?");
ps.setString(1, user);
ResultSet rs = ps.executeQuery();
```

---

### CWE-22: Path Traversal

**Java Example:**

```java
File file = new File("/data/" + request.getParameter("file"));
```

**Detection:**

* **SAST:** PMD and Fortify identify unsafe file concatenation.
* **DAST:** Burp Suite Intruder can test for `../` traversal.

**Remediation:**

* Validate and normalize paths with `Paths.get().normalize()` and restrict access to known directories.

---

### CWE-306: Missing Authentication for Critical Function

**Java Example:**

```java
@WebServlet("/admin/deleteUser")
public class DeleteUserServlet extends HttpServlet {
  protected void doPost(HttpServletRequest request, HttpServletResponse response) {
    // No authentication check
  }
}
```

**Detection:**

* **SAST:** Checkmarx flags servlet methods lacking access control.
* **DAST:** Burp Suite Pro identifies admin endpoints with no auth.

**Remediation:**

* Enforce access control checks using frameworks (Spring Security, JAAS).

---

### CWE-502: Deserialization of Untrusted Data

**Java Example:**

```java
ObjectInputStream in = new ObjectInputStream(socket.getInputStream());
Object obj = in.readObject();
```

**Detection:**

* **SAST:** Fortify identifies use of Java serialization APIs.
* **DAST:** Burp Suite's Collaborator helps test for deserialization vulnerabilities.

**Remediation:**

* Avoid Java serialization; prefer JSON or XML with strict schemas.
* Use whitelisting in `ObjectInputFilter` (Java 9+).

---

## Conclusion

Preventing the CWE Top 25 in Java applications requires a proactive approach to secure coding, combined with rigorous testing using SAST and DAST tools. Leverage both open-source and commercial solutions, and incorporate secure development practices early in the SDLC.

For complete CWE descriptions and more Java-specific guidance, visit the [MITRE CWE website](https://cwe.mitre.org/).

---

**Disclaimer:** This content is educational and should not be solely relied upon for secure application development. Always perform comprehensive security reviews and use multiple testing layers.

[↑ Back to Top](#cwe-top-25)