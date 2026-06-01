---
layout: post
title: "Browser-Safe AI Systems, Part 34: Lab Architecture for Browser-Based AI Security Testing"
date: 2026-05-24
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, ai-security, browser-security, prompt-injection, red-team, adversary-emulation, detection-engineering, llm-security, lab-architecture]
---

# Browser-Safe AI Systems, Part 34: Lab Architecture for Browser-Based AI Security Testing

Part 33 moved this series from argument to validation.

That shift requires architecture.

A serious browser-AI training program cannot be a loose collection of prompts, screenshots, and model responses. It needs a lab architecture that makes every claim testable, every result reviewable, and every meaningful decision tied to evidence.

A browser-based AI security lab must be designed so that each test case produces evidence about what the browser loaded, what rendered, what changed, what entered model context, what the model returned, what policy decided, what enforcement occurred, and what an analyst could reconstruct.

The lab is not just a place to ask a model questions.

It is an evidence pipeline.

Its purpose is to make hostile browser content observable without letting that content become trusted instruction, executable policy, or uncontrolled test behavior.

In the current AI Browser Security Test Suite, this architecture is implemented as a workshop track rather than left as an abstract diagram. The local `ollama-webui` target provides the weak controlled surface. Playwright, Chromium, curl, jq, `rg`, `sha256sum`, OWASP ZAP, mitmproxy, and mitmdump form the practical evidence path. The workshop documents and runners preserve browser source, DOM, visible text, screenshots, frame trees, timing observations, proxy evidence, model-bound context reviews, artifact manifests, SHA256 indexes, and reviewer archives where each lab requires them.

The architecture still has maturity boundaries. Lab 11 is an initial working exception workflow lab and is explicitly marked for future Playwright evidence capture integration and target-backed exception workflow gating. Classroom timing validation and instructor rehearsal are also release-hardening tasks. That is the correct posture: current status should be recorded, not hidden.

## Why Architecture Matters

Browser-based AI security testing fails when the lab is poorly designed.

The most common failure is testing only the model response. A tester loads a page, asks a model for a verdict, takes a screenshot of the answer, and treats that as evidence. That is not enough. It does not show what the browser rendered, what the DOM contained, what context entered the model, or whether policy was applied outside the model.

Another failure is missing browser evidence. A result that lacks DOM snapshots, rendered text, screenshots, frame context, timing records, or redirect metadata cannot support a strong conclusion. It may show that something happened, but not why.

A weak lab also fails to distinguish trusted instruction from untrusted page content. That distinction is central to browser-based AI security testing. Hostile browser content must be treated as evidence, not as authority.

Repeatability is another failure point. If the lab does not capture test case identifiers, target version, browser version, model version, harness version, policy version, and artifact hashes, it cannot support retesting after a model, browser, policy, or control change.

A lab without an artifact manifest produces fragile evidence.

A lab without deterministic policy turns the model into the control plane.

A lab without analyst review produces output that may be technically interesting but operationally weak.

Weak lab design produces weak conclusions.

## Architecture Principles

The lab architecture is built around explicit design principles.

### Local First

The default target should be local or lab-owned.

Local-first design reduces legal, ethical, and operational risk. It also makes tests repeatable. A lab that depends on live third-party content, third-party users, or uncontrolled external infrastructure cannot provide stable evidence for core training cases.

This does not mean browser-based AI security testing can never be applied to real products. It means product testing requires authorization, defined scope, rules of engagement, and evidence controls. The training lab should not depend on that.

### Authorized Only

Every test must operate within an explicit authorization boundary.

The lab should make it difficult to accidentally test systems outside scope. URLs, targets, browser profiles, test data, and network assumptions should be controlled. The architecture should not encourage opportunistic testing against real services.

This prevents the lab from becoming an unauthorized scanning or abuse platform.

### Synthetic Probes Only

The lab should use synthetic browser artifacts, seeded data, and inert files.

Synthetic probes allow the tester to study risk patterns without collecting real credentials, targeting real users, or creating operational harm. The point is to validate control behavior, not to run real phishing operations or exploit third-party systems.

The probe should be safe. The failure mode should still be real.

### Browser Evidence Before Model Interpretation

Evidence must be captured before the model interprets the page.

The browser is the observation surface. A lab that sends content directly to a model before preserving browser state loses the ability to inspect what happened. DOM, rendered text, screenshots, frames, redirects, timing, and metadata should be collected as independent artifacts.

The model output is a later artifact, not the first source of truth.

### Explicit Trust Boundaries

The architecture must label and preserve trust boundaries.

Browser content is untrusted. Model output is untrusted until validated. Analyst notes are commentary unless tied to canonical artifacts. Policy decisions must be explainable without depending on free-form model language.

Without explicit trust boundaries, untrusted page content can become instruction, and model output can become policy.

### Deterministic Policy Outside the Model

The model may classify, summarize, extract, or score.

It must not own the final decision.

Final decisions such as allow, block, warn, escalate, or record-only should be made by deterministic policy outside the model. That policy should accept constrained inputs, reject malformed model output, and produce reviewable decisions.

This prevents the model from becoming an unbounded policy engine.

### Immutable Artifact Capture Where Practical

Artifacts should be written once and referenced by manifest.

Where practical, the lab should preserve raw evidence rather than rewriting it during analysis. Derived artifacts can be generated later, but canonical inputs should remain stable.

Hashes should be used to support integrity checks and retesting.

### Reproducible Test Runs

A lab run should be reproducible enough that another tester can review the same case, inspect the same artifacts, and challenge the same conclusion.

Model nondeterminism may still exist. That does not excuse nondeterministic lab design. The target, test case, browser, harness, policy, and artifacts should remain controlled and versioned.

### Safe Failure Handling

The lab should fail closed in its own workflow.

If evidence capture fails, the run should be marked incomplete. If model output validation fails, policy should not accept the output as authoritative. If the target is not in scope, the run should stop.

A safe lab does not silently continue after losing evidence.

### Analyst-Readable Output

A report should be readable by a human reviewer.

The output should not require someone to reverse engineer the harness to understand the finding. The report should show scope, inputs, artifacts, model response, validation result, policy decision, enforcement simulation, and evidence gaps.

This matters because browser-based AI security testing is not complete until a human can review and challenge the result.

### Versioned Test Cases

Test cases should have stable identifiers and versions.

A test case should not be an ad hoc prompt saved in someone’s shell history. It should describe the objective, inputs, expected evidence, expected policy behavior, safety assumptions, and retest conditions.

Versioned test cases allow regression testing.

### Separation Between Target, Harness, Model, and Evidence Store

The lab should separate the controlled target, browser automation harness, model interface, policy engine, and evidence store.

That separation reduces confusion about responsibility. The target provides observable behavior. The harness drives and records the browser. The model produces untrusted output. The policy engine makes deterministic decisions. The evidence store preserves artifacts.

This prevents the architecture from collapsing into a single opaque demo.

## High-Level Architecture Diagram

```text
+---------------------------+
|  Versioned Test Case      |
|  manifest, objective,     |
|  safety scope, expected   |
|  evidence, expected       |
|  policy behavior          |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Controlled Lab Target    |
|  local or lab-owned       |
|  inspectable browser-AI   |
|  application or page set  |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Browser Automation       |
|  Runner                   |
|  controlled browser       |
|  session, profile, timing |
+-------------+-------------+
              |
              v
+-------------+---------------------------------------------+
|  Evidence Collectors                                      |
|                                                           |
|  +-------------------+  +-------------------------------+ |
|  | DOM Snapshot      |  | Rendered Text                 | |
|  +-------------------+  +-------------------------------+ |
|  +-------------------+  +-------------------------------+ |
|  | Screenshot        |  | Frame Tree                    | |
|  +-------------------+  +-------------------------------+ |
|  +-------------------------------------------------------+ |
|  | Network, Redirect, Timing, and State-Change Metadata | |
|  +-------------------------------------------------------+ |
+-------------+---------------------------------------------+
              |
              v
+-------------+-------------+
|  Context Builder          |
|  labels untrusted page    |
|  content, preserves       |
|  instruction boundary     |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Local Model Interface    |
|  controlled model access  |
|  classification or        |
|  summarization only       |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Model Output Validator   |
|  schema checks, parsing,  |
|  constraint enforcement,  |
|  malformed output reject  |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Deterministic Policy     |
|  Engine                   |
|  allow, block, warn,      |
|  escalate, record-only    |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Enforcement Simulator    |
|  safe local outcome       |
|  simulation               |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Artifact Store           |
|  raw artifacts, derived   |
|  artifacts, hashes,       |
|  manifest                 |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Structured Report        |
|  Generator                |
|  markdown, summaries,     |
|  evidence references      |
+-------------+-------------+
              |
              v
+-------------+-------------+
|  Analyst Review Workflow  |
|  inspect, challenge,      |
|  reproduce, retest        |
+---------------------------+
```

## Current Workshop Mapping

The implemented workshop maps the architecture into concrete lab responsibilities:

| Architecture Responsibility | Current Workshop Expression |
|---|---|
| Controlled target | The deliberately weak local `ollama-webui` target on loopback |
| Browser automation | Playwright and Chromium runners for browser-observed evidence |
| Direct and proxied HTTP evidence | curl, mitmdump or mitmproxy, OWASP ZAP passive review where selected |
| Evidence integrity | `artifact-manifest.json`, `SHA256SUMS.txt`, reviewer archives, and checksums |
| Trust-boundary review | model-bound context review artifacts and marker-provenance notes |
| Deterministic policy review | Lab 10 verdict-policy simulator and target-backed policy gate artifact |
| Capstone integration | Lab 12 deterministic package plus target-backed live evidence wrapper |

This mapping matters because a methodology article can sound complete while the implementation remains vague. The current suite is intentionally more specific: each lab must say what evidence it expects, what tools produce it, what safety boundary applies, and what the result does not prove.

## Component Model

### Controlled Lab Target

The controlled lab target is the intentionally inspectable environment where browser-based AI security behavior can be observed safely.

In this project, the local Ollama Web UI target provides a weak, local, browser-based AI application suitable for learning and validation. It should not be described as a production-secure product or a hardened assistant. Its value is that it is inspectable, local, and controlled.

The lab target exists to produce observable browser behavior. It should allow the tester to load synthetic artifacts, inspect browser state, and evaluate how content can move from page to model context.

A good lab target should be easy to reset. It should not contain real credentials, real user data, or dependencies on third-party systems for core tests.

### Browser Automation Runner

The browser automation runner drives the browser session.

It loads test pages, controls timing, captures state, and avoids relying on manual observation. Manual testing still has value, but a training lab needs repeatable browser behavior.

The runner should control the browser profile, viewport, target URL, test timing, and evidence capture sequence. It should record browser and automation versions. It should produce a run directory with all artifacts for that test case.

Tools such as [Playwright](https://playwright.dev/) are useful here because they support browser automation, screenshots, traces, network inspection, and DOM-oriented debugging workflows. The specific tool can change, but the architectural responsibility remains the same.

### Evidence Collectors

Evidence collectors preserve what the browser saw and did before model interpretation becomes part of the record.

#### DOM Collector

The DOM collector captures the browser’s document state.

This is not the same as downloading raw HTML. The DOM can change after scripts execute. The collector should preserve enough structure to support later review, especially when visible content and underlying document state diverge.

#### Rendered Text Collector

The rendered text collector captures what the browser exposes as visible or user-facing text.

This helps compare raw source, DOM state, and rendered state. Differences between these views are important in browser-based AI security testing because model-facing extraction may not match what a user sees.

#### Screenshot Collector

The screenshot collector captures visual evidence.

Screenshots matter because browser risk can be visual. Brand impersonation, QR handoffs, visual spoofing, fake warnings, and layout manipulation may not be represented accurately in text extraction alone.

A screenshot is not complete evidence by itself. It becomes useful when correlated with DOM, frame, redirect, and timing artifacts.

#### Frame-Tree Collector

The frame-tree collector captures parent and child frame relationships.

Nested frames can change risk interpretation. A parent page may appear benign while a child frame carries the relevant content. If the lab loses frame source, per-frame URL, or frame hierarchy, it may lose the evidence needed to understand the case.

#### Redirect and Network Metadata Collector

The redirect and network metadata collector records navigation behavior.

This does not need to become a full packet capture for every lab. The minimum useful record should include requested URL, final URL, redirect chain, relevant response metadata, and network events needed to explain the browser state.

This collector is especially important when a visible page is only one step in a browser-mediated workflow.

#### Timing and State-Change Collector

The timing and state-change collector records when evidence was captured and whether content changed after initial load.

Delayed content can create false confidence. A page that appears safe at first render may change after a timer, script event, redirect, user gesture, or asynchronous fetch. The lab should support before and after capture where timing matters.

### Context Builder

The context builder determines what content is allowed to enter the model context.

This is a critical trust boundary.

The context builder should label browser-derived content as untrusted. It should preserve separation between system instructions, test instructions, policy context, and page content. It should avoid merging hostile page text into trusted instructions.

The output of the context builder should be saved as an artifact. Without that artifact, a reviewer cannot determine what the model actually received.

### Local Model Interface

The local model interface provides controlled model access.

The model can classify, summarize, extract, or compare evidence. It can help test how browser-derived content affects AI-assisted workflows. It can also demonstrate how brittle the pipeline becomes when untrusted content is not labeled or constrained.

The model must not be the policy authority.

In this lab architecture, model output is an input to validation and policy. It is not a final security decision.

### Model Output Validator

The model output validator parses and constrains model output.

It should reject malformed output. It should enforce schemas where structured output is expected. It should separate explanation text from machine-consumable fields. It should fail safely when the model returns ambiguous or unsupported content.

This maps directly to the problem described by the [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/), where prompt injection and improper output handling are model-application risks that must be addressed before downstream use.

A validator does not make the model trustworthy. It reduces the chance that free-form model output becomes uncontrolled application behavior.

### Deterministic Policy Engine

The deterministic policy engine makes final decisions.

It should accept constrained inputs from the validator and explicit test policy. It should produce decisions such as allow, block, warn, escalate, or record-only. It should log the rule, input fields, decision, and reason.

The policy engine must be outside the model.

This is one of the most important design constraints in browser-based AI security testing. If the model owns the policy decision, the lab is testing the model’s current behavior, not the security control plane.

### Enforcement Simulator

The enforcement simulator records what would happen if a policy decision were enforced.

In a training lab, enforcement should be simulated safely. The simulator can record outcomes such as warning shown, navigation blocked, analyst escalation created, report generated, or record-only event saved.

It should not take destructive actions. It should not affect real users. It should not modify third-party systems.

The point is to test decision flow, not to create operational impact.

### Artifact Store

The artifact store preserves canonical evidence.

It should store raw and derived artifacts in a run directory. It should include a manifest with filenames, purposes, timestamps, and hashes. It should preserve enough context for review and retest.

The artifact store is the difference between a demonstration and evidence.

If an artifact is missing, the report should say so.

### Structured Report Generator

The structured report generator turns artifacts into a readable record.

The report should include scope, target, test case, versions, evidence summary, model context, model output, validation result, policy decision, enforcement simulation, failures, gaps, and retest notes.

The report should reference artifacts rather than replacing them.

A report that only contains narrative conclusions is weak. A report that links conclusions to preserved artifacts is useful.

### Analyst Review Workflow

The analyst review workflow is the human validation layer.

An analyst should be able to inspect artifacts, challenge conclusions, compare expected and actual behavior, identify evidence gaps, and rerun the test after changes.

This matters because the final consumer of browser-based AI security testing is often not the model, and not the test harness. It is a human responsible for deciding whether a control can be trusted.

## Trust Boundaries

The lab must assume that browser content is hostile.

It must also assume that model output is untrusted until validated.

The main trust boundaries are:

### Hostile Browser Content and Test Harness

The target page, rendered content, DOM, metadata, frames, redirects, and timing behavior are evidence. They are not trusted instructions.

The harness should capture this content without letting it alter test control flow outside expected browser behavior.

### Test Harness and Model Context

The harness must not blindly forward browser content to the model as if it were instruction.

The context builder should label browser-derived content, preserve source fields, and separate page evidence from system or test instructions.

### Model Output and Policy Decision

Model output must pass through validation before policy consumes it.

The policy engine should reject missing, malformed, unsupported, or ambiguous model output. Free-form language should not become a machine decision.

### Policy Decision and Enforcement Simulation

Policy decisions should feed a safe enforcement simulator.

The simulator should record outcomes without touching real users, real credentials, or third-party systems. This preserves safety while still testing the control path.

### Evidence Store and Report Generator

The report generator should reference canonical artifacts.

It should not silently rewrite evidence, omit missing artifacts, or convert uncertainty into certainty. The report is an interpretation layer. The artifact store is the evidence layer.

### Analyst Notes and Canonical Artifacts

Analyst notes are valuable, but they are not canonical evidence by themselves.

The lab should distinguish reviewer interpretation from preserved artifacts. A reviewer should be able to say, “I disagree with the conclusion,” and still inspect the same evidence.

## Data Flow

A normal lab run should follow a controlled data flow.

1. Select the test case.

2. Prepare the local lab target.

3. Launch a controlled browser session.

4. Capture baseline browser state.

5. Load the synthetic browser artifact.

6. Capture DOM, rendered text, screenshot, frames, redirects, timing, and metadata.

7. Build model context with explicit untrusted-content labels.

8. Query the local model or model interface.

9. Validate model output.

10. Apply deterministic policy.

11. Simulate enforcement.

12. Save artifacts.

13. Generate a structured report.

14. Review evidence.

15. Retest after changes.

The ordering matters.

Browser evidence should exist before model interpretation. Model output should be validated before policy. Policy should be applied before enforcement simulation. Reports should be generated from artifacts, not from memory.

## Artifact Requirements

| Artifact | Purpose | Required For | Failure If Missing |
|---|---|---|---|
| Test case manifest | Defines objective, scope, inputs, expected evidence, and expected decision behavior | Reproducibility and review | The run becomes an ad hoc demonstration |
| Browser version | Records the browser environment | Retesting and browser-specific behavior analysis | Browser-dependent results cannot be explained |
| Model version | Records the model under test | Retesting and model behavior comparison | Model changes cannot be distinguished from harness changes |
| Harness version | Records the test harness state | Reproducibility | Test logic changes cannot be tracked |
| Raw HTML | Preserves initial source material where applicable | Source versus DOM comparison | Source-level evidence is unavailable |
| DOM snapshot | Captures browser document state | DOM and rendered-state analysis | Script-mutated content cannot be reviewed |
| Rendered text | Captures user-facing text extraction | Comparing visible text to model-bound context | The reviewer cannot determine what text was visible or extracted |
| Screenshot | Preserves visual state | Visual deception and analyst review | The visual risk cannot be reconstructed |
| Frame tree | Preserves nested browsing context | iframe and origin analysis | Frame source and hierarchy are lost |
| Redirect chain | Records navigation path | Link and handoff analysis | Final state cannot be connected to prior navigation |
| Network metadata summary | Records relevant browser network behavior | Explaining loaded resources and redirects | Important browser behavior may be invisible |
| Timing record | Records capture sequence and state changes | Delayed content testing | Time-dependent behavior cannot be reproduced |
| Model context | Shows what entered the model | Trust boundary review | The reviewer cannot tell what the model saw |
| Raw model output | Preserves model response | Validation and comparison | Validator and policy behavior cannot be audited |
| Validation result | Shows parsing and schema outcome | Model-output handling review | Malformed output may be silently accepted |
| Policy decision | Records deterministic decision | Control-plane review | The final decision cannot be explained |
| Enforcement simulation result | Shows safe outcome | End-to-end control flow | Decision impact is unclear |
| Analyst notes | Captures human review | Review and challenge process | Human interpretation is lost |
| Report markdown | Provides readable summary | Communication and audit trail | Results remain scattered across artifacts |
| Artifact manifest with hashes | Provides inventory and integrity support | Evidence integrity and retest | Artifacts cannot be verified reliably |

## Reproducibility Requirements

A browser-AI lab run is reproducible when another tester can identify the same test case, prepare the same target, run the same harness, inspect the same classes of artifacts, and challenge the same conclusion.

Reproducibility requires pinned test case identifiers, stable synthetic inputs, local target version, browser version, model name and version, harness version, deterministic policy file, artifact hashes, and clear run directory naming.

The lab should not have a hidden dependency on live third-party content for core tests. It should not require uncontrolled external network access to produce basic evidence. It should not depend on real accounts, real victims, real credentials, or real phishing infrastructure.

Model nondeterminism can still exist.

That is not a reason to abandon reproducibility.

It means the surrounding pipeline must become more disciplined. The lab should preserve inputs, context, model output, validation result, policy decision, and artifacts so that changes in model behavior can be observed rather than guessed.

## Safety Controls

The architecture must prevent the lab from becoming an abuse toolkit.

The default target must be local or lab-owned. The data must be synthetic. The credentials must be seeded test values only, if credentials are needed at all. The lab must not collect real credentials, steal cookies, extract tokens, deploy malware, perform destructive actions, run real phishing operations, scan third-party systems, or provide bypass guidance against real products.

Enforcement should be simulated safely.

Authorization boundaries should be visible in the test case manifest and harness configuration.

Failure modes should be safe. If the target is not approved, stop. If evidence capture fails, mark the run incomplete. If model output is malformed, reject it. If policy cannot decide, escalate or record incomplete status rather than inventing certainty.

Seriousness does not require recklessness.

A stronger lab is safer, not louder.

## Relationship to Existing Security Guidance

This lab architecture should align with established security work without pretending to replace it.

The [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) provides disciplined structure for web application security testing. It remains relevant because browser-based AI security testing still depends on web testing fundamentals: authentication, authorization, session behavior, input handling, client-side behavior, deployment configuration, and application logic.

The [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) helps frame model-application risks such as prompt injection, improper output handling, excessive agency, and related failures in systems that place LLMs into application workflows.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) helps frame governance, mapping, measurement, and management of AI risks. For this lab, that means the architecture must support measurement, not just demonstration.

[MITRE ATLAS](https://atlas.mitre.org/) provides a knowledge base of adversary tactics and techniques against AI-enabled systems. Its value here is not that every lab case must map directly to a technique. Its value is that adversarial AI behavior should be studied as part of a system, not as isolated model trivia.

[Playwright](https://playwright.dev/docs/trace-viewer) and similar browser automation tools help implement evidence capture. Playwright’s trace viewer documentation describes recorded traces that allow review of actions, logs, network activity, screenshots, and DOM snapshots. Its [screenshot documentation](https://playwright.dev/docs/screenshots) supports visual artifact capture. The lab architecture should not depend on one tool forever, but the evidence requirements align well with this class of browser automation capability.

The point is not to turn Part 34 into a literature review.

The point is to show that browser-based AI security testing can inherit discipline from web testing, AI risk management, adversarial AI knowledge bases, and browser automation practice.

## What This Lab Is Not

This lab is not a prompt-injection trick collection.

It is not a phishing kit.

It is not a browser exploitation framework.

It is not a malware lab.

It is not a tool for unauthorized vendor testing.

It is not a product benchmark unless scope, methodology, authorization, and evidence are defined.

It is not a replacement for web application security testing.

It is an architecture for controlled browser-based AI security testing.

## Quality Bar for a Lab Run

A high-quality lab run must execute a defined test case.

It must capture browser evidence before model interpretation.

It must preserve trust boundaries.

It must record exact inputs and outputs.

It must validate model output.

It must apply deterministic policy.

It must simulate enforcement safely.

It must produce a structured report.

It must include artifact hashes.

It must support analyst review.

It must support retest.

A run that only shows a model response is not enough.

A run that only shows a screenshot is not enough.

A run that cannot show what entered model context is not enough.

A run that cannot explain the policy decision is not enough.

A run that cannot be reviewed by another analyst is not enough.

## Failure Examples Without Payloads

The following failure classes are useful because they test the architecture without requiring unsafe payload publication.

A page includes hidden DOM content. The context builder passes that content to the model without labeling it as untrusted page content. The model treats the content as instruction-like context. The lab should detect that the trust boundary failed.

A screenshot shows a stronger risk signal than the extracted text. The model receives only text and misses the visual risk. The lab should show that evidence capture and model context did not represent the same browser state.

An iframe contains the relevant risky content, but the evidence package stores only the parent URL. The analyst cannot determine where the content came from. The lab should fail the run for incomplete frame evidence.

Delayed content appears after the first scan. The initial capture looks safe. A later capture shows a different state. The lab should record timing and state change rather than treating the first capture as final.

Model output does not match the expected schema. The validator rejects it. If policy still accepts the free-form answer, the lab should flag policy bypass of validation.

A policy decision relies on natural-language model explanation instead of constrained fields. The lab should flag the model as acting beyond its role.

The report says a test passed but omits raw artifacts. The analyst cannot reconstruct the conclusion. The lab should treat that as a reporting failure.

The analyst cannot reproduce the conclusion after a browser, model, or policy update because versions were not recorded. The lab should treat that as a reproducibility failure.

None of these examples require publishing exploit strings.

They require disciplined evidence capture.

## Closing Thesis

Part 34 defines the lab architecture required for serious browser-based AI security testing.

The purpose is not to make models look foolish.

The purpose is to test whether the full browser-AI control plane can observe hostile content, preserve evidence, constrain model behavior, enforce deterministic policy, and produce reviewable security outcomes.

A serious lab does not start with a prompt.

It starts with architecture.

It captures the browser.

It preserves the boundary between evidence and instruction.

It treats model output as untrusted.

It keeps policy deterministic.

It makes every important decision reviewable.

That is the standard this project should hold itself to.