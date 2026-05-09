---
layout: post
title: "Threat Hunting Primer - Section 1: Intro & Overview - Cloud Threat Hunting"
date: 2025-05-12
author: unattributed
categories: [threat-hunting]
tags: [threat-hunting, aws, azure, gcp]
---

# Threat Hunting in Multi-Cloud Environments

---

## Introduction

The ever-expanding attack surface of cloud-native systems introduces sophisticated threats that evade conventional security tooling. In a multi-cloud environment (AWS, Azure, GCP), defenders must combine telemetry, detection rules, behavioral analytics, and threat intelligence to proactively hunt for anomalies.

This blog post provides a **detailed technical walkthrough of cloud-native threat hunting strategies**, using real-world tools and data sources from the three major cloud platforms, enhanced with **Elastic AI**, **MITRE ATT&CK mappings**, **Lambda/KQL-based detections**, **YARA rules**, and CI/CD pipeline integration.

---

## Why Cloud Threat Hunting?

Cloud platforms provide immense agility — and equally vast risks. Threat hunting in cloud involves:

- **Correlating activity across heterogeneous services** (Compute, Storage, Networking, IAM, Serverless).
- **Detecting unknown or novel threats** by exploring logs and anomalies not caught by default rules.
- **Proactively securing environments** beyond reactive alerting or SIEM coverage.

---

## Cloud Platforms Covered

We will dive into threat hunting with the following:

<table style="border-collapse: collapse; width: 100%; border: 1px solid lightgrey;">
  <thead>
    <tr>
      <th style="border: 1px solid lightgrey; padding: 8px;">Platform</th>
      <th style="border: 1px solid lightgrey; padding: 8px;">Focus Areas</th>
      <th style="border: 1px solid lightgrey; padding: 8px;">Native Security Tools</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>AWS</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Serverless (Lambda), IAM, S3, CloudTrail, VPC, GuardDuty</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">CloudTrail, GuardDuty, Security Hub, Detective, AWS Config</td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Azure</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">AD Identity, Log Analytics, Function Apps, Key Vault, Containers</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Microsoft Defender XDR, Azure Sentinel, Azure Monitor</td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>GCP</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">IAM, SCC, VPC, Cloud Functions, Pub/Sub, BigQuery</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Security Command Center, Cloud Audit Logs, Google SecOps</td>
    </tr>
  </tbody>
</table>

---

## What You'll Learn

- How to **derive data** from native cloud services.
- How to **craft detection rules** using:
  - AWS Lambda
  - Azure Kusto Query Language (KQL)
  - YARA rules
- How to **map behaviors to MITRE ATT&CK**
- How to **centralize findings in Elastic AI**
- How to **embed threat hunting in CI/CD pipelines**

---

## Example: Interactive Detection Rule (HTML block)

Below is an example rule written for AWS Lambda to detect overly permissive S3 policies.

<div style="position:relative;">
  <button onclick="copyCode('code1')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code1', 's3_policy_detector.py')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
<pre id="code1" style="background:#1e1e1e;color:#dcdcdc;padding:1em;"><code>
def lambda_handler(event, context):
  if event['detail']['eventName'] == "PutBucketPolicy":
    if "Allow": "Everyone" in event['detail']
      ['requestParameters']:
      raise_alert("Public S3 bucket detected")
</code></pre>
<script>
  function copyCode(id) {
    const el = document.createElement("textarea");
    el.value = document.getElementById(id).innerText;
    document.body.appendChild(el);
    el.select();
    document.execCommand("copy");
    document.body.removeChild(el);
  }
  function downloadCode(id, filename) {
    const text = document.getElementById(id).innerText;
    const element = document.createElement('a');
    const file = new Blob([text], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }
</script>