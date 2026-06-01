---
layout: post
title: "Browser-Safe AI Systems, Part 39: Vendor Due-Diligence Testing for Browser-Based AI Controls"
date: 2026-05-24
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, ai-security, browser-security, red-team, detection-engineering, vendor-risk, due-diligence, llm-security, security-architecture]
---

# Browser-Safe AI Systems, Part 39: Vendor Due-Diligence Testing for Browser-Based AI Controls

Part 38 defined analyst usefulness as an evidence quality and workflow problem.

The next question is how a buyer, security architect, SOC lead, procurement security reviewer, or vendor-risk reviewer should evaluate vendor claims about browser-based AI controls.

A vendor claim about browser-based AI protection is not enough.

A claim that says “AI detects malicious pages” does not tell the customer what the product observes. It does not tell the customer whether the product captures DOM evidence, rendered text, screenshots, frame trees, redirect metadata, timing records, model context, model output, validation results, deterministic policy decisions, or analyst-reviewable reports.

It does not tell the customer whether untrusted browser content is labeled.

It does not tell the customer whether model output is constrained.

It does not tell the customer whether deterministic policy owns the final decision.

It does not tell the customer whether analysts can reconstruct events.

Vendor due diligence for browser-based AI controls must be evidence-driven.

A vendor claim is meaningful only when the customer can understand what the product observes, what enters model context, how model output is constrained, how deterministic policy is enforced, what evidence is preserved, how analysts can review decisions, and how the control behaves under safe synthetic test cases.

## Defining Vendor Due Diligence for Browser-Based AI Controls

Vendor due diligence for browser-based AI controls is the structured evaluation of a vendor’s security claims, architecture, evidence handling, model-context boundaries, output validation, deterministic policy controls, privacy protections, analyst workflows, and retestability.

It is not a demo review.

The public AI Browser Security Test Suite can support this mindset, but it must be used carefully. It is a local training and control-validation harness, not an authorization slip to test vendor infrastructure. Vendor testing requires written scope, vendor-approved environments or lab-owned reproductions, rules of engagement, and evidence-handling controls.

The useful transfer from the suite to due diligence is the artifact standard: ask what the product observes, what enters model context, how model output is constrained, what owns policy, what evidence is preserved, what analysts can inspect, and how the customer can retest after model, browser, policy, or vendor changes.

It is not blind trust in an AI verdict.

It is not a generic questionnaire alone.

It is not satisfied by a slide that says the product uses AI.

Due diligence must include evidence, architecture, testing, and operational review.

The reviewer should be able to ask:

* What does the control observe?
* What browser artifacts does it preserve?
* What content enters model context?
* How is browser-derived content labeled as untrusted?
* How is model output validated?
* What owns the final decision?
* How are policy decisions enforced?
* What can analysts inspect?
* What can customers retest?
* What happens when evidence is incomplete?
* What happens when the model is uncertain?
* What happens when the model output is malformed?
* What data is retained?
* What data is sent to models?
* How is tenant isolation enforced?

A browser-based AI control sits close to sensitive browser activity. That makes due diligence more than a procurement checkbox.

It is a security architecture review.

## Why Ordinary Vendor Questions Are Insufficient

Ordinary vendor questions are often too weak for browser-based AI controls.

A generic questionnaire may ask whether the vendor uses encryption, performs access control, has incident response procedures, supports logging, and follows secure development practices. Those questions still matter. They are not enough.

Browser-based AI controls introduce pipeline-specific questions.

A vendor may describe AI capability without evidence detail.

A vendor may conflate model verdict with policy decision.

A vendor may not explain what browser artifacts are captured.

A vendor may not disclose how model context is built.

A vendor may not preserve enough evidence for SOC use.

A vendor may not support safe customer-led validation.

A vendor may not define failure modes.

A vendor may not explain privacy, retention, and tenant isolation for browser artifacts.

A vendor may say the product “understands page intent,” but not explain whether that conclusion comes from DOM evidence, rendered text, screenshot analysis, URL metadata, iframe context, model classification, reputation data, deterministic policy, or a combination of signals.

That ambiguity matters.

Browser-based AI controls require pipeline-level due diligence.

The customer must evaluate the control path from browser observation to evidence preservation, model context, model output, validation, deterministic policy, enforcement, reporting, and analyst review.

## Vendor Claim Categories

| Vendor Claim | What It Could Mean | Due-Diligence Question | Evidence Required | Risk If Unverified |
|---|---|---|---|---|
| AI detects malicious pages | Model classifies browser content as risky | What browser evidence is used for classification? | DOM, rendered text, screenshot, URL metadata, model context, model output, policy decision | Customer may trust a verdict without knowing what was observed |
| AI understands page intent | Model or rule system infers user-facing purpose | How is intent derived and validated? | Evidence views, context builder details, validation result, policy mapping | Marketing language may hide weak or unreviewable logic |
| AI blocks phishing | Control prevents access or warns users | What signal triggers blocking and who owns the decision? | Policy rules, enforcement record, model output, validation result | Model may be treated as policy authority |
| AI analyzes screenshots | Visual state is used as evidence | Are screenshots preserved and reviewable? | Screenshot artifact, capture timing, viewport or full-page details | Visual claims may be unverifiable |
| AI inspects DOM | Document state contributes to analysis | Is live DOM captured, stored, and correlated with rendered state? | DOM snapshot, rendered text, capture timing | Hidden or script-mutated content may be mishandled |
| AI protects against prompt injection | Control handles untrusted content entering AI workflows | How are untrusted browser inputs separated from trusted instructions? | Model context artifact, trust labels, context-builder documentation | Page content may become trusted instruction |
| AI summarizes browser risk | Model generates analyst-facing explanation | Does the summary reference preserved evidence? | Report markdown, artifact links, raw model output | Summary may replace evidence instead of explaining it |
| AI reduces false positives | Control improves alert precision | What evidence supports false positive reduction? | False positive review samples, policy changes, evidence packages | Claim may be statistical or anecdotal without operational proof |
| AI improves SOC triage | Alerts become more useful to analysts | Can analysts reconstruct the event and challenge the model? | Analyst report, artifacts, policy decision, uncertainty flags | SOC may receive confident but unreviewable alerts |
| AI adapts to new threats | Model or service updates over time | How are changes controlled and retested? | Change logs, model versioning, retest results | Behavior may drift without customer visibility |
| Policy is configurable | Customers can tune outcomes | What can policy change, and what remains model-driven? | Policy documentation, test results, enforcement records | Configuration may not control the actual decision path |
| Customer data is protected | Browser artifacts are handled securely | What is collected, retained, redacted, and sent to models? | Data-flow documentation, retention policy, tenant controls | Sensitive browser content may be exposed or retained unnecessarily |
| Alerts are explainable | Analyst can understand why an event fired | Does explanation reference canonical artifacts? | Report, artifact manifest, model context, policy decision | Explanation may be a model narrative without evidence |

## Architecture Questions

A buyer should ask architecture questions before accepting claims about browser-based AI protection.

What browser artifacts are captured?

Is raw HTML captured?

Is live DOM captured?

Is rendered text captured?

Are screenshots captured?

Is frame-tree evidence captured?

Are redirects captured?

Is timing captured?

What evidence enters model context?

How is untrusted browser content labeled?

How are system instructions separated from browser-derived content?

Is model output schema-validated?

What owns the final policy decision?

Can policy reject unsupported model claims?

Are enforcement actions deterministic?

Are artifacts hashed or otherwise integrity-tracked?

Can analysts inspect raw evidence?

Can customers retest after model or policy changes?

These questions are not academic.

They determine whether the customer is buying a security control, a model-assisted feature, or a black-box summary generator.

A mature vendor should be able to explain the control path in operational terms.

## Evidence Requirements for Due Diligence

| Evidence Area | Vendor Must Show | Customer Should Verify | Failure Signal |
|---|---|---|---|
| DOM evidence | Whether live DOM is captured and how it is stored or summarized | DOM evidence is available for reviewed events or test cases | Vendor cannot show what the document contained |
| Rendered text evidence | Whether user-visible or extractable text is captured | Rendered text can be compared to DOM and screenshot | Text evidence is absent or collapsed into model summary |
| Screenshot evidence | Whether screenshots are captured where relevant | Screenshot is preserved with timing and context | Visual claims cannot be reviewed |
| Frame-tree evidence | Whether nested frames are recorded | Parent and child frame relationships are preserved | Vendor loses nested content source |
| Timing evidence | Whether capture timing and state changes are recorded | Delayed content behavior can be reviewed | Vendor treats first capture as final state |
| Redirect metadata | Whether navigation path and final URL are recorded | Redirects and final destination can be reconstructed | Vendor provides only final verdict |
| Model context artifact | What evidence was sent to the model | Browser-derived content is labeled untrusted | Customer cannot review what the model received |
| Raw model output | Model response before validation | Raw output is inspectable or summarized with caveats | Vendor hides model behavior |
| Validation result | How model output is parsed and constrained | Malformed or unsupported outputs are rejected | Free-form output reaches policy |
| Deterministic policy decision | Final decision owner and rule basis | Policy decision is recorded separately from model verdict | Model appears to own policy |
| Enforcement record | What action was taken or simulated | Action maps to policy, not unvalidated model output | Enforcement path is unclear |
| Analyst report | Human-readable review record | Report references artifacts and uncertainty | Report is narrative without evidence |
| Artifact manifest | Inventory of artifacts and integrity metadata | Required artifacts are listed with presence and hashes where practical | Evidence package is incomplete or unverifiable |
| Privacy and retention controls | What is collected, retained, redacted, and deleted | Controls match customer risk tolerance | Browser artifacts are retained without clear limits |
| Tenant isolation controls | How customer data is separated | Isolation is documented and testable | Cross-tenant exposure risk is unclear |
| Retest support | How customers retest after changes | Model, policy, browser, and harness versions are tracked | Control behavior cannot be compared over time |

## Testing With Safe Synthetic Cases

Customers can use safe synthetic browser-AI attack cases for vendor due diligence, but testing must be authorized.

The goal is not to publish bypass recipes.

The goal is to validate control properties.

Tests should use local, lab-owned, or vendor-approved environments. They should use inert markers and seeded data. They should not include real credential collection, malware, live phishing, token theft, cookie theft, destructive behavior, or third-party targeting.

Safe synthetic tests can verify whether the vendor control handles browser evidence correctly.

Useful objectives include:

* verify DOM versus rendered evidence capture
* verify screenshot correlation
* verify frame-tree preservation
* verify delayed-content handling
* verify model-context labeling
* verify model-output validation
* verify deterministic policy separation
* verify analyst report usefulness
* verify artifact completeness
* verify retestability

A vendor that supports this type of safe validation is easier to evaluate than a vendor that only offers a polished demo.

A mature vendor should welcome controlled validation.

It should also insist on scope, authorization, and safe test design.

## Due-Diligence Workflow

A disciplined due-diligence workflow should be explicit.

1. Define the business and security use case.

2. Define scope and authorization.

3. Identify vendor claims to validate.

4. Request architecture documentation.

5. Request evidence samples.

6. Request privacy, retention, and tenant-isolation details.

7. Request model-context and output-handling details.

8. Request policy and enforcement documentation.

9. Define safe synthetic validation cases.

10. Execute tests only in authorized environments.

11. Review artifacts.

12. Compare vendor claims to observed behavior.

13. Review SOC usefulness.

14. Document gaps and compensating controls.

15. Define acceptance, rejection, pilot, or retest decision.

This workflow prevents the review from becoming a demo reaction.

It gives the customer a path from claim to evidence.

## SOC and Analyst Requirements

A vendor must provide evidence that supports analyst work.

SOC usefulness requires evidence-rich alerts.

It requires artifact links.

It requires screenshot or visual evidence where relevant.

It requires DOM or rendered-text details where relevant.

It requires frame context where relevant.

It requires model context transparency.

It requires raw or summarized model output with caveats.

It requires validation result.

It requires deterministic policy result.

It requires severity and confidence explanation.

It requires uncertainty and missing-evidence flags.

It requires retest identifiers.

It requires exportable evidence.

A vendor that cannot support analyst review may still have a useful feature.

The customer should not treat it as a mature security control.

A feature that helps a user make a decision is not the same as a SOC-ready control. SOC-ready controls need evidence, traceability, triage support, escalation support, suppression logic, and retestability.

## Privacy, Retention, and Tenant Isolation

Browser-AI controls may process sensitive browser artifacts.

Those artifacts can include screenshots, DOM, URLs, rendered text, file names, user context, SaaS page content, authentication-adjacent workflows, and analyst notes.

This creates privacy, retention, and tenant-isolation questions.

The review should ask:

* What is collected?
* What is redacted?
* What is sent to models?
* Are models local, vendor-hosted, customer-hosted, or third-party?
* Is customer data used for training?
* What is retained?
* For how long?
* Who can access artifacts?
* How is tenant isolation enforced?
* How are logs protected?
* Can customers disable or scope artifact capture?
* Can customers export and delete evidence?
* Are screenshots treated differently from text artifacts?
* Are URLs retained?
* Are page titles retained?
* Are file names retained?
* Are user identifiers retained?
* Are analyst notes retained with the event?
* Can retention settings vary by policy, tenant, group, or event type?
* What happens when evidence is redacted before analyst review?
* What happens when redaction removes required evidence?

This is not legal advice.

It is technical due diligence.

A control that captures rich browser evidence can be valuable. It can also create sensitive evidence stores. Customers need to understand both sides.

## Failure Modes Vendors Should Disclose

Mature vendors should describe failure modes and safe defaults.

Important failure modes include:

* capture failure
* model timeout
* model uncertainty
* schema validation failure
* policy conflict
* missing screenshot
* missing DOM
* missing frame tree
* unsupported browser feature
* partial evidence
* offline mode
* excessive false positives
* suspected false negatives
* privacy redaction failure
* tenant-isolation concern

The reviewer should ask what happens in each condition.

Does the control fail open?

Does it fail closed?

Does it degrade to record-only?

Does it warn?

Does it escalate?

Does it suppress?

Does it mark evidence incomplete?

Does it notify analysts?

Does it preserve partial artifacts?

Does it block enforcement when evidence is missing?

A mature control should not silently convert uncertainty into confidence.

## Evaluation Decision Model

Vendor due diligence should end with a clear decision.

Possible outcomes include:

* acceptable for pilot
* acceptable with compensating controls
* acceptable for record-only mode
* needs further testing
* not suitable for enforcement
* not suitable for SOC workflow
* rejected due to evidence gaps
* rejected due to privacy or retention risk
* rejected due to unclear policy authority

Record-only mode can be an appropriate interim decision.

A product may preserve useful evidence while enforcement confidence is not yet mature. In that case, the customer may choose to collect evidence, evaluate alerts, and build confidence before enabling blocking or user-facing enforcement.

That is not a weak decision.

It is a disciplined one.

The wrong decision is treating an unreviewed AI verdict as an enforcement-ready control.

## Red Flags

Several red flags should slow or stop vendor acceptance.

The vendor cannot explain what enters model context.

The vendor treats model verdict as policy authority.

The vendor cannot provide raw or reviewable evidence.

The vendor cannot show how screenshots, DOM, frames, and redirects are handled.

The vendor cannot explain false positives or false negatives.

The vendor cannot support safe customer-led testing.

The vendor hides uncertainty.

The vendor cannot explain data retention.

The vendor cannot explain tenant isolation.

The vendor claims “AI understands intent” without evidence.

The vendor cannot support retesting after model changes.

The vendor does not separate marketing claims from testable behavior.

The vendor cannot explain what happens when the model times out.

The vendor cannot explain what happens when evidence capture fails.

The vendor cannot show how analysts challenge the verdict.

These red flags do not automatically prove the product is bad.

They do mean the customer lacks enough evidence to treat the product as a mature browser-based AI security control.

## Due-Diligence Questionnaire

### Architecture and Data Flow

What is the end-to-end data flow from browser observation to final enforcement decision?

Which components run on the endpoint, in the browser, in the customer environment, in the vendor cloud, or in third-party model infrastructure?

What browser artifacts are captured?

What artifacts are preserved?

What artifacts are only transient?

What data enters model context?

What data is excluded from model context?

How are browser-derived inputs labeled as untrusted?

What controls separate system instruction, customer policy, model context, and page content?

What versions are recorded for model, browser, policy, and product components?

### Browser Evidence Capture

Do you capture raw HTML?

Do you capture live DOM?

Do you capture rendered text?

Do you capture screenshots?

Do you capture frame-tree evidence?

Do you capture redirect chains?

Do you capture timing and state changes?

Do you capture URL metadata?

Do you capture per-frame URL and source information?

Can analysts inspect those artifacts?

Can customers export those artifacts?

Can customers configure which artifacts are collected?

What happens when an artifact cannot be captured?

### Model Context and Prompt Boundary

How is model context constructed?

What browser-derived content is included?

What browser-derived content is excluded?

How is untrusted browser content labeled?

How are system instructions protected from page content?

How are customer policy instructions protected from page content?

Can customers inspect model context?

Can customers inspect model prompt templates or equivalent context-building logic?

How do you prevent hidden, framed, or delayed content from being treated as trusted instruction?

What happens when context is truncated?

What happens when evidence views disagree?

### Model Output Validation

What output formats can the model produce?

Is model output schema-validated?

What happens when model output is malformed?

What happens when model output is ambiguous?

What happens when model output contains unsupported claims?

Can free-form explanation affect enforcement?

Can model confidence affect enforcement directly?

Are validation failures logged?

Can analysts inspect validation results?

### Policy and Enforcement

What owns the final decision?

Is final policy deterministic?

Can policy reject unsupported model claims?

Can policy operate without model output?

Can policy distinguish allow, block, warn, escalate, record-only, and incomplete evidence?

What enforcement actions are supported?

Can enforcement run in record-only mode?

How are policy decisions logged?

Can customers test policy behavior safely?

What happens when policy conflicts with model output?

### Analyst and SOC Workflow

What does an analyst see in an alert?

Can the analyst inspect screenshot evidence?

Can the analyst inspect DOM or rendered text evidence?

Can the analyst inspect frame-tree evidence?

Can the analyst inspect model context?

Can the analyst inspect raw or structured model output?

Can the analyst inspect validation results?

Can the analyst inspect deterministic policy decisions?

Does the alert identify uncertainty?

Does the alert identify missing artifacts?

Can the analyst export evidence?

Can the analyst mark false positives and false negatives with evidence?

Can the analyst trigger retesting?

### Privacy, Retention, and Tenant Isolation

What browser artifacts are collected?

What artifacts may contain sensitive user or business data?

What is redacted before storage?

What is redacted before model use?

What is sent to vendor-hosted systems?

What is sent to third-party model providers, if anything?

Is customer data used for model training?

How long is evidence retained?

Can customers configure retention?

Can customers delete evidence?

How is tenant isolation enforced?

How is evidence access controlled?

How are analyst notes protected?

How are logs protected?

How are screenshots handled differently from text artifacts?

### Testing and Retesting

Can customers run safe synthetic test cases?

Can customers run tests in a lab-owned or vendor-approved environment?

Can customers test DOM versus rendered mismatch handling?

Can customers test screenshot correlation?

Can customers test frame-tree preservation?

Can customers test delayed-content handling?

Can customers test model-context labeling?

Can customers test model-output validation?

Can customers test deterministic policy separation?

Can customers test analyst report usefulness?

Can customers retest after model changes?

Can customers retest after policy changes?

Can customers retest after product updates?

### Failure Modes and Support

What happens if evidence capture fails?

What happens if screenshot capture fails?

What happens if DOM capture fails?

What happens if frame-tree capture fails?

What happens if model inference times out?

What happens if model output is malformed?

What happens if the model is uncertain?

What happens if policy cannot decide?

What happens if privacy redaction removes needed evidence?

What happens if offline mode is required?

How are false positives investigated?

How are false negatives investigated?

What artifacts are required for vendor support escalation?

### Governance and Change Management

How are model updates controlled?

How are policy updates controlled?

How are prompt or context-builder updates controlled?

How are evidence-capture changes controlled?

How are customer-facing changes communicated?

Can customers pin versions?

Can customers review release notes tied to detection behavior?

Can customers obtain test evidence for major changes?

How are regressions handled?

How are customer-specific policies protected across updates?

## Relationship to Authoritative References

Vendor due diligence for browser-based AI controls should align with established security discipline.

The [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) helps keep validation structured. Browser-based AI controls still depend on web security fundamentals, browser behavior, evidence, and repeatable testing.

The [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) helps frame model-context and output-handling due diligence. Prompt injection, insecure output handling, excessive agency, and overreliance are directly relevant when a vendor places AI inside a browser security workflow.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) helps connect vendor evaluation to governance, measurement, and risk management. Due diligence should produce measurable evidence, not only subjective confidence.

[MITRE ATLAS](https://atlas.mitre.org/) helps frame adversarial AI behavior at the system level. Browser-based AI control review should evaluate the pipeline, not only the model.

[Playwright](https://playwright.dev/) and similar browser automation tools help customers understand what browser evidence can be captured. Playwright documentation covers [screenshots](https://playwright.dev/docs/screenshots), [trace viewing](https://playwright.dev/docs/trace-viewer), and [frames](https://playwright.dev/docs/frames), which map directly to evidence expectations discussed in this series.

The purpose of referencing these sources is not decoration.

The purpose is to anchor due diligence in structured testing, model-application risk, AI governance, adversarial system thinking, and browser evidence capture.

## What Vendor Due Diligence Is Not

Vendor due diligence is not a product endorsement.

It is not a benchmark without scope and methodology.

It is not unauthorized testing.

It is not blind trust in a demo.

It is not blind trust in a model confidence score.

It is not a replacement for broader security architecture review.

It is not a replacement for privacy, legal, or procurement review.

It is not proof that a product is secure or insecure without evidence.

Vendor due diligence is a structured effort to separate testable security behavior from claims.

## Practitioner Quality Bar

A high-quality vendor due-diligence review should be strong enough that a security architect can understand the control boundary.

A SOC lead should be able to judge analyst usefulness.

A detection engineer should be able to identify required signals.

An incident responder should be able to understand escalation value.

A privacy reviewer should be able to identify browser artifact risks.

A procurement reviewer should be able to separate claims from evidence.

A future tester should be able to retest after vendor, model, browser, or policy changes.

That is the standard.

If the review cannot determine what the control observes, it is incomplete.

If the review cannot determine what enters model context, it is incomplete.

If the review cannot determine who owns policy, it is incomplete.

If the review cannot determine what evidence analysts can inspect, it is incomplete.

If the review cannot determine what is retained, it is incomplete.

If the review cannot support retesting, it is incomplete.

## Closing Thesis

Part 39 defines vendor due diligence for browser-based AI controls as an evidence-driven validation activity.

The question is not whether a vendor says it uses AI.

The question is what the control observes, what evidence it preserves, how it handles untrusted browser content, how it constrains model output, how deterministic policy is enforced, how analysts review events, and whether customers can retest the control safely.

A serious vendor review must move from claim to architecture.

From architecture to evidence.

From evidence to analyst usefulness.

From analyst usefulness to policy confidence.

From policy confidence to retestability.

That is how browser-based AI controls should be evaluated.