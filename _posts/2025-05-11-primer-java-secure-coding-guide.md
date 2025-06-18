---
layout: post
title: "Primer - Java Secure Coding Guide"
date: 2025-05-11
author: unattributed
categories: [java]
tags: [secure-coding, java, code-review]
---

# unattributed Guide to Java Secure Coding 

## Table of Contents
- [unattributed Guide to Java Secure Coding](#unattributed-guide-to-java-secure-coding)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Core Security Principles](#core-security-principles)
    - [1. Fundamental Design Principles](#1-fundamental-design-principles)
    - [2. Input Validation (Oracle INPUT-1)](#2-input-validation-oracle-input-1)
  - [CWE Top 25 Mitigations](#cwe-top-25-mitigations)
    - [Critical Web Application Risks](#critical-web-application-risks)
    - [System-Level Risks](#system-level-risks)
  - [IDE Security Configuration](#ide-security-configuration)
    - [Visual Studio Code](#visual-studio-code)
    - [IntelliJ IDEA](#intellij-idea)
    - [Eclipse IDE](#eclipse-ide)
  - [Secure Development Workflows](#secure-development-workflows)
    - [Pre-Commit Hooks](#pre-commit-hooks)
    - [CI/CD Pipeline](#cicd-pipeline)
  - [Advanced Security Techniques](#advanced-security-techniques)
    - [1. Cryptographic Controls](#1-cryptographic-controls)
    - [2. Memory Safety](#2-memory-safety)
    - [3. Secure Serialization](#3-secure-serialization)
  - [Security Verification Checklists](#security-verification-checklists)
    - [Code Review Checklist](#code-review-checklist)
    - [Production Readiness Audit](#production-readiness-audit)
  - [References and Attribution](#references-and-attribution)

## Introduction

This guide synthesizes Oracle's Secure Coding Guidelines for Java SE (v10.0, May 2023), MITRE's CWE Top 25, and modern secure development practices into a comprehensive technical resource. It provides senior developers and security professionals with:

- Actionable secure coding patterns
- IDE-specific security configurations
- Automated verification techniques
- Reference implementations for critical security controls

*"To minimize the likelihood of security vulnerabilities caused by programmer error, Java developers should adhere to recommended coding guidelines."* - Oracle Secure Coding Guidelines

## Core Security Principles

### 1. Fundamental Design Principles

**Principle of Least Privilege (Oracle FUNDAMENTALS-3)**
```java
// Secure service design
public final class PaymentService {
    private final PaymentProcessor processor;
    
    @RolesAllowed("PAYMENT_ADMIN")
    public void processPayment(PaymentRequest request) {
        validateRequest(request);
        processor.charge(request);
    }
    
    // Private constructor prevents instantiation
    private PaymentService(PaymentProcessor processor) {
        this.processor = processor;
    }
}
```

**Immutable Data Objects (Oracle MUTABLE-1)**
```java
public final class UserCredentials {
    private final byte[] passwordHash;
    private final byte[] salt;
    
    public UserCredentials(byte[] password, byte[] salt) {
        this.passwordHash = Arrays.copyOf(password, password.length);
        this.salt = Arrays.copyOf(salt, salt.length);
    }
    
    // No setters, defensive copies on getters
    public byte[] getPasswordHash() {
        return Arrays.copyOf(passwordHash, passwordHash.length);
    }
}
```

### 2. Input Validation (Oracle INPUT-1)

**Comprehensive Validation Framework**
```java
// Jakarta Bean Validation 3.0 + Custom Constraints
public class UserInput {
    @NotBlank @Size(max=100)
    private String name;
    
    @Email
    private String email;
    
    @Pattern(regexp="^[a-zA-Z0-9_\\-]{8,20}$")
    private String username;
    
    @SafeHTML
    private String bio;
}

// Custom validator example
@Constraint(validatedBy = SafeHtmlValidator.class)
public @interface SafeHTML {
    String message() default "Unsafe HTML content";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}
```

## CWE Top 25 Mitigations

### Critical Web Application Risks

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey;">CWE</th>
      <th style="border: 1px solid lightgrey;">Risk</th>
      <th style="border: 1px solid lightgrey;">Java Mitigation</th>
      <th style="border: 1px solid lightgrey;">Verification</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;"><a href="https://cwe.mitre.org/data/definitions/89.html">CWE-89</a></td>
      <td style="border: 1px solid lightgrey;">SQL Injection</td>
      <td style="border: 1px solid lightgrey;">
        <!-- Add Java mitigation content here -->
      </td>
      <td style="border: 1px solid lightgrey;">
        <!-- Add verification content here -->
      </td>
    </tr>
  </tbody>
</table>

```java
// JPA Criteria API
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<User> q = cb.createQuery(User.class);
q.where(cb.equal(
    root.get("username"), 
    cb.parameter(String.class, "user")));
```

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey;">CWE</th>
      <th style="border: 1px solid lightgrey;">Risk</th>
      <th style="border: 1px solid lightgrey;">Java Mitigation</th>
      <th style="border: 1px solid lightgrey;">Verification</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;"><a href="https://cwe.mitre.org/data/definitions/79.html">CWE-79</a></td>
      <td style="border: 1px solid lightgrey;">XSS</td>
      <td style="border: 1px solid lightgrey;">
        - Use OWASP Java Encoder<br>
        - Validate and sanitize user input
      </td>
      <td style="border: 1px solid lightgrey;">
        - SonarQube Rule S3649<br>
        - SpotBugs SQLI detector
      </td>
    </tr>
  </tbody>
</table>


```java
// OWASP Java Encoder
String safeOutput = Encode.forHtmlContent(untrustedInput);
```

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey;">Area</th>
      <th style="border: 1px solid lightgrey;">Check</th>
      <th style="border: 1px solid lightgrey;">Tool</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;">Web Security</td>
      <td style="border: 1px solid lightgrey;">ZAP Active Scan</td>
      <td style="border: 1px solid lightgrey;">Check CSP headers</td>
    </tr>
  </tbody>
</table>


### System-Level Risks

**CWE-502: Unsafe Deserialization**
```java
// Java 17 Serialization Filter
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "maxdepth=10;maxarray=1000;!org.apache.commons.collections4.*"
);

try (ObjectInputStream ois = new ObjectInputStream(input)) {
    ois.setObjectInputFilter(filter);
    return (Data) ois.readObject();
}
```

**CWE-125: Buffer Overflow**
```java
// Java 16 Memory Access API
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = MemorySegment.allocateNative(100, session);
    // Bounds-checked access
    int value = segment.get(ValueLayout.JAVA_INT, 0);
}
```

## IDE Security Configuration

### Visual Studio Code

**Security Extensions:**
1. **SonarLint**
   ```json
   {
     "sonarlint.ls.java.extraArgs": [
       "-Dsonar.java.source=17",
       "-Dsonar.security.audit=true"
     ]
   }
   ```
2. **OWASP Dependency Check Task**
   ```json
   {
     "type": "shell",
     "command": "mvn org.owasp:dependency-check:check",
     "problemMatcher": "$dependency-check"
   }
   ```

### IntelliJ IDEA

**Security Analysis Setup:**
1. **Inspection Profile**
   ```xml
   <profile name="Security Audit">
     <inspection_tool class="SqlInjection" enabled="true" level="ERROR"/>
     <inspection_tool class="UnsafeDeserialization" enabled="true" level="ERROR"/>
   </profile>
   ```
2. **CodeQL Integration**
   ```bash
   codeql database create java-secure --language=java \
     --command="mvn clean install"
   ```

### Eclipse IDE

**Secure Development Configuration:**
1. **FindSecBugs Setup**
   ```xml
   <buildCommand>
     <name>edu.umd.cs.findbugs.plugin.eclipse.findbugsBuilder</name>
     <arguments>
       <dictionary>
         <key>securityOnly</key>
         <value>true</value>
       </dictionary>
     </arguments>
   </buildCommand>
   ```
2. **ESAPI Validation**
   ```java
   ESAPI.validator().setValidator(
     new DefaultValidator(ESAPI.securityConfiguration())
       .setMaximumInputLength(256)
       .setAllowNull(false)
   );
   ```

## Secure Development Workflows

### Pre-Commit Hooks

```bash
#!/bin/sh
# Reject commits with security anti-patterns
git diff --cached | grep -E \
  'ObjectInputStream|Runtime\.exec|ProcessBuilder' && \
  echo "SECURITY REJECT: Dangerous pattern detected" && exit 1
```

### CI/CD Pipeline

```yaml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: OWASP Dependency Check
        run: mvn org.owasp:dependency-check:check
      - name: SAST Analysis
        uses: github/codeql-action/analyze@v2
        with:
          languages: java
          queries: security-and-quality
      - name: DAST Scan
        uses: zaproxy/action-full-scan@v0.3.0
        with:
          target: 'http://localhost:8080'
```

## Advanced Security Techniques

### 1. Cryptographic Controls

**Secure Key Handling (CWE-320)**
```java
// Java KeyStore API with proper protection
KeyStore ks = KeyStore.getInstance("PKCS12");
try (InputStream is = Files.newInputStream(keystorePath)) {
    ks.load(is, password);
}

Key key = ks.getKey("alias", keyPassword);
if (key instanceof SecretKey secretKey) {
    Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
    cipher.init(Cipher.ENCRYPT_MODE, secretKey);
}
```

### 2. Memory Safety

**Foreign Memory API (Java 16+)**
```java
try (MemorySession session = MemorySession.openConfined()) {
    MemorySegment segment = MemorySegment.allocateNative(100, session);
    // Type-safe access
    segment.set(ValueLayout.JAVA_INT, 0, 42);
    int value = segment.get(ValueLayout.JAVA_INT, 0);
}
```

### 3. Secure Serialization

**JEP 415: Context-Specific Filters**
```java
ObjectInputFilter.Config.setSerialFilterFactory((info) -> {
    if (info.serialClass() != null && 
        info.serialClass().getName().startsWith("com.safe.")) {
        return ObjectInputFilter.Status.ALLOWED;
    }
    return ObjectInputFilter.Status.REJECTED;
});
```

## Security Verification Checklists

### Code Review Checklist

```markdown
- [ ] **Input Validation**
  - [ ] All entry points validate CWE-20
  - [ ] Regex anchors used (CWE-777)
  - [ ] Custom validators for business logic

- [ ] **Cryptography**
  - [ ] No custom algorithms (CWE-327)
  - [ ] Proper IV/nonce usage (CWE-329)
  - [ ] Key rotation implemented

- [ ] **Error Handling**
  - [ ] No system details leaked (CWE-209)
  - [ ] Finalizers not relied upon (CWE-586)
```

### Production Readiness Audit

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey;">Area</th>
      <th style="border: 1px solid lightgrey;">Check</th>
      <th style="border: 1px solid lightgrey;">Tool</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;">Dependencies</td>
      <td style="border: 1px solid lightgrey;">No known vulnerabilities</td>
      <td style="border: 1px solid lightgrey;">OWASP DC</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;">APIs</td>
      <td style="border: 1px solid lightgrey;">Rate limiting enabled</td>
      <td style="border: 1px solid lightgrey;">ZAP</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey;">Config</td>
      <td style="border: 1px solid lightgrey;">No default credentials</td>
      <td style="border: 1px solid lightgrey;">Checkspec</td>
    </tr>
  </tbody>
</table>

## References and Attribution

1. **Oracle Secure Coding Guidelines for Java SE**  
   Document version: 10.0, May 2023  
   [https://www.oracle.com/java/technologies/javase/seccodeguide.html](https://www.oracle.com/java/technologies/javase/seccodeguide.html)

2. **MITRE CWE Top 25 Most Dangerous Software Weaknesses**  
   2023 Edition  
   [https://cwe.mitre.org/top25/](https://cwe.mitre.org/top25/)

3. **OWASP Java Secure Coding Practices**  
   [https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

4. **Java Security Evolution**  
   Inside Java Security Articles  
   [https://inside.java/tag/security/](https://inside.java/tag/security/)

*unattributed* _makes zero promises_ that this document will be periodically updated to reflect new threats and defensive techniques, as always keep hunting.

[🔝 Back to Top](#unattributed-guide-to-java-secure-coding)