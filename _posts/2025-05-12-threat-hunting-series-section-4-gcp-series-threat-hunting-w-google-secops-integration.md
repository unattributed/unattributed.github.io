---
layout: post
title: "Threat Hunting Primer - Section 4: GCP Primer -Threat Hunting w/ Google SecOps Integration"
date: 2025-05-12
author: unattributed
categories: [threat-hunting, gcp]
tags: [threat-hunting, gcp]
---

# GCP Cloud Threat Hunting

Google Cloud Platform (GCP) offers high-fidelity logging and native security tools through services like Security Command Center (SCC) and Google Security Operations (formerly Chronicle). These tools, coupled with threat data from VPC Flow Logs and IAM audit trails, provide a powerful foundation for threat hunting.

---

## Key Security and Observability Tools

<table>
  <thead>
    <tr><th>Service</th><th>Description</th><th>Threat Hunting Use Cases</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Cloud Audit Logs</strong></td>
      <td>Captures administrative and API activities</td>
      <td>Detect unauthorized policy changes, privilege escalations</td>
    </tr>
    <tr>
      <td><strong>VPC Flow Logs</strong></td>
      <td>Monitors network traffic to/from instances</td>
      <td>Identify beaconing, lateral movement, data exfiltration</td>
    </tr>
    <tr>
      <td><strong>Security Command Center (SCC)</strong></td>
      <td>Unified view of misconfigurations, vulnerabilities, and threats</td>
      <td>Monitor for public buckets, overly permissive IAM, exposed APIs</td>
    </tr>
    <tr>
      <td><strong>Google Security Operations (SecOps)</strong></td>
      <td>SIEM and threat intelligence platform</td>
      <td>Correlate indicators across time and assets</td>
    </tr>
    <tr>
      <td><strong>Cloud Functions</strong></td>
      <td>Serverless event-driven functions</td>
      <td>Execute detection logic at scale, integrate alerting pipelines</td>
    </tr>
  </tbody>
</table>

---

## MITRE ATT&CK Mapping (GCP)

<table>
  <thead>
    <tr><th>Tactic</th><th>Technique</th><th>GCP Source</th><th>Detection Strategy</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Privilege Escalation</td>
      <td>T1078 - Valid Accounts</td>
      <td>Cloud Audit Logs</td>
      <td>Detect 'setIamPolicy' on high-priv roles (e.g., Owner)</td>
    </tr>
    <tr>
      <td>Defense Evasion</td>
      <td>T1070 - Indicator Removal</td>
      <td>Cloud Logging</td>
      <td>Disabled logging or missing events</td>
    </tr>
    <tr>
      <td>Command & Control</td>
      <td>T1071 - Application Layer Protocol</td>
      <td>VPC Flow Logs</td>
      <td>Traffic to uncommon domains or rare geos</td>
    </tr>
  </tbody>
</table>

---

## Example: Detect GCP IAM Policy Escalation

<div style="position:relative;">
  <button onclick="copyCode('code7')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code7', 'gcp_iam_policy_alert.json')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code7" style="background:#1e1e1e;color:#dcdcdc;padding:1em;overflow-x:auto;white-space:pre-wrap;"><code>
resource.type="gce_instance"
logName="projects/your-project/logs/cloudaudit.googleapis.com%2Factivity"
protoPayload.methodName="SetIamPolicy"
protoPayload.serviceData.policyDelta.bindingDeltas.action="ADD"
protoPayload.serviceData.policyDelta.bindingDeltas.role="roles/owner"
</code></pre>

---

## Elastic AI Integration (GCP)

Elastic Agent can subscribe to Pub/Sub topics that export logs from:

- **Cloud Audit Logs**
- **VPC Flow Logs**
- **SCC Findings**

These logs are transformed into ECS format and ingested into Kibana dashboards or automated detection pipelines.

---

## Suggested GCP Hunting Indicators

<table>
  <thead>
    <tr><th>Behavior</th><th>Service</th><th>Query Example</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Excessive privilege grants</td>
      <td>Audit Logs</td>
      <td>methodName="SetIamPolicy" role="roles/owner"</td>
    </tr>
    <tr>
      <td>Unusual outbound DNS</td>
      <td>VPC Flow Logs</td>
      <td>dest.port=53 AND dest.domain NOT IN known_domains</td>
    </tr>
    <tr>
      <td>Public GCS bucket creation</td>
      <td>Cloud Audit Logs</td>
      <td>storage.setIamPolicy with 'allUsers'</td>
    </tr>
  </tbody>
</table>

---

## Serverless Threat Detection with Cloud Functions

Use GCP Cloud Functions to automate alerts and remediation.

<div style="position:relative;">
  <button onclick="copyCode('code8')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code8', 'cloud_function_alert.py')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code8" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
def detect_policy_change(event, context):
    if "SetIamPolicy" in event['protoPayload']['methodName']:
        if "roles/owner" in event['protoPayload']['serviceData']
            ['policyDelta']['bindingDeltas'][0]['role']:
            alert("Privilege escalation detected in GCP")
</code></pre>