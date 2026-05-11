---
layout: post
title: "Browser-Safe AI Systems, Appendix B: Vendor Due-Diligence Questionnaire"
date: 2026-05-09
author: unattributed
categories: [ai-security, browser-security, vendor-risk, governance]
tags: [browser-safe-ai, vendor-risk, due-diligence, ai-governance, privacy]
---

> Series support document: Browser-Safe AI Systems, Appendix B: Vendor Due-Diligence Questionnaire.

This supporting document belongs with the Browser-Safe AI Systems series. It is designed as a practical reference that can be used alongside the main sections when reviewing vendors, scoping assessments, or standardizing language across analyst, red-team, developer, and stakeholder discussions.

Series navigation: [Series index]({% post_url 2026-05-09-browser-safe-ai-systems-00-series-index %})

* * *

# Appendix B. Vendor Due-Diligence Questionnaire

This questionnaire is intended for security analysts, red team members, developers, architects, privacy teams, procurement teams, and technical stakeholders evaluating browser-safe AI systems.

The goal is not to create a paperwork exercise.

The goal is to identify what the system observes, what it sends to AI services, how it handles evidence, what AI can influence, how policy is enforced, and whether the control can be tested and trusted.

## B.1 System Scope

### Questions

* What browser activity does the system inspect?
* Does the system inspect managed browsers only, or unmanaged browsers as well?
* Does the system inspect SaaS workflows?
* Does the system inspect private application access?
* Does the system inspect file uploads?
* Does the system inspect file downloads?
* Does the system inspect QR-code workflows?
* Does the system inspect browser redirects?
* Does the system inspect iframe or embedded content?
* Does the system inspect mobile browser handoff?
* Does the system inspect user interaction after initial page load?

### Evidence to Request

* Architecture diagram
* Data flow diagram
* Browser control points
* Policy enforcement points
* List of inspected artifact types
* List of unsupported browser scenarios
* Deployment mode documentation
* Known limitations

## B.2 AI Processing

### Questions

* Where is AI used in the browser security pipeline?
* What model or model provider is used?
* Is the model local, vendor-hosted, customer-hosted, or third-party hosted?
* What browser artifacts are sent to the model?
* Are screenshots sent to the model?
* Are DOM snapshots sent to the model?
* Is OCR output sent to the model?
* Are URLs or query strings sent to the model?
* Is user identity sent to the model?
* Is device context sent to the model?
* Is policy context sent to the model?
* Are prompts stored?
* Are model responses stored?
* Are prompts or responses used for training?
* Are prompts or responses used for tuning?
* Can customers opt out of training or shared tuning?
* Is zero-retention mode available?
* Are model changes communicated to customers?
* Can customers test before and after model changes?

### Evidence to Request

* AI data flow description
* Prompt and response handling policy
* Model provider terms
* Training and tuning policy
* Retention policy for prompts and responses
* Model change management process
* Customer opt-out controls

## B.3 Data Collection

### Questions

* Are screenshots captured?
* Are screenshots full page, viewport only, cropped, or feature-extracted?
* Are DOM snapshots captured?
* Are full URLs retained?
* Are query strings retained?
* Are QR targets decoded and retained?
* Are redirect chains retained?
* Are iframe trees retained?
* Are file names retained?
* Are form fields retained?
* Are hidden fields retained?
* Are cookies or headers retained?
* Are HAR-like artifacts collected?
* Are user and device identifiers stored with events?

### Evidence to Request

* Artifact inventory
* Data dictionary
* Field-level sensitivity classification
* Collection trigger conditions
* Example alert records
* Example SIEM export
* Example support bundle

## B.4 Redaction and Minimization

### Questions

* What is redacted before model submission?
* What is redacted before storage?
* What is redacted before analyst display?
* What is redacted before SIEM export?
* What is redacted before ticket creation?
* What is redacted before support bundle generation?
* Are passwords detected and redacted?
* Are session tokens detected and redacted?
* Are cookies detected and redacted?
* Are reset links detected and redacted?
* Are OAuth codes detected and redacted?
* Are API keys detected and redacted?
* Are screenshots masked?
* Are DOM fields masked?
* Are query parameters stripped or tokenized?
* Can redaction rules be configured?
* Is redaction tested with seeded sensitive data?

### Evidence to Request

* Redaction policy
* Redaction test results
* Sample redacted artifacts
* Sample raw versus redacted event
* Redaction failure behavior
* Redaction configuration options

## B.5 Model Output Handling

### Questions

* Is model output structured?
* Is output schema-constrained?
* Are reason codes predefined?
* Are unsupported fields rejected?
* Is model output validated before use?
* Can free-form model output influence enforcement?
* Can free-form model output influence analyst summaries?
* Can free-form model output influence exceptions?
* Can model output create or modify policy?
* What happens when model output is invalid?
* What happens when model output is low confidence?
* What happens when model output conflicts with policy?

### Evidence to Request

* Model output schema
* Reason code list
* Validation rules
* Invalid output handling documentation
* Sample valid output
* Sample invalid output behavior
* Policy enforcement trace

## B.6 Policy and Enforcement

### Questions

* What decisions can the system make?
* Can it allow, block, isolate, warn, or restrict?
* Can it prevent credential submission?
* Can it restrict file upload?
* Can it restrict file download?
* Can it require step-up authentication?
* Can it escalate to analyst review?
* Is final enforcement deterministic?
* Is policy enforced outside the model?
* Are policy decisions auditable?
* Are policy changes logged?
* Can customers simulate policy changes before deployment?

### Evidence to Request

* Policy decision flow
* Enforcement matrix
* Policy audit logs
* Sample policy trace
* Change management documentation
* Rollback procedure

## B.7 Fail-Open and Fail-Closed Behavior

### Questions

* What happens when the AI model is unavailable?
* What happens when the model times out?
* What happens when screenshot capture fails?
* What happens when DOM extraction fails?
* What happens when redaction fails?
* What happens when policy lookup fails?
* What happens when evidence conflicts?
* What happens when confidence is low?
* Are fail-open events logged?
* Are fail-closed events logged?
* Can failure behavior be configured by risk level?
* Are high-risk workflows handled differently?

### Evidence to Request

* Failure mode table
* Fallback behavior documentation
* Fail-open metrics
* Fail-closed metrics
* Test results for model outage
* Test results for invalid output
* Test results for missing evidence

## B.8 Evidence and SOC Usefulness

### Questions

* What evidence appears in alerts?
* Are screenshots available?
* Are DOM artifacts available?
* Are QR targets shown?
* Are redirects shown?
* Are reason codes included?
* Are confidence values included?
* Is uncertainty visible?
* Is policy action visible?
* Are exceptions visible?
* Can analysts replay the event?
* Can analysts see what was redacted?
* Is SIEM export structured?
* Are raw artifacts copied into tickets?
* Are alert fields searchable?

### Evidence to Request

* Sample analyst alert
* Sample SIEM event
* Sample case record
* Evidence schema
* Replay workflow
* Analyst guide
* Triage playbook

## B.9 Tenant Isolation

### Questions

* How is tenant data isolated?
* Are raw artifacts tenant-scoped?
* Are prompts tenant-scoped?
* Are model responses tenant-scoped?
* Are support bundles tenant-scoped?
* Are debug logs tenant-scoped?
* Are feedback labels tenant-scoped?
* Can one tenant's data influence another tenant's detection?
* Can one tenant's exception influence another tenant?
* Are tenant access controls audited?
* Are tenant-specific encryption keys used?

### Evidence to Request

* Tenant isolation architecture
* Access control model
* Support access model
* Tenant data handling policy
* Cross-tenant prevention controls
* Audit evidence

## B.10 Support Access

### Questions

* Can vendor support access customer evidence?
* Is customer approval required?
* Is support access just-in-time?
* Is support access time-limited?
* Is support access audited?
* Can support view raw screenshots?
* Can support view DOM artifacts?
* Can support view model prompts?
* Can support export evidence?
* Are support bundles redacted?
* Are support bundles deleted after case closure?

### Evidence to Request

* Support access policy
* Support audit log sample
* Support bundle sample
* Support retention policy
* Customer approval workflow

## B.11 Exception Governance

### Questions

* Who can approve exceptions?
* Are exceptions scoped by user, group, domain, path, workflow, and time?
* Do exceptions expire?
* Are stale exceptions reported?
* Are exceptions auditable?
* Can exceptions bypass AI inspection?
* Can exceptions suppress alerts?
* Can exceptions override DLP?
* Are exception changes regression-tested?
* Are exceptions reviewed after incidents?

### Evidence to Request

* Exception workflow
* Exception schema
* Example exception record
* Exception audit log
* Stale exception report
* Exception review process

## B.12 Feedback and Tuning

### Questions

* Can user feedback influence future detection?
* Can analyst labels influence future detection?
* Is feedback reviewed before tuning?
* Is feedback tenant-scoped?
* Is feedback used for shared models or shared rules?
* Can feedback be rolled back?
* Are tuning changes regression-tested?
* Are false negatives monitored after tuning?
* Are false positives monitored after tuning?

### Evidence to Request

* Feedback workflow
* Tuning governance process
* Model or rule update procedure
* Regression test process
* Rollback process
* Metrics before and after tuning

## B.13 Privacy and Compliance

### Questions

* What personal data is collected?
* What regulated data may be captured?
* Are data processing terms available?
* Are subprocessors documented?
* Is data residency configurable?
* Are retention periods configurable?
* Is deletion supported?
* Is legal hold supported?
* Are privacy reviews performed for new AI features?
* Are customers notified of material data handling changes?

### Evidence to Request

* Privacy documentation
* Data processing agreement
* Subprocessor list
* Data residency documentation
* Retention and deletion policy
* Privacy impact assessment

## B.14 Validation and Testing

### Questions

* Does the vendor provide test cases?
* Can customers run adversarial validation?
* Can customers test hidden DOM behavior?
* Can customers test screenshot deception?
* Can customers test QR handoff?
* Can customers test delayed content?
* Can customers test Unicode spoofing?
* Can customers test model outage behavior?
* Can customers test redaction using seeded data?
* Are model and policy changes regression-tested?
* Are test results exportable?

### Evidence to Request

* Validation guide
* Test artifact examples
* Regression test process
* Change validation process
* Customer test support process

## B.15 Decision Criteria

A browser-safe AI vendor or internal platform is stronger when it can demonstrate:

* clear data inventory
* clear AI data flow
* redaction before sensitive use
* structured model output
* deterministic policy enforcement
* safe failure behavior
* replayable evidence
* SOC-useful alerts
* tenant isolation
* governed exceptions
* governed feedback
* red-team validation support
* auditability
* measurable outcomes

## B.16 Final Due-Diligence Principle

The safest evaluation rule is:

**Do not evaluate browser-safe AI by feature claims alone. Evaluate what it collects, what AI can influence, how evidence is protected, how decisions fail, how exceptions are governed, and how the control can be independently validated.**