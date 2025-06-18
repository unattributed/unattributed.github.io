---
layout: post
title: "Threat Hunting Primer - Section 2: AWS Primer - Threat Hunting Products"
date: 2025-05-12
author: unattributed
categories: [threat-hunting]
tags: [threat-hunting, aws]
---

# AWS Cloud Threat Hunting

AWS provides a rich set of security and observability services across identity, compute, networking, and serverless layers. Threat hunters can ingest telemetry from these services into Elastic AI or other SIEM/SOAR platforms, and build custom Lambda-based detectors for real-time analytics.

---

## Key Security and Observability Tools

<table>
  <thead>
    <tr><th>Service</th><th>Description</th><th>Threat Hunting Use Cases</th></tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>CloudTrail</strong></td>
      <td>Captures all API calls and events within AWS</td>
      <td>Detect privilege escalation, IAM changes, new service usage</td>
    </tr>
    <tr>
      <td><strong>VPC Flow Logs</strong></td>
      <td>Logs IP traffic going to/from network interfaces</td>
      <td>Track lateral movement, detect beaconing, data exfiltration</td>
    </tr>
    <tr>
      <td><strong>GuardDuty</strong></td>
      <td>ML-based threat detection engine</td>
      <td>Monitor for compromised instances, unusual login locations</td>
    </tr>
    <tr>
      <td><strong>AWS Lambda</strong></td>
      <td>Serverless function service with event-driven triggers</td>
      <td>Execute detection logic on-the-fly with minimal infrastructure</td>
    </tr>
    <tr>
      <td><strong>AWS Config</strong></td>
      <td>Tracks resource configuration history and drift</td>
      <td>Detect insecure configurations, noncompliant IAM policies</td>
    </tr>
    <tr>
      <td><strong>Security Hub</strong></td>
      <td>Central dashboard for findings from AWS services</td>
      <td>Correlate findings across CloudTrail, GuardDuty, Inspector</td>
    </tr>
    <tr>
      <td><strong>Detective</strong></td>
      <td>Graph-based threat analysis of logs and behaviors</td>
      <td>Investigate incidents like credential misuse, role assumptions</td>
    </tr>
  </tbody>
</table>

---

## Example: Lambda Function to Detect Public EC2 AMIs

<div style="position:relative;">
  <button onclick="copyCode('code2')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code2', 'public_ami_detector.py')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code2" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
def lambda_handler(event, context):
    if event['detail']['eventName'] == "ModifyImageAttribute":
        if "launchPermission" in event['detail']['requestParameters']:
            permissions = event['detail']['requestParameters']['launchPermission']
            if {"group": "all"} in permissions:
                raise_alert("EC2 AMI made public")
</code></pre>

---

## MITRE ATT&CK Mapping (AWS)

<table>
  <thead>
    <tr><th>Tactic</th><th>Technique</th><th>AWS Source</th><th>Detection Strategy</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Initial Access</td>
      <td>T1078 - Valid Accounts</td>
      <td>CloudTrail</td>
      <td>Login events from unknown IPs or geographies</td>
    </tr>
    <tr>
      <td>Persistence</td>
      <td>T1098 - Account Manipulation</td>
      <td>IAM API Events</td>
      <td>Unauthorized user additions to privileged groups</td>
    </tr>
    <tr>
      <td>Defense Evasion</td>
      <td>T1070 - Indicator Removal</td>
      <td>CloudTrail, S3</td>
      <td>Disabling or deleting logging configurations</td>
    </tr>
    <tr>
      <td>Exfiltration</td>
      <td>T1041 - Exfiltration Over C2 Channel</td>
      <td>VPC Flow Logs</td>
      <td>Outbound traffic to rare foreign IPs</td>
    </tr>
  </tbody>
</table>

---

## Elastic AI Integration (AWS)

You can use Filebeat or Elastic Agent to stream logs from CloudTrail, GuardDuty, and VPC Flow Logs into Elastic. Here's a sample detection rule that correlates high-severity GuardDuty findings:

<div style="position:relative;">
  <button onclick="copyCode('code3')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code3', 'elastic_guardduty_rule.json')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code3" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.module": "aws" }},
        { "match": { "aws.service.name": "guardduty" }},
        { "range": { "aws.guardduty.severity": { "gte": 7 } } }
      ]
    }
  }
}
</code></pre>

---

## Suggested AWS Threat Hunting Queries

You can use these indicators across your security stack:

<table>
  <thead>
    <tr><th>Behavior</th><th>Service</th><th>Sample Indicator</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>Suspicious EC2 launch from TOR exit node</td>
      <td>CloudTrail</td>
      <td>sourceIPAddress = known_tor_ips</td>
    </tr>
    <tr>
      <td>IAM User adding new Admin policy</td>
      <td>CloudTrail</td>
      <td>PutUserPolicy + AdministratorAccess</td>
    </tr>
    <tr>
      <td>Outbound DNS to rare domain</td>
      <td>VPC Flow Logs + Route53</td>
      <td>*.xyz or *.top domains with no previous history</td>
    </tr>
  </tbody>
</table>