---
layout: post
title: "Browser-Safe AI Systems, Part 07: Defining Poison Packets for Browser AI"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, poison-packets, adversarial-input, red-team]
---

> Series: Browser-Safe AI Systems, Part 07 of 32.

This post continues the Browser-Safe AI Systems series by focusing on defining poison packets for browser ai. The goal is to keep the discussion useful for analysts who investigate alerts, red teams who validate controls, developers who build the pipeline, and technical stakeholders who own risk decisions.

Series navigation: [Previous: Part 06]({% post_url 2026-05-09-browser-safe-ai-systems-06-the-core-risk-untrusted-web-content-entering-an-ai-context %}) | [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-series-index %}) | [Next: Part 08]({% post_url 2026-05-09-browser-safe-ai-systems-08-practical-attack-classes-against-ai-backed-browser-security %})

* * *

## 7. Defining Poison Packets for Browser AI

A poison packet is a crafted input object designed to corrupt interpretation.

In traditional network language, a packet is a unit of traffic. In browser-safe AI, the idea is broader. The packet may be any artifact that enters the AI inspection path: web page, DOM snapshot, screenshot, image, QR code, metadata, form field, accessibility-tree object, redirect chain, support bundle, log artifact, or model-generated summary.

A useful working definition is:

**A poison packet is any crafted browser, document, or workflow artifact designed to manipulate AI interpretation, classification, evidence handling, policy enforcement, or downstream automation.**

The term matters because it moves the conversation away from only thinking about malware. A poison packet does not need memory corruption, sandbox escape, endpoint compromise, or payload installation. It may only need to make the AI-assisted system reach the wrong conclusion.

That conclusion may be: this page is safe, this login form is legitimate, this brand match is trustworthy, this file movement is normal, this user action is low risk, this alert is noise, this exception should be approved, this analyst summary is accurate, or this event should tune future detection.

OWASP describes indirect prompt injection as a condition where an LLM accepts input from external sources such as websites or files, and that external content alters model behavior in unintended ways. That is one form of poison packet. The broader concept also includes visual deception, malformed structure, data minimization failures, evidence distortion, and unsafe downstream handling. ([genai.owasp.org](https://genai.owasp.org/llmrisk/llm01-prompt-injection/))

A poison packet can target several layers.

### 7.1 Poisoning the Classifier

The attacker wants the system to mislabel a page, file, workflow, or session. Examples include a phishing page that includes hidden benign claims, a fake login page with neutral DOM text, a page that changes after inspection, a QR page that moves the user to an uninspected credential flow, a Unicode spoof, or an oversized DOM that forces fallback behavior.

For analysts, every allowed decision should be explainable. For red teams, these are false-negative tests. For developers, DOM, screenshot, URL, redirect behavior, and form intent should be compared. For stakeholders, the business question is whether the control can explain decisions under adversarial conditions.

### 7.2 Poisoning the Evidence

A browser-safe AI system may produce screenshots, summaries, verdicts, risk labels, SIEM events, support artifacts, and analyst notes. If those artifacts are incomplete or misleading, the investigation can go in the wrong direction.

Examples include a page that renders one message to the user and another to inspection, a DOM snapshot that omits visible deception, a screenshot captured before delayed content appears, a model summary that downplays credential requests, or a support bundle containing session tokens.

### 7.3 Poisoning the Policy Path

If AI output influences enforcement, a poison packet may shape whether the system allows, blocks, isolates, warns, restricts, escalates, or suppresses a page. Model output should not be policy. The model may provide classification. Policy code should decide enforcement.

### 7.4 Poisoning the Data Handling Path

Browser-safe AI may process sensitive artifacts. Screenshots may contain names, documents, account identifiers, and internal data. DOM snapshots may contain hidden fields. HAR files and support bundles may contain session material. A poison packet may cause sensitive data to be captured, retained, summarized, forwarded, or exposed.

### 7.5 Poisoning the Feedback Loop

Some systems use analyst feedback, user reports, allowlists, blocklists, or exception approvals to improve future outcomes. That feedback path is valuable, but it can become a poisoning path. Repeated false positive reports, social engineering through exception requests, manipulated analyst summaries, and permanent policy exceptions can create durable bypasses.

### 7.6 Practical Test Categories

A validation program should include hidden DOM instruction pages, CSS-hidden content pages, screenshot-visible instruction pages, SVG metadata pages, alt-text manipulation pages, accessibility-tree mismatch pages, DOM versus screenshot disagreement pages, delayed credential forms, QR workflow escape pages, Unicode and homograph spoof pages, oversized DOM stress pages, malformed metadata pages, fake login pages using seeded credentials, fake file-sharing pages using inert files, and exception-workflow manipulation tests.

### 7.7 Defensive Principle

The browser is a hostile input channel.

A poison packet is how that hostility is packaged for the AI era.

The safest rule is:

**Hostile content should not be able to silently control classification, evidence, policy, data handling, or future tuning.**