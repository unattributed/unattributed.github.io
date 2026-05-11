---
layout: post
title: "Browser-Safe AI Systems, Part 25: Building a Practical Python Test Harness"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, python, test-harness, automation, red-team]
---

> Series: Browser-Safe AI Systems, Part 25 of 32.

This post continues the Browser-Safe AI Systems series by focusing on building a practical python test harness. The goal is to keep the discussion useful for analysts who investigate alerts, red teams who validate controls, developers who build the pipeline, and technical stakeholders who own risk decisions.

Series navigation: [Previous: Part 24]({% post_url 2026-05-09-browser-safe-ai-systems-24-red-team-testing-methodology-for-ai-browser-controls %}) | [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-00-series-index %}) | [Next: Part 26]({% post_url 2026-05-09-browser-safe-ai-systems-26-evidence-collection-what-must-be-logged-and-verified %})

* * *

## 25. Building a Practical Python Test Harness

A browser-safe AI validation program benefits from a practical test harness.

The purpose of the harness is not to build phishing infrastructure.

The purpose is to generate controlled browser artifacts, drive them through a protected browser path, and collect repeatable evidence.

A useful harness should help security teams answer:

**What happened when a known adversarial test page passed through the browser security pipeline?**

### 25.1 What the Harness Should Do

A practical Python harness should support four functions:

1. Generate controlled test pages.
2. Serve those pages from an approved lab domain or local test environment.
3. Drive a browser through the workflows where allowed.
4. Collect evidence and compare expected behavior to observed behavior.

The harness should use seeded credentials, inert files, lab domains, and clearly labeled test pages.

### 25.2 Test Page Generator

The page generator should create repeatable variants.

Useful page types include:

* hidden DOM instruction page
* CSS-hidden text page
* screenshot-visible instruction page
* SVG metadata page
* fake login form with seeded credentials only
* image-rendered login form
* QR-code handoff page
* delayed credential form
* DOM and screenshot mismatch page
* Unicode spoofing page
* oversized DOM page
* malformed metadata page
* fake file-sharing page using inert files
* fake support upload page
* scanner-safe page that changes after interaction

Each generated page should include:

* test ID
* test description
* expected secure behavior
* visible content
* hidden content
* risk category
* timestamp
* version hash

### 25.3 Web Server Layer

The harness can serve test pages from a controlled server.

For basic local testing, Python can serve static content. For more realistic testing, a small Flask or FastAPI app can provide dynamic behavior such as delayed rendering, user-agent changes, region simulation, and staged workflows.

The server should log:

* request timestamp
* source IP
* user agent
* requested path
* referrer
* cookie state where used
* stage of workflow
* test ID
* submission of seeded data only

The server should never collect real credentials.

### 25.4 Browser Automation Layer

Browser automation can be used where permitted.

The automation layer should:

* open test pages
* wait for defined page states
* capture screenshots
* capture DOM
* capture page title
* capture visible text
* capture console errors where useful
* follow controlled redirects
* interact with seeded forms
* scan QR targets where implemented
* record timing
* save artifacts per test ID

Playwright is a strong option for this class of testing because it supports modern browser automation and artifact capture.

Selenium can also be used, especially in environments where it is already part of the testing stack.

### 25.5 Evidence Collector

The evidence collector should produce one folder per test.

Useful artifacts:

* test metadata JSON
* screenshot before interaction
* screenshot after interaction
* DOM before interaction
* DOM after interaction
* extracted text
* QR target if present
* redirect log
* browser console log
* server access log
* seeded submission log
* expected behavior
* observed behavior
* analyst notes
* policy result
* SIEM event reference
* screenshot hash
* DOM hash

### 25.6 Safety Controls

Required safeguards:

* lab domains only
* seeded credentials only
* inert files only
* no real brand impersonation against public users
* no public credential collection
* clear page banners for internal testing where appropriate
* limited access to generated pages
* access logging
* test data deletion process
* no malware
* no denial-of-service behavior unless explicitly authorized
* no attacks against vendor infrastructure

### 25.7 Analyst, Red-Team, Developer, and Stakeholder Use

Analysts can review screenshots, DOM snapshots, event timelines, SIEM alerts, policy actions, and seeded data handling.

Red teams can use the harness as a regression suite for adversarial browser content.

Developers can validate redaction, schema validation, output handling, timeout behavior, evidence storage, and downstream output sanitization.

Stakeholders can track pass rate, false negatives, false positives, fail-open count, evidence completeness, redaction failures, and retest status.

### 25.8 Defensive Principle

A Python harness does not need to be complex to be useful.

It needs to be safe, repeatable, evidence-rich, and aligned to real browser attack classes.

The safest rule is:

**Generate controlled hostile artifacts, run them through the protected browser path, capture evidence, compare expected and observed behavior, and repeat after every meaningful change.**