---
layout: post
title: "Threat Hunting Primer - Azure IOC Detection Cobalt Strike"
date: 2025-05-12
author: unattributed
categories: [threat-hunting, cobaltstrike, azure]
tags: [threat-hunting, azure, cobaltstrike]
---

# **Azure Threat Hunting & IOC Detection**  

## **Introduction to Azure Threat Hunting**  
Azure threat hunting is a **proactive security practice** that involves searching for cyber threats that may have bypassed existing security controls. Microsoft Azure provides a suite of tools to **detect, investigate, and respond** to security incidents using **Indicators of Compromise (IOCs)** and behavioral analytics.  

---

## **Key Azure Services for Threat Hunting**  

### **1. Microsoft Defender for Cloud**  
Microsoft Defender for Cloud provides **unified security management** and **advanced threat protection** across hybrid cloud workloads.  

#### **Key Components & Functions**  

<table>
    <thead>
        <tr>
            <th>Component</th>
            <th>Function</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Cloud Security Posture Management (CSPM)</strong></td>
            <td>Continuously assesses security posture and provides compliance benchmarks (e.g., CIS, NIST).</td>
        </tr>
        <tr>
            <td><strong>Microsoft Defender for Servers</strong></td>
            <td>Protects VMs with EDR (Endpoint Detection & Response) and vulnerability assessments.</td>
        </tr>
        <tr>
            <td><strong>Microsoft Defender for SQL</strong></td>
            <td>Detects SQL injection attacks, suspicious database logins, and data exfiltration.</td>
        </tr>
        <tr>
            <td><strong>Microsoft Defender for Containers</strong></td>
            <td>Scans Kubernetes clusters for misconfigurations and runtime threats.</td>
        </tr>
        <tr>
            <td><strong>Threat Intelligence Alerts</strong></td>
            <td>Correlates IOCs (malicious IPs, domains, hashes) with internal telemetry.</td>
        </tr>
    </tbody>
</table>
```

**Example Threat Detection in Defender for Cloud:**  
- Detects **brute-force attacks** on Azure VMs via failed RDP/SSH logins.  
- Alerts on **suspicious process execution** (e.g., PowerShell downloading malware).  
- Identifies **anomalous network traffic** (e.g., connections to known C2 servers).  

---

### **2. Microsoft Sentinel (Cloud-Native SIEM & SOAR)**  
Microsoft Sentinel is a **scalable SIEM** that uses **AI-driven analytics** and **custom hunting queries** to detect threats.  

#### **AI & Machine Learning in Sentinel**  
- **Anomaly Detection**: Identifies unusual login patterns (e.g., impossible travel).  
- **Behavioral Analytics**: Uses **UEBA (User & Entity Behavior Analytics)** to detect insider threats.  
- **Fusion Detection**: Correlates multiple low-severity alerts into high-confidence incidents.  

#### **Custom Hunting Queries (KQL Examples)**  

**Example 1: Hunting for Cobalt Strike Beacon (Lateral Movement IOC)**  
```kusto
// Detect Cobalt Strike default C2 ports (e.g., 50050)  
CommonSecurityLog  
| where DeviceVendor == "Microsoft"  
| where DestinationPort in (50050, 4444, 53)  
| where Activity contains "beacon" or ProcessName contains "beacon"  
| summarize count() by SourceIP, DestinationIP, DestinationPort  
```

**Example 2: Detecting PsExec Lateral Movement**  
```kusto
// Look for PsExec usage (common in lateral movement)  
SecurityEvent  
| where EventID == 4688 // Process creation  
| where ProcessName contains "PsExec" or CommandLine contains "PsExec"  
| project TimeGenerated, Computer, Account, ProcessName, CommandLine  
```

**Example 3: Suspicious Scheduled Task Creation (Persistence)**  
```kusto
// Hunt for malicious scheduled tasks  
SecurityEvent  
| where EventID == 4698 // Scheduled task creation  
| where SubjectUserName != "SYSTEM"  
| where TaskName contains "Update" or TaskName contains "Maintenance"  
| project TimeGenerated, Computer, TaskName, CommandLine  
```

---

### **3. Azure Monitor & Log Analytics for Threat Hunting**  
Azure Monitor collects logs from Azure resources, while **Log Analytics** enables deep investigation using **KQL queries**.  

#### **Configuration Steps**  
1. **Enable Diagnostic Logs** for:  
   - Azure Active Directory (sign-ins, audit logs)  
   - Azure VMs (Security Events, Sysmon)  
   - Network Security Groups (NSG Flow Logs)  
2. **Create a Log Analytics Workspace** and connect data sources.  
3. **Write KQL Queries** to hunt for threats.  

#### **Log Analytics Hunting Examples**  

**Example 1: Detecting Pass-the-Hash Attacks**  
```kusto
SecurityEvent  
| where EventID == 4624 // Successful logon  
| where LogonType == 3 // Network logon  
| where Account contains "$" // Checking machine accounts (common in PtH)  
| summarize count() by Account, SourceIP  
```

**Example 2: Hunting for DNS Tunneling (C2 Communication)**  
```kusto
// Look for long DNS queries (common in C2 tunneling)  
DnsEvents  
| where strlen(Query) > 50  
| where Query contains ".exe" or Query contains ".dll"  
| project TimeGenerated, Computer, Query, ClientIP  
```

**Example 3: Detecting Azure AD Backdoor Accounts**  
```kusto
SigninLogs  
| where ResultType == "0" // Successful logins  
| where AppDisplayName == "Office 365"  
| where UserPrincipalName endswith "#EXT#@tenant.onmicrosoft.com"  
| summarize count() by UserPrincipalName, IPAddress  
```

---

## **IOC Detection in Microsoft Sentinel (Lateral Movement Focus)**  

### **1. Detecting Cobalt Strike Beacon (Lateral Movement IOC)**  
Cobalt Strike is a popular **post-exploitation framework** used in ransomware attacks.  

**KQL Query to Detect Cobalt Strike C2 Traffic:**  
```kusto
// Look for Cobalt Strike default JA3/S hashes (malicious SSL fingerprints)  
let cobalt_strike_ja3 = dynamic(["72a589da586844d7f0818ce684948eea", "a0e9f5d64349fb13191bc781f81f42e1"]);  
AzureDiagnostics  
| where ResourceType == "APPLICATIONGATEWAYS"  
| where sslClientHello_ja3_hash in~ (cobalt_strike_ja3)  
| project TimeGenerated, sslClientHello_ja3_hash, clientIP_s  
```

**Detecting Cobalt Strike Process Injection:**  
```kusto
// Hunt for process hollowing (common in Cobalt Strike)  
SecurityEvent  
| where EventID == 4688 // Process creation  
| where ParentProcessName contains "explorer.exe"  
| where NewProcessName contains "rundll32.exe"  
| project TimeGenerated, Computer, ParentProcessName, NewProcessName  
```

---

## **Best Practices for Azure Threat Hunting**  
✅ **Centralize Logs** (Azure AD, NSG, VM logs in Log Analytics)  
✅ **Use MITRE ATT&CK Mappings** (Align queries with TTPs)  
✅ **Automate Response** (Sentinel Playbooks for auto-remediation)  
✅ **Leverage Threat Intel Feeds** (Integrate MISP, AlienVault OTX)  

---

## **Conclusion**  
Azure provides **Defender for Cloud, Sentinel, and Log Analytics** for **proactive threat hunting**. By using **KQL queries**, security teams can detect **IOCs like Cobalt Strike beacons, lateral movement, and credential dumping**. Continuous monitoring and AI-driven detections enhance security posture in hybrid environments.  

Would you like additional examples on **Azure AD attack detection** or **cloud-specific ransomware hunting**? 🚀