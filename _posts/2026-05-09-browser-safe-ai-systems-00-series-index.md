---
layout: post
title: "Series: Browser-Safe AI Systems"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, ai-security, browser-security, prompt-injection, phishing, red-team, soc, series]
---

# Series: Browser-Safe AI Systems

Browser-safe AI systems are becoming part of the modern security control plane because the browser is where users authenticate, open SaaS, move files, follow links, scan QR codes, and make trust decisions.

This series treats browser-safe AI as a controlled security pipeline, not as a magic model. The central position is that hostile browser content should be treated as adversarial input, AI verdicts should be constrained, policy should remain outside the model, and every important decision should produce evidence that analysts, red teams, developers, and stakeholders can review.

The series is written for four audiences:

* Security analysts who need evidence-rich alerts.
* Red team members who need repeatable validation methods.
* Developers who need secure input, output, and policy boundaries.
* Technical stakeholders who need measurable risk reduction.

## Main Series

* [Part 01: Executive Summary]({% post_url 2026-05-09-browser-safe-ai-systems-01-executive-summary %})
* [Part 02: Why Browser-Safe AI Systems Matter Now]({% post_url 2026-05-09-browser-safe-ai-systems-02-why-browser-safe-ai-systems-matter-now %})
* [Part 03: From Browser Isolation to AI-Assisted Browser Defense]({% post_url 2026-05-09-browser-safe-ai-systems-03-from-browser-isolation-to-ai-assisted-browser-defense %})
* [Part 04: What the SafeBreach Gemini Calendar Research Demonstrates]({% post_url 2026-05-09-browser-safe-ai-systems-04-what-the-safebreach-gemini-calendar-research-demonstrates %})
* [Part 05: Why This Research Applies to Browser-Safe AI Systems]({% post_url 2026-05-09-browser-safe-ai-systems-05-why-this-research-applies-to-browser-safe-ai-systems %})
* [Part 06: The Core Risk: Untrusted Web Content Entering an AI Context]({% post_url 2026-05-09-browser-safe-ai-systems-06-the-core-risk-untrusted-web-content-entering-an-ai-context %})
* [Part 07: Defining Poison Packets for Browser AI]({% post_url 2026-05-09-browser-safe-ai-systems-07-defining-poison-packets-for-browser-ai %})
* [Part 08: Practical Attack Classes Against AI-Backed Browser Security]({% post_url 2026-05-09-browser-safe-ai-systems-08-practical-attack-classes-against-ai-backed-browser-security %})
* [Part 09: Indirect Prompt Injection Through Web Pages]({% post_url 2026-05-09-browser-safe-ai-systems-09-indirect-prompt-injection-through-web-pages %})
* [Part 10: Hostile DOM, Hidden Text, and Metadata Manipulation]({% post_url 2026-05-09-browser-safe-ai-systems-10-hostile-dom-hidden-text-and-metadata-manipulation %})
* [Part 11: Screenshot-Based Prompt Injection and Visual Deception]({% post_url 2026-05-09-browser-safe-ai-systems-11-screenshot-based-prompt-injection-and-visual-deception %})
* [Part 12: DOM Versus Rendered Page Mismatch]({% post_url 2026-05-09-browser-safe-ai-systems-12-dom-versus-rendered-page-mismatch %})
* [Part 13: QR Phishing, Brand Impersonation, and Multistage Lures]({% post_url 2026-05-09-browser-safe-ai-systems-13-qr-phishing-brand-impersonation-and-multistage-lures %})
* [Part 14: Unicode, Homograph, and Visual Spoofing Attacks]({% post_url 2026-05-09-browser-safe-ai-systems-14-unicode-homograph-and-visual-spoofing-attacks %})
* [Part 15: Delayed Content, Region-Gated Pages, and Evasive Phishing]({% post_url 2026-05-09-browser-safe-ai-systems-15-delayed-content-region-gated-pages-and-evasive-phishing %})
* [Part 16: AI Verdict Manipulation and False Negative Risk]({% post_url 2026-05-09-browser-safe-ai-systems-16-ai-verdict-manipulation-and-false-negative-risk %})
* [Part 17: False Positives, Alert Fatigue, and Trust Erosion]({% post_url 2026-05-09-browser-safe-ai-systems-17-false-positives-alert-fatigue-and-trust-erosion %})
* [Part 18: Data Handling Risks: Screenshots, DOM, URLs, and User Context]({% post_url 2026-05-09-browser-safe-ai-systems-18-data-handling-risks-screenshots-dom-urls-and-user-context %})
* [Part 19: Privacy, Retention, Redaction, and Tenant Isolation]({% post_url 2026-05-09-browser-safe-ai-systems-19-privacy-retention-redaction-and-tenant-isolation %})
* [Part 20: Model Output Handling: Why AI Verdicts Must Be Constrained]({% post_url 2026-05-09-browser-safe-ai-systems-20-model-output-handling-why-ai-verdicts-must-be-constrained %})
* [Part 21: Fail-Open Versus Fail-Closed Security Decisions]({% post_url 2026-05-09-browser-safe-ai-systems-21-fail-open-versus-fail-closed-security-decisions %})
* [Part 22: Feedback-Loop Poisoning and Exception Abuse]({% post_url 2026-05-09-browser-safe-ai-systems-22-feedback-loop-poisoning-and-exception-abuse %})
* [Part 23: Secure Architecture Principles for Browser-Safe AI]({% post_url 2026-05-09-browser-safe-ai-systems-23-secure-architecture-principles-for-browser-safe-ai %})
* [Part 24: Red-Team Testing Methodology for AI Browser Controls]({% post_url 2026-05-09-browser-safe-ai-systems-24-red-team-testing-methodology-for-ai-browser-controls %})
* [Part 25: Building a Practical Python Test Harness]({% post_url 2026-05-09-browser-safe-ai-systems-25-building-a-practical-python-test-harness %})
* [Part 26: Evidence Collection: What Must Be Logged and Verified]({% post_url 2026-05-09-browser-safe-ai-systems-26-evidence-collection-what-must-be-logged-and-verified %})
* [Part 27: SOC Usefulness: Turning AI Decisions Into Actionable Evidence]({% post_url 2026-05-09-browser-safe-ai-systems-27-soc-usefulness-turning-ai-decisions-into-actionable-evidence %})
* [Part 28: Governance Questions for Vendors and Customers]({% post_url 2026-05-09-browser-safe-ai-systems-28-governance-questions-for-vendors-and-customers %})
* [Part 29: Practical Recommendations for Security Teams]({% post_url 2026-05-09-browser-safe-ai-systems-29-practical-recommendations-for-security-teams %})
* [Part 30: Practical Recommendations for Vendors and Developers]({% post_url 2026-05-09-browser-safe-ai-systems-30-practical-recommendations-for-vendors-and-developers %})
* [Part 31: How This Research Changes Browser Security Validation]({% post_url 2026-05-09-browser-safe-ai-systems-31-how-this-research-changes-browser-security-validation %})
* [Part 32: Conclusion: Treat AI as an Untrusted Classifier Inside a Controlled Security Pipeline]({% post_url 2026-05-09-browser-safe-ai-systems-32-conclusion-treat-ai-as-an-untrusted-classifier-inside-a-controlled-security-pipeline %})

## Supporting Documents

* [Appendix B: Vendor Due-Diligence Questionnaire]({% post_url 2026-05-09-browser-safe-ai-systems-33-vendor-due-diligence-questionnaire %})
* [Appendix C: Rules of Engagement Template]({% post_url 2026-05-09-browser-safe-ai-systems-34-rules-of-engagement-template %})
* [Appendix D: Glossary]({% post_url 2026-05-09-browser-safe-ai-systems-35-glossary %})

## Series Principle

**Treat AI as an untrusted classifier inside a controlled security pipeline.**