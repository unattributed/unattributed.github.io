---
layout: post
title: "Browser-Safe AI Systems, Part 26: Evidence Collection: What Must Be Logged and Verified"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, evidence, logging, soc, siem]
---

> Series: Browser-Safe AI Systems, Part 26 of 32.

This post continues the Browser-Safe AI Systems series by focusing on evidence collection: what must be logged and verified. The goal is to keep the discussion useful for analysts who investigate alerts, red teams who validate controls, developers who build the pipeline, and technical stakeholders who own risk decisions.

Series navigation: [Previous: Part 25]({% post_url 2026-05-09-browser-safe-ai-systems-25-building-a-practical-python-test-harness %}) | [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-series-index %}) | [Next: Part 27]({% post_url 2026-05-09-browser-safe-ai-systems-27-soc-usefulness-turning-ai-decisions-into-actionable-evidence %})

* * *

## 26. Evidence Collection: What Must Be Logged and Verified

Browser-safe AI systems are only as useful as the evidence they produce.

A block without evidence is hard to tune.  
An allow without evidence is hard to trust.  
A model verdict without artifacts is hard to investigate.  
A summary without source data is hard to verify.  
A SIEM event without context is hard to act on.

The purpose of evidence collection is to make security decisions reviewable.

A useful system should answer:

**What happened, why did the system decide that, what action was taken, and can the decision be reproduced?**

### 26.1 Minimum Evidence Package

A minimum evidence package should include:

* timestamp
* user identity
* device identity
* network context
* browser context
* URL
* sanitized URL
* domain
* path
* referrer where appropriate
* page title
* rendered screenshot
* DOM snapshot or extracted structural summary
* OCR output where used
* QR target where present
* redirect chain
* iframe or frame tree
* form fields detected
* file action detected
* upload or download metadata
* model verdict where available
* model confidence where available
* reason codes
* policy name
* enforcement action
* user-facing message
* SIEM event reference
* exception state
* redaction status

Not every artifact needs to be available to every analyst.

But the system should know what was collected, what was redacted, and what informed the decision.

### 26.2 Evidence for Analysts

Analysts need evidence that supports triage.

An analyst view should show:

* what the user saw
* what the page asked the user to do
* whether credentials were requested
* whether MFA was requested
* whether a QR code was present
* whether file movement occurred
* whether brand impersonation was suspected
* whether DOM and screenshot evidence conflicted
* whether content changed after initial load
* what policy applied
* what action was taken
* whether an exception influenced the result
* whether evidence was redacted

### 26.3 Evidence for Red Teams

Red teams need evidence that supports repeatability.

A red-team evidence record should include:

* test case ID
* expected secure behavior
* observed behavior
* screenshots
* DOM artifacts
* server logs
* browser logs
* policy result
* SIEM alert
* model verdict if available
* analyst-visible evidence
* seeded data tracking
* reproducibility notes

### 26.4 Evidence for Developers

Developers need evidence that supports debugging and secure design.

Useful developer evidence includes:

* extractor output
* redaction output
* model request metadata
* model response schema status
* validation errors
* policy decision trace
* timeout state
* fallback state
* exception logic
* evidence object identifiers
* downstream export status
* log sanitization status

This should be access-controlled.

Developer visibility should not become uncontrolled access to sensitive browser content.

### 26.5 Raw Evidence Versus Derived Evidence

Raw evidence includes full screenshots, DOM snapshots, logs, prompts, model responses, HAR-like artifacts, and support bundles.

Derived evidence includes extracted indicators, reason codes, risk labels, redacted summaries, hashes, feature flags, and policy results.

Raw evidence is more complete but more sensitive.

Derived evidence is safer but may omit context.

A good system stores and exposes them differently.

Raw evidence should have stricter access controls and shorter retention.

Derived evidence can often be retained longer and shared more broadly.

### 26.6 Replayability

Replayability means the team can reconstruct the decision.

A replayable event should include enough context to answer:

* what page state was inspected
* what artifacts were available
* what model input was used
* what output was returned
* what policy was applied
* what action resulted
* whether the event would be handled the same way today

Replayability is critical for incident response, false positive review, false negative review, red-team retesting, policy tuning, vendor escalation, and audit review.

### 26.7 Evidence Gaps

Common evidence gaps include:

* screenshot missing
* DOM missing
* QR target not decoded
* redirect chain not captured
* iframe tree missing
* model verdict unavailable
* reason code absent
* policy name missing
* user context missing
* exception influence not logged
* redaction status unknown
* analyst summary not tied to raw artifacts
* SIEM event missing key fields
* user-visible page state not preserved

Evidence gaps should be tracked as findings.

### 26.8 Defensive Principle

Evidence is the bridge between prevention and trust.

The safest rule is:

**Log the evidence, protect the evidence, make the decision explainable, and ensure the event can be replayed or reviewed when the verdict matters.**