---
layout: post
title: "Browser-Safe AI Systems, Appendix C: Rules of Engagement Template"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, red-team, governance]
tags: [browser-safe-ai, rules-of-engagement, red-team, security-validation, seeded-data]
---

> Series support document: Browser-Safe AI Systems, Appendix C: Rules of Engagement Template.

This supporting document belongs with the Browser-Safe AI Systems series. It is designed as a practical reference that can be used alongside the main sections when reviewing vendors, scoping assessments, or standardizing language across analyst, red-team, developer, and stakeholder discussions.

Series navigation: [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-00-series-index %})

* * *

# Appendix C. Rules of Engagement Template

This template defines safe operating boundaries for validating browser-safe AI systems.

It is intended for authorized security assessments, red-team exercises, product security reviews, internal validation, and customer acceptance testing.

The purpose is to test controls without creating uncontrolled phishing, credential theft, data leakage, business disruption, or vendor infrastructure risk.

## C.1 Engagement Purpose

The engagement will evaluate whether browser-safe AI controls can safely inspect hostile browser artifacts, classify risky workflows, enforce policy, preserve evidence, protect sensitive data, and provide useful SOC telemetry.

The assessment will focus on controlled adversarial test content and approved workflows.

The assessment will not target real users unless explicitly authorized.

The assessment will not collect real credentials.

The assessment will not attack vendor-owned infrastructure.

## C.2 Engagement Scope

### In Scope

Approved testing may include:

* controlled lab domains
* test browser sessions
* test user accounts
* seeded credentials
* inert file samples
* controlled QR-code pages
* fake login pages using seeded credentials only
* fake file-sharing workflows using inert files
* fake support upload pages using seeded data
* delayed content tests
* DOM and screenshot mismatch tests
* hidden DOM content tests
* screenshot-based deception tests
* Unicode and homograph-style tests using approved domains
* data handling tests with seeded sensitive values
* fail-open and fail-closed behavior tests
* exception workflow review
* SOC alert review
* SIEM event review
* evidence retention review

### Out of Scope

The following are out of scope unless separately approved:

* collection of real user credentials
* testing against real users
* public phishing campaigns
* attacks against vendor infrastructure
* denial-of-service testing
* malware execution
* exploitation of third-party systems
* impersonation of real third-party brands outside approved lab context
* bypassing legal access controls
* accessing data outside authorized test accounts
* persistence on endpoints
* destructive activity
* unauthorized data exfiltration

## C.3 Authorized Test Data

Only approved test data may be used.

Allowed seeded data examples:

* fake usernames
* fake passwords
* fake session tokens
* fake customer IDs
* fake account numbers
* fake API keys
* fake reset links
* fake OAuth codes
* fake internal URLs
* fake regulated data markers
* inert files
* synthetic documents
* test QR targets

No production secrets may be used.

No real customer data may be used.

No real user passwords may be used.

## C.4 Approved Infrastructure

Testing should use approved infrastructure only.

Approved infrastructure may include:

* lab domain
* lab web server
* internal test network
* approved cloud test environment
* approved test browser profile
* approved test user accounts
* approved SIEM test index
* approved evidence repository
* approved ticketing sandbox

All domains, IP addresses, and accounts should be documented before testing begins.

## C.5 Test User Accounts

Test accounts should be clearly identified.

Required properties:

* no privileged production access unless specifically approved
* no access to real sensitive data
* seeded mailbox or SaaS content only
* known group membership
* known policy assignment
* known device posture
* known browser configuration
* known network path

Account usage should be logged.

## C.6 Credential Handling

Rules:

* do not collect real credentials
* do not request real credentials from users
* do not store real credentials in test artifacts
* use seeded credentials only
* label seeded credentials clearly
* record where seeded credentials appear
* verify redaction in logs, alerts, screenshots, prompts, and exports
* delete seeded credentials after testing where appropriate

A test that accidentally captures real credentials must be escalated immediately.

## C.7 File Handling

Rules:

* use inert files only
* do not use malware
* do not use weaponized documents
* do not use real sensitive data
* label test files clearly
* use seeded file names where needed
* track upload and download behavior
* verify file metadata handling
* verify evidence and SIEM logging

If malware-like files are required for a specific assessment, they require separate written approval and containment procedures.

## C.8 QR-Code Testing

Rules:

* QR targets must point to approved lab destinations
* QR pages must not collect real credentials
* QR targets must not impersonate real brands outside approved context
* QR target URLs must be documented
* QR scans should be conducted from approved test devices where possible
* mobile handoff behavior should be logged
* no public distribution of QR lures

The purpose is to test cross-context workflow handling.

## C.9 Evidence Handling

All evidence should be protected.

Evidence may include:

* screenshots
* DOM snapshots
* URLs
* QR targets
* seeded credentials
* seeded tokens
* test logs
* model verdicts
* model prompts
* model responses
* SIEM events
* analyst notes
* ticket records
* support bundles

Evidence handling rules:

* store evidence in approved location
* restrict access
* redact where possible
* separate raw evidence from derived evidence
* label sensitive artifacts
* avoid copying raw evidence into chat or email
* audit access where possible
* define retention and deletion timeline

## C.10 Redaction Testing

Seeded sensitive data should be used to verify redaction.

Track seeded data across:

* browser alert
* screenshot
* DOM snapshot
* model prompt
* model response
* SIEM event
* analyst summary
* ticket
* support bundle
* debug log
* export

Any unexpected unredacted seeded data should be logged as a finding.

## C.11 SOC Coordination

Before active testing, notify appropriate SOC contacts.

Provide:

* test window
* test accounts
* test domains
* test IP addresses
* expected alert types
* escalation contacts
* stop condition
* evidence collection plan

SOC coordination should not disable realistic detection unless the assessment specifically requires blind testing and approval exists.

## C.12 Stop Conditions

Testing must stop if:

* real credentials are captured
* real user data is exposed
* production service disruption occurs
* testing affects unauthorized users
* vendor infrastructure appears impacted
* legal or compliance risk is identified
* emergency contact requests stop
* test behavior deviates from approved scope

Stop conditions should be enforced immediately.

## C.13 Escalation Process

High-risk findings should be escalated quickly.

Immediate escalation examples:

* unsafe allow of credential-harvesting workflow
* real credential capture
* sensitive data leakage into logs or prompts
* cross-tenant exposure
* broad policy bypass
* fail-open behavior on high-risk workflow
* support bundle containing secrets
* evidence exposed to unauthorized roles

Escalation should include:

* summary
* evidence
* affected scope
* reproduction steps
* recommended containment
* immediate risk reduction

## C.14 Communications

Define communication channels before testing.

Include:

* engagement owner
* technical lead
* SOC contact
* privacy contact
* application owner
* vendor contact where applicable
* emergency stop contact

Do not share raw sensitive evidence in broad channels.

Use links to protected evidence repositories where possible.

## C.15 Reporting Requirements

The final report should include:

* executive summary
* scope
* methodology
* test cases
* observed behavior
* evidence summary
* findings
* severity
* affected policy or workflow
* redaction and privacy observations
* SOC usefulness observations
* exception governance observations
* recommendations
* retest plan

The report should distinguish between:

* detection failure
* policy failure
* evidence failure
* data handling failure
* usability issue
* governance issue

## C.16 Retesting

Retesting should occur after:

* policy change
* model change
* redaction change
* exception approval
* SIEM integration change
* alert schema change
* fail-open behavior change
* false negative fix
* false positive tuning

Retesting should use the same test ID and evidence format where possible.

## C.17 Approval Checklist

Before testing begins, confirm:

* scope approved
* domains approved
* accounts approved
* test data approved
* dates approved
* SOC notified
* emergency contacts defined
* evidence storage approved
* stop conditions accepted
* legal constraints reviewed
* privacy constraints reviewed
* vendor constraints reviewed where applicable

## C.18 Final Rules-of-Engagement Principle

The safest operating rule is:

**Use controlled infrastructure, seeded data, inert files, approved accounts, protected evidence handling, clear stop conditions, and documented authority for every browser-safe AI validation activity.**