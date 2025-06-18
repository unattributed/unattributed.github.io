---
layout: post
title: "Threat Hunting Primer - Section 3: Azure Primer - Azure elements & KQL Deep Dive"
date: 2025-05-12
author: unattributed
categories: [threat-hunting, azure]
tags: [threat-hunting, azure]
---

# Azure Cloud Threat Hunting

Microsoft Azure provides extensive logging, endpoint, and identity telemetry integrated with their Defender and Sentinel platforms. With rich support for Kusto Query Language (KQL), threat hunters can extract detailed insights from cloud activity and behavioral anomalies.

---

## Key Security and Observability Tools

<table>
  <thead>
    <tr><th>Service</th><th>Description</th><th>Threat Hunting Use Cases</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Microsoft Defender XDR</strong></td>
      <td>Cross-platform security insights (identity, endpoint, cloud)</td>
      <td>Advanced threat correlation across devices, services, and identities</td>
    </tr>
    <tr>
      <td><strong>Azure Monitor / Log Analytics</strong></td>
      <td>Unified platform for logs and metrics</td>
      <td>Query and visualize log data using KQL for detections</td>
    </tr>
    <tr>
      <td><strong>Azure AD Sign-In Logs</strong></td>
      <td>Tracks sign-in activity across users and services</td>
      <td>Brute-force attempts, impossible travel, MFA bypass</td>
    </tr>
    <tr>
      <td><strong>Azure Activity Logs</strong></td>
      <td>Tracks configuration and management actions in Azure</td>
      <td>Detect unauthorized resource manipulation</td>
    </tr>
    <tr>
      <td><strong>Azure Key Vault</strong></td>
      <td>Securely stores secrets, certificates, and keys</td>
      <td>Alert on excessive access or failed retrievals</td>
    </tr>
  </tbody>
</table>

---

## Deep Dive: KQL for Threat Hunting

Kusto Query Language (KQL) is used in Azure Monitor, Log Analytics, and Microsoft Sentinel for querying large datasets.

---

### Example 1: Detect Multiple Failed Logins

<div style="position:relative;">
  <button onclick="copyCode('code4')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code4', 'failed_login_kql.txt')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code4" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
SigninLogs
| where ResultType == 50074
| summarize FailedAttempts = count() by IPAddress, 
|  bin(TimeGenerated, 1h)
| where FailedAttempts > 10
</code></pre>

---

### Example 2: Impossible Travel Detection

<div style="position:relative;">
  <button onclick="copyCode('code5')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code5', 'impossible_travel_kql.txt')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code5" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
SigninLogs
| extend timestamp = TimeGenerated, 
         location = tostring(Location), 
         user = UserPrincipalName
| summarize makeset(location), 
            min(timestamp), 
            max(timestamp) by user
| where array_length(makeset_location) > 1
</code></pre>

---

## MITRE ATT&CK Mapping (Azure)

<table>
  <thead>
    <tr><th>Tactic</th><th>Technique</th><th>Azure Source</th><th>Detection Strategy</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Credential Access</td>
      <td>T1110 - Brute Force</td>
      <td>Azure AD Sign-In Logs</td>
      <td>Multiple failed sign-in attempts from the same IP</td>
    </tr>
    <tr>
      <td>Lateral Movement</td>
      <td>T1021.002 - SMB/Remote Desktop</td>
      <td>Defender for Endpoint</td>
      <td>Multiple device logins from single account within a short time</td>
    </tr>
    <tr>
      <td>Persistence</td>
      <td>T1098 - Account Manipulation</td>
      <td>Activity Logs</td>
      <td>Admin rights assignment to new accounts</td>
    </tr>
    <tr>
      <td>Exfiltration</td>
      <td>T1048 - Exfiltration Over Alternative Protocol</td>
      <td>Log Analytics + Network Watcher</td>
      <td>Traffic to unknown external hosts via non-standard ports</td>
    </tr>
  </tbody>
</table>

---

## Elastic AI Integration (Azure)

Azure logs can be exported using the **Azure Monitor Diagnostic Settings** into Event Hub or Logstash pipelines. Elastic Agent or Beats can ingest this directly into your SIEM.

Example rule for detecting privileged escalation in Azure AD:

<div style="position:relative;">
  <button onclick="copyCode('code6')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code6', 'elastic_azuread_admin.json')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "azure.auditlogs.operationName": "Add member to role" } },
        { "match": { "azure.auditlogs.properties.targetRole": "Global Administrator" } }
      ]
    }
  }
}
```

---

## Suggested Azure Hunting Queries

<table>
  <thead>
    <tr><th>Behavior</th><th>Service</th><th>KQL or Detection</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Excessive Key Vault reads</td>
      <td>Azure Monitor</td>
      <td>Monitor VaultAccessLogs for high frequency</td>
    </tr>
    <tr>
      <td>Disabled MFA detection</td>
      <td>Sign-In Logs</td>
      <td>ResultType 50140 or sign-ins without MFA used</td>
    </tr>
    <tr>
      <td>Audit log tampering</td>
      <td>Activity Logs</td>
      <td>DisableAuditLogs or Remove-DiagnosticSetting events</td>
    </tr>
  </tbody>
</table>