---
layout: post
title: "Burp Primer - Using WSTG and DVWA for WebApp elearning"
date: 2025-05-12
author: unattributed
categories: [webappsec]
tags: [webapp, burp, dvwa, owasp, owasp-wstg, owasp-top-10]
---

# Testing OWASP WSTG and OWASP Top 10 Vulnerabilities with Burp Suite Professional on DVWA

## Introduction

As part of web application security testing, Burp Suite Professional offers powerful tools like **Intruder** and **Repeater** for conducting in-depth vulnerability assessments. In this post, we’ll dive deeper into how these tools can be utilized to identify OWASP Top 10 vulnerabilities, focusing on advanced testing techniques with **Burp Suite's Intruder** and **Repeater** features. Additionally, we’ll reference useful open-source resources, such as the [Malicious PDF repository](https://github.com/jonaslejon/malicious-pdf) and [IntruderPayloads repository](https://github.com/1N3/IntruderPayloads), to enhance fuzz testing with known malicious payloads.

## Using Burp Suite's Intruder and Repeater Features

### 1. **Intruder: Automating Attacks and Fuzzing**

Burp Suite's **Intruder** tool is essential for automating attacks, specifically when testing for injection flaws, authentication bypasses, and other vulnerability types that require payload injection. It can be used to fuzz input fields with custom payloads to identify vulnerabilities such as **SQL Injection**, **XSS**, **Command Injection**, and others.

#### 1.1 **Setting Up Intruder**

Let’s walk through how to configure and use Burp Suite's **Intruder** for fuzzing inputs with malicious payloads:

1. **Intercepting the Request**:

   * Open Burp Suite and set up the proxy.
   * Navigate to the **Proxy** tab and ensure **Intercept** is turned on.
   * Visit the vulnerable **DVWA** page that you want to test (for example, the **SQL Injection** page).
   * Submit a form with user input, such as a username and password or a search query.
   * Burp Suite will intercept the HTTP request.

2. **Sending the Request to Intruder**:

   * Right-click on the intercepted request and select **Send to Intruder**.
   * Navigate to the **Intruder** tab, and you’ll see the request listed.

3. **Defining Payload Positions**:

   * Click on the **Positions** tab.
   * Burp Suite will automatically try to identify potential places where you can inject payloads, such as form fields or URL parameters. You can click **Clear** to remove any default positions and manually select positions by highlighting the parameters (e.g., user input fields).
   * Once you’ve selected a position, click **Add** to add it as a payload position.

4. **Choosing Payloads**:

   * Navigate to the **Payloads** tab.
   * Select **Payload Type**. You can choose from various predefined payloads like **Simple list**, **Numbers**, **Character stuffer**, etc.
   * For fuzzing **SQL Injection**, you can load a list of SQL injection payloads or, for **XSS**, use **JavaScript payloads**.
   * Here’s where you can leverage known malicious payloads from the following open-source repositories:

     * **[Malicious PDF Payloads](https://github.com/jonaslejon/malicious-pdf)**: This repository contains examples of malicious payloads designed for testing PDF-related vulnerabilities.
     * **[IntruderPayloads](https://github.com/1N3/IntruderPayloads)**: This collection includes various payloads for fuzz testing against SQL injection, XSS, command injection, and more. It’s a useful resource for testing known attack vectors.

5. **Starting the Attack**:

   * Once the payloads are set, click **Start attack**.
   * Burp Suite will automatically fuzz the input field with the defined payloads and capture the responses.
   * Pay close attention to the **Status** and **Length** of each response. For example, a change in the length of the response might indicate a successful injection.

6. **Analyzing Results**:

   * Once the attack completes, look at the responses for anomalies such as:

     * Successful SQL injection errors (e.g., database errors).
     * Reflected XSS payloads that trigger script execution.
     * Command injection errors or unexpected server responses.
   * Use these results to identify and verify potential vulnerabilities.

### 2. **Repeater: Manual Testing and Request Replay**

While **Intruder** is ideal for automating payload fuzzing, **Repeater** is perfect for manual testing of individual requests and responses. **Repeater** allows security professionals to modify and resend requests multiple times to test how the web application responds to different inputs.

#### 2.1 **Setting Up Repeater**

1. **Intercepting a Request**:

   * As with Intruder, start by intercepting a request in the **Proxy** tab.
   * Right-click the request and select **Send to Repeater**.

2. **Modifying the Request**:

   * Go to the **Repeater** tab.
   * You’ll see the intercepted request. Modify specific parameters, headers, or payloads manually.
   * For example, you can inject XSS payloads into a form input field or modify a URL parameter to test for SQL injection.

3. **Sending the Request**:

   * After modifying the request, click **Go** to send it.
   * The response from the server will appear below, allowing you to inspect the result.

4. **Replaying the Request**:

   * You can keep modifying and sending the request to test different payloads or configurations.

#### 2.2 **Examples of Using Repeater**

* **SQL Injection**: Modify the input fields to test different SQL injection payloads manually (e.g., `' OR '1'='1`).
* **XSS**: Modify form parameters or URL parameters with XSS payloads (e.g., `<script>alert('XSS')</script>`).
* **Command Injection**: Try injecting OS commands into input fields to test for command injection vulnerabilities.

**Repeater** allows you to fine-tune your testing by observing the server’s response to each request modification.

### 3. **Fuzzing with Known Malicious Payloads**

As mentioned earlier, using payload lists from trusted repositories like **Malicious PDF** and **IntruderPayloads** enhances the fuzzing process and can help you identify vulnerabilities that are commonly missed.

Here’s how to integrate them into your Burp Suite testing:

#### 3.1 **Using the Malicious PDF Repository**

The **Malicious PDF repository** provides known malicious payloads used to test PDF vulnerabilities, which may be applicable to web applications that process PDF files.

1. Clone the repository to your machine:

   ```bash
   git clone https://github.com/jonaslejon/malicious-pdf.git
   ```

2. Identify the types of payloads you want to test (e.g., **JavaScript-based PDF exploits**).

3. Use Burp Suite’s **Intruder** tool to fuzz any file-upload functionality or parameters that may process PDFs.

#### 3.2 **Using the IntruderPayloads Repository**

The **IntruderPayloads** repository provides a wide variety of payloads for testing SQL injection, XSS, and command injection, which can be directly used in Burp Suite’s **Intruder**.

1. Clone the **IntruderPayloads** repository:

   ```bash
   git clone https://github.com/1N3/IntruderPayloads.git
   ```

2. Select a payload category relevant to your tests (e.g., SQL injection payloads).

3. In Burp Suite, load the payloads into **Intruder**:

   * In the **Payloads** tab, click **Load** and select the payload file from the repository.
   * Launch the attack as described above.

## Conclusion

Burp Suite Professional’s **Intruder** and **Repeater** tools are invaluable for conducting thorough web application security tests. **Intruder** automates the process of injecting payloads to fuzz input fields, while **Repeater** allows for manual request modification and response analysis. By leveraging known malicious payloads from repositories like **Malicious PDF** and **IntruderPayloads**, you can effectively test for a wide range of vulnerabilities, including SQL Injection, XSS, and more.

This combination of Burp Suite and additional resources like **Malicious PDF** and **IntruderPayloads** ensures that your vulnerability testing is comprehensive and efficient, helping to identify and mitigate vulnerabilities in web applications more effectively.

---

This expanded guide should provide clear instructions on using **Burp Suite's Intruder** and **Repeater**, as well as how to incorporate known malicious payloads from trusted repositories to enhance the fuzzing and testing process.

**Note**: This article will spawn a large series of articles on Web Application Penetration Testing using Burp, Zap, and other tools

[↑ Back to Top](#testing-owasp-wstg-and-owasp-top-10-vulnerabilities-with-burp-suite-professional-on-dvwa)