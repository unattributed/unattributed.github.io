---
layout: post
title: "Threat Hunting Primer - Section 7: Cross-Cloud Correlation Using Elastic AI"
date: 2025-05-12
author: unattributed
categories: [threat-hunting, automation]
tags: [threat-hunting, automation]
---

# Enterprise-Scale Threat Correlation with Elastic AI

Modern enterprises rarely rely on a single cloud provider — hybrid and multi-cloud environments are the new norm. Elastic AI provides the visibility and intelligence to ingest, normalize, and correlate security data from AWS, Azure, and GCP in one place, enabling true end-to-end threat detection and hunting.

---

## Why Elastic AI for Multi-Cloud Security?

Elastic AI’s unified security and observability platform provides:

- **Data normalization:** Converts AWS CloudTrail, Azure Monitor, and GCP Audit logs into Elastic Common Schema (ECS).
- **Cross-source detection:** Create rules that operate across services, regardless of origin.
- **Machine learning:** Identify rare, anomalous behaviors without predefined signatures.
- **Prebuilt dashboards:** Visualize GuardDuty alerts next to Azure AD sign-ins or GCP IAM changes.

---

## Ingesting Multi-Cloud Data

Elastic Agents and Beats can be deployed as follows:

<table style="border-collapse: collapse; width: 100%; border: 1px solid lightgrey;">
  <thead>
    <tr>
      <th style="border: 1px solid lightgrey; padding: 8px;">Platform</th>
      <th style="border: 1px solid lightgrey; padding: 8px;">Data Sources</th>
      <th style="border: 1px solid lightgrey; padding: 8px;">Elastic Integration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;">AWS</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">CloudTrail, VPC Flow Logs, GuardDuty</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Filebeat modules, AWS input via S3 + CloudWatch</td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;">Azure</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Log Analytics, Azure AD Logs, Defender</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Event Hub -> Logstash/Beats pipeline</td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 8px;">GCP</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Audit Logs, SCC, VPC Flow Logs</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Pub/Sub + Elastic Agent or Google Log Export to GCS</td>
    </tr>
  </tbody>
</table>

---

## Cross-Platform Detection Rule (Elastic DSL)

The following rule detects admin role assignments across all platforms:

<div style="position:relative;">
  <button onclick="copyCode('code11')" style="position:absolute;top:0;right:0;">Copy</button>
  <button onclick="downloadCode('code11', 'elastic_admin_escalation_rule.json')" style="position:absolute;top:0;right:60px;">Download</button>
</div>
```json
{
  "query": {
    "bool": {
      "should": [
        { 
          "match": { 
            "aws.cloudtrail.eventName": "AddUserToGroup" 
          } 
        },
        { 
          "match": { 
            "azure.auditlogs.operationName": "Add member to role" 
          } 
        },
        { 
          "match": { 
            "gcp.auditlog.methodName": "SetIamPolicy" 
          } 
        }
      ],
      "minimum_should_match": 1
    }
  }
}
```

---

## Visualizing Threat Activity

Elastic dashboards let you pivot across platforms:

- **Heatmaps** of login attempts by country (Azure + AWS)
- **Bar charts** of IAM changes by platform
- **Time series graphs** correlating alerts to incident response

---

## Machine Learning for Behavioral Detection

Elastic's ML module can identify:

- **Rare user behaviors**: A user accessing data from a new region or service.
- **Spike detection**: Unusual amounts of failed logins or S3 API calls.
- **Process anomalies**: Lambda executions doing unexpected operations.

---

## Real-World Use Case

**Scenario:**  
You detect that a GCP service account has been granted Owner rights at 2:45 AM UTC. In Elastic, this triggers a rule which simultaneously checks:

- Was a similar role change made in Azure within 30 minutes?
- Was an IAM permission escalation made in AWS?

If so, an **Elastic alert is triggered** showing a potential coordinated attack across cloud accounts.

---

## Final Thoughts

Elastic AI offers a battle-tested solution for organizations seeking comprehensive visibility across cloud environments. With customizable detection rules, embedded ML, and real-time dashboards, your SOC or SRE team can hunt, detect, and respond to threats—no matter where they originate.

By integrating Elastic with native cloud telemetry, CI/CD workflows, YARA detection logic, and AI reporting tools, you empower your threat hunting and reliability engineering efforts with automation, speed, and scale.


[Back to Top](#enterprise-scale-threat-correlation-with-elastic-ai)