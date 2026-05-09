---
layout: post
title: "Browser-Safe AI Systems, Appendix D: Glossary"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, reference]
tags: [browser-safe-ai, glossary, ai-security, browser-security, reference]
---

> Series support document: Browser-Safe AI Systems, Appendix D: Glossary.

This supporting document belongs with the Browser-Safe AI Systems series. It is designed as a practical reference that can be used alongside the main sections when reviewing vendors, scoping assessments, or standardizing language across analyst, red-team, developer, and stakeholder discussions.

Series navigation: [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-series-index %})

* * *

# Appendix D. Glossary

This glossary defines terms used throughout the browser-safe AI document.

The definitions are written for security analysts, red team members, developers, architects, privacy teams, and technical stakeholders.

## Browser-Safe AI

A browser security approach that uses AI to help inspect, classify, summarize, or enforce decisions about browser activity, web pages, SaaS workflows, file movement, phishing risk, or user interaction.

## Browser Isolation

A security control that separates untrusted web content from the local endpoint, often by executing browser content in a remote or controlled environment and presenting a safer interactive session to the user.

## Remote Browser Isolation

A form of browser isolation where browsing activity is executed away from the endpoint, often in a cloud or remote environment.

## AI-Assisted Browser Defense

A browser security model where AI helps interpret page content, user workflows, visual deception, phishing indicators, file movement, or risky browser behavior.

## Semi-Autonomous Security System

A system that can interpret signals, make recommendations, trigger workflows, or influence enforcement without requiring a human decision at every step.

## Poison Packet

A crafted input object designed to corrupt interpretation, classification, evidence handling, policy enforcement, or downstream automation in an AI-assisted system.

In browser-safe AI, a poison packet may be a web page, screenshot, DOM snapshot, QR code, metadata field, support artifact, or model-generated summary.

## Indirect Prompt Injection

An attack where hostile instructions are embedded in external content, such as a web page, document, email, or calendar invite, and later processed by an AI system in a way that alters the system's behavior.

## Direct Prompt Injection

An attack where the user or attacker enters instructions directly into an AI interface to override, bypass, or manipulate intended behavior.

## Hostile DOM

A DOM structure intentionally crafted to mislead parsers, models, analysts, or browser security controls.

## DOM

The Document Object Model, the structured representation of a web page used by browsers and scripts.

## Rendered Page

The user-visible version of the page after layout, styling, scripts, images, fonts, and browser rendering are applied.

## DOM Versus Rendered Page Mismatch

A condition where the DOM and the visible page do not tell the same story, such as a benign DOM paired with a deceptive visual overlay.

## Screenshot-Based Prompt Injection

An attack where text or visual content in a screenshot is crafted to influence an AI system that analyzes images or rendered browser views.

## Visual Deception

A page design technique intended to make users or AI systems believe a page, brand, workflow, or action is legitimate when it is not.

## Brand Impersonation

The use of logos, layout, wording, colors, domain similarity, or workflow patterns to imitate a trusted organization or service.

## Homograph Attack

An attack that uses visually similar characters to make one identifier look like another, often in domains, names, or page text.

## Unicode Confusable

A character that can be visually confused with another character, especially across scripts or character sets.

## IDN

Internationalized Domain Name, a domain name that supports non-ASCII characters.

## Punycode

An ASCII-compatible encoding used to represent internationalized domain names.

## QR Phishing

A phishing technique that uses QR codes to move the user to a malicious or deceptive destination, often shifting the attack from desktop to mobile.

## Cross-Context Handoff

A workflow where the user is moved from one device, browser, application, network, or trust context to another, such as scanning a QR code from a desktop browser with a personal mobile phone.

## Multistage Lure

A phishing or deception workflow that unfolds across multiple steps, such as email entry, brand selection, credential prompt, MFA prompt, and redirect.

## Delayed Content

Content that appears after initial page load, after a timer, after user interaction, or after a state change.

## Region-Gated Page

A page that changes behavior based on the visitor's geography, IP address, ASN, language, or network context.

## Scanner Evasion

A technique where a page shows benign content to scanners, crawlers, sandboxes, or automation, while showing malicious content to real users.

## AI Verdict

A model-generated classification, label, confidence value, summary, or recommendation about a browser event, page, file, or workflow.

## Verdict Manipulation

An attempt to influence an AI verdict through hostile page content, hidden text, screenshots, metadata, timing, or workflow design.

## False Negative

A failure where malicious or risky activity is classified as safe, allowed, under-alerted, or missed.

## False Positive

A failure where legitimate activity is classified as risky, blocked, warned, or over-alerted.

## Alert Fatigue

A condition where analysts receive too many low-value or unclear alerts, reducing attention and trust.

## Trust Erosion

The loss of confidence in a security control due to repeated false positives, poor explanations, inconsistent behavior, or excessive business friction.

## Fail-Open

A failure behavior where the system allows an activity to proceed when classification, inspection, policy, or enforcement fails.

## Fail-Closed

A failure behavior where the system blocks, isolates, restricts, escalates, or requires additional validation when classification, inspection, policy, or enforcement fails.

## Safe Degradation

A failure mode where the system continues to provide reduced but safe protection when a component is unavailable or uncertain.

## Structured Output

Model output constrained to a defined schema, such as allowed verdicts, reason codes, confidence values, and evidence references.

## Free-Form Output

Unstructured natural-language model output. It may be useful for explanation but should not directly drive security enforcement.

## Schema Validation

The process of checking that model output conforms to required fields, allowed values, type constraints, and size limits.

## Reason Code

A predefined explanation label that describes why a security decision or alert occurred.

Examples include credential form detected, QR code present, DOM mismatch, brand-domain mismatch, or low confidence.

## Policy Engine

The deterministic component that applies explicit rules or configuration to decide enforcement actions.

## Enforcement Action

The action taken by the system, such as allow, block, warn, isolate, restrict upload, restrict download, prevent credential submission, or escalate.

## Evidence Package

The collection of artifacts that explain a browser security decision, such as URL, screenshot, DOM, OCR output, QR target, redirect chain, model verdict, policy action, and reason codes.

## Replayable Evidence

Evidence that allows an analyst, engineer, or tester to reconstruct what happened and why the system acted.

## Raw Evidence

Original or near-original artifacts such as screenshots, DOM snapshots, model prompts, logs, or support bundles.

## Derived Evidence

Processed evidence such as reason codes, redacted summaries, hashes, indicators, feature flags, or policy results.

## Redaction

The removal, masking, or transformation of sensitive data before storage, display, model submission, export, or support access.

## Minimization

The practice of collecting and retaining only the evidence needed for security decision-making and investigation.

## Retention

The length of time evidence or artifacts are stored.

## Tenant Isolation

The separation of data, policy, prompts, responses, feedback, support access, and artifacts between customers, business units, or environments.

## Feedback Loop

A process where user reports, analyst dispositions, exceptions, allowlists, blocklists, or tuning decisions influence future system behavior.

## Feedback-Loop Poisoning

An attempt to manipulate future detection or enforcement by influencing feedback, labels, exceptions, or tuning decisions.

## Exception

A scoped deviation from default security policy, often used to allow a specific user, group, domain, path, workflow, or application.

## Exception Abuse

The misuse or overuse of exceptions in a way that weakens the security control or creates standing bypasses.

## SIEM

Security Information and Event Management system used to collect, correlate, search, and investigate security events.

## SOAR

Security Orchestration, Automation, and Response platform used to automate security workflows.

## SOC

Security Operations Center, the team or function responsible for monitoring, triage, investigation, and response.

## Seeded Data

Synthetic test data intentionally placed in a controlled test to verify redaction, logging, data handling, or leakage behavior.

## Inert File

A harmless test file used to validate upload, download, scanning, logging, or policy behavior without using malware.

## Lab Domain

An approved domain controlled by the testing team for safe validation activities.

## Browser Artifact

Any object derived from browser activity, including screenshots, DOM, URLs, cookies, forms, metadata, QR codes, redirects, logs, and user interaction data.

## Model Prompt

The input sent to an AI model, which may include instructions, page evidence, extracted text, user context, or policy context.

## Model Response

The output returned by an AI model, such as a verdict, summary, reason code, recommendation, or classification.

## Prompt Retention

The storage of prompts after model invocation.

## Zero-Retention Mode

A mode where prompts and responses are not retained by the model provider or service beyond what is necessary for processing, subject to the provider's exact terms and implementation.

## Downstream Output Injection

A condition where unsafe or hostile content from model output enters another system, such as a SIEM, ticket, chat message, dashboard, report, or automation workflow.

## Controlled Pipeline

A security architecture where AI is one component inside a governed process of evidence collection, redaction, classification, validation, policy enforcement, logging, and review.

## Core Principle

The core principle of this document is:

**Treat AI as an untrusted classifier inside a controlled security pipeline.**