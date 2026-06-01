---
layout: post
title: "Browser-Safe AI Systems, Part 33: From Research Series to Evidence-Backed Training Program"
date: 2026-05-24
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, ai-security, browser-security, prompt-injection, phishing, red-team, soc, series, adversary-emulation, detection-engineering, secure-ai, llm-security]
---

# Browser-Safe AI Systems, Part 33: From Research Series to Evidence-Backed Training Program

The first phase of this series established the argument.

The next phase is where that argument is operationalized.

That phase now exists as a local workshop track in the AI Browser Security Test Suite. The current development state is no longer only a research idea or a loose set of helper scripts. It is a student-facing workshop sequence with a deliberately weak local `ollama-webui` target, safe synthetic markers, browser evidence capture, proxy evidence where relevant, artifact manifests, SHA256 indexes, and a capstone package.

A browser-based AI system should be tested as a security pipeline, not as a model feature. The model is only one component. The browser, DOM, rendered page, screenshots, iframes, extracted context, policy engine, enforcement decision, logs, and analyst evidence all matter.

That has been the central position of this series from the beginning: browser content is adversarial input, AI verdicts must be constrained, policy must remain outside the model, and important decisions must produce evidence that analysts, red teams, developers, and stakeholders can review.

This article marks the transition from research series to evidence-backed training program, and it should be read against that implementation state.

The goal is not to publish more opinions about prompt injection.

The goal is to build a practical learning path for cybersecurity professionals who need to test whether browser-based AI controls survive contact with adversarial browser content, while keeping the work local-only, synthetic-only, authorized-only, and reviewable.

## Current Implementation Baseline

The current suite uses three concrete layers.

First, the research series defines the security argument: browser content is untrusted input, AI output is advisory, deterministic policy owns control decisions, and evidence is mandatory.

Second, the local `ollama-webui` target gives the workshop a deliberately weak browser-based AI surface running on loopback. It is a training target, not a hardened product and not a production security claim.

Third, the AI Browser Security Test Suite turns the argument into labs. The workshop now includes Labs 00 through 12, with local evidence packages, first-party helpers, live evidence runners for most browser-evidence-heavy labs, and a target-backed capstone runner. The current maturity still has open release-hardening work, especially classroom timing validation and instructor rehearsal, and Lab 11 remains less mature than the fully browser-backed labs. Those caveats matter because this track is judged by evidence rather than ambition.

## Why a Lab Program Is Necessary

Reading about browser-AI risk is useful.

It is not sufficient.

A professional tester needs to observe the full chain:

browser artifact, rendered state, extracted context, model response, policy decision, enforcement outcome, evidence package, analyst review.

That chain is where the real failures happen.

A model might summarize a hostile page correctly but still influence a weak downstream decision.

A browser control might detect obvious visible text but miss hidden DOM content.

A screenshot workflow might capture the visible lure but lose the iframe context that explains where the content came from.

A system might block a page but fail to save enough evidence for a SOC analyst to understand the event.

A model might produce a confident verdict while the system loses track of the artifact that caused it.

That is why browser-based AI security cannot be validated by looking at model output alone.

The test target is the pipeline.

## The Intended Learner

This material is not written for someone encountering prompt injection for the first time.

The intended learner already understands web security, browser behavior, red-team methodology, application security, identity workflows, SOC evidence, incident review, and control validation.

They know that a convincing demo is not the same thing as a useful test.

They know that screenshots can mislead.

They know that DOM state and rendered state are not the same thing.

They know that a detection without evidence is a weak detection.

They know that a security decision that cannot be reconstructed will not survive serious review.

The intended learner needs a disciplined way to answer a harder question:

Can a browser-based AI security claim survive contact with hostile browser content, controlled evidence capture, repeatable testing, and analyst scrutiny?

That is the standard the current workshop track is built to meet.

## Training Philosophy

The lab program is built around several operating assumptions.

Do not trust the page.

Do not trust hidden browser content.

Do not trust the model verdict without evidence.

Do not let the model own policy.

Do not accept evidence that cannot be replayed.

Do not call a control effective until it has been tested against realistic browser artifact classes.

These are not slogans. They are test design requirements.

If hostile browser content can enter the model context, the test must show where it entered.

If a model verdict influences an enforcement decision, the test must show whether policy remained deterministic.

If a control claims to inspect browser state, the test must show whether it captured DOM, rendered text, screenshots, frame context, and state changes.

If a report claims that a page was malicious, the evidence must let another analyst reconstruct why.

## The Three-Layer Project Model

This project now has three connected layers.

### Layer 1: Research Series

The research series defines the threat model, defensive principles, test categories, governance concerns, and architecture expectations.

It explains why browser-based AI controls should treat web content, rendered text, hidden DOM, metadata, screenshots, QR handoffs, delayed content, user feedback, and exception requests as adversarial inputs.

It also defines the design position that AI should be treated as an untrusted classifier inside a controlled security pipeline.

### Layer 2: Local Lab Target

The local lab target gives the tester a controlled place to observe behavior.

The `ollama-webui` project is intentionally described as an insecure local lab application for chatting with models served by Ollama. It is explicitly not a secure product, not a hardened assistant, and not a production-ready AI coding environment. Its value is that it is weak, inspectable, browser-based, and local.

That matters.

A serious training program should not depend on attacking third-party systems. It should provide a lab surface where risk patterns can be demonstrated without collecting real credentials, abusing real users, or testing infrastructure outside the operator's scope.

### Layer 3: Test Suite and Evidence Harness

The AI Browser Security Test Suite is the executable validation layer.

It uses the local `ollama-webui` target as a deliberately weak, locally runnable browser-based LLM app for testing, prototyping, and demonstrating browser-AI security weaknesses safely. The intended review model is:

research claim, safe synthetic probe, browser evidence, model response, structured report, analyst review.

That review model is the heart of the training program.

It forces each lab to connect theory to evidence.

A claim without a test is only commentary.

A test without evidence is only a demonstration.

Evidence without analyst review is only stored data.

The training program has to connect all three.

## What the Labs Should Teach

The labs are organized around browser-AI failure classes, not payload strings.

The point is not to teach someone to memorize examples.

The point is to teach testers how to reason about classes of browser artifacts, how those artifacts enter AI-assisted workflows, and what evidence is required to prove the control handled them safely.

| Lab Area | Skill Taught | Evidence Required | Failure Mode Exposed |
|---|---|---|---|
| Raw DOM versus rendered page | Compare source state with browser-rendered state | Raw HTML, DOM snapshot, visible text, screenshot | Static parsing misses what the user or model-facing browser actually sees |
| Hidden text and metadata | Identify non-obvious content that may enter model context | DOM extract, computed style notes, metadata capture | Hidden or low-visibility content influences model output |
| Screenshot and visual deception | Validate whether visual evidence supports the security decision | Screenshot, visible text extract, model-bound context | Visual lure and extracted text disagree |
| iframe and frame-tree ambiguity | Preserve frame origin and nested content context | Frame tree, frame URLs, per-frame text, screenshot | Parent page appears benign while nested content carries risk |
| Delayed content and state changes | Detect content that changes after initial load | Before and after DOM, before and after screenshot, timing record | Early scan passes, later rendered state becomes unsafe |
| QR code and off-browser handoff | Capture browser-to-mobile or browser-to-external transition risk | Screenshot, decoded QR target, redirect notes, final destination | Security pipeline misses handoff outside ordinary link inspection |
| Model context boundary | Determine what browser content entered the model prompt or context | Extracted context artifact, prompt boundary record, redaction notes | Untrusted page content becomes indistinguishable from trusted instruction |
| Model output handling | Test whether model output is validated before downstream use | Raw model output, schema validation result, rejected fields | Free-form model response becomes executable or authoritative control input |
| Policy enforcement outside the model | Verify deterministic control ownership | Policy input, policy rule, model signal, enforcement decision | Model verdict becomes the policy authority |
| Evidence package and analyst review | Produce a defensible record of what happened | Artifact manifest, hashes, report, replay notes | Detection cannot be reconstructed, challenged, or retested |

A lab that does not produce evidence should be considered incomplete.

A lab that cannot be replayed should be considered weak.

A lab that relies on a model's explanation as the only proof should fail.

In the current workshop track, those areas map onto a concrete sequence:

| Workshop Area | Current Implementation Role |
|---|---|
| Lab 00 | Environment, target, browser, proxy, media tooling, manifest, and checksum readiness |
| Lab 01 | Baseline browser-AI evidence capture and local proxy evidence |
| Lab 02 | Indirect prompt injection through visible text, hidden DOM, and metadata fixtures |
| Lab 03 | Hidden DOM and low-visibility evidence, including source, DOM, visible text, computed style, screenshots, and proxy artifacts |
| Lab 04 | DOM versus rendered-page mismatch evidence |
| Lab 05 | Screenshot and visual deception evidence |
| Lab 06 | iframe and frame-tree source-confusion evidence |
| Lab 07 | Delayed content and state-transition evidence |
| Lab 08 | QR-style handoff and off-browser transition evidence |
| Lab 09 | Synthetic sensitive-data handling and marker tracking |
| Lab 10 | Model verdict manipulation and deterministic policy separation |
| Lab 11 | Fail-open pressure and exception-abuse workflow evidence, with future browser-backed maturity still called out |
| Lab 12 | Target-backed capstone attack-chain evidence package |

## How This Differs From Ordinary Web App Testing

This work does not replace the OWASP Web Security Testing Guide.

It builds on it.

OWASP describes WSTG as a cybersecurity testing resource for web application developers and security professionals, with structured identifiers for test scenarios. That structure remains valuable.

Traditional web application testing asks whether the application can be attacked.

Browser-AI testing asks an additional question:

What happens when adversarial browser content is observed, extracted, summarized, transformed, judged, logged, and acted upon by an AI-assisted security workflow?

That is not a replacement for web security.

It is an additional control-plane problem.

The tester still needs ordinary web testing discipline. Authentication, authorization, session handling, input validation, output encoding, access control, browser behavior, and business logic still matter.

But browser-AI systems add new questions:

What content entered the model context?

Was it labeled as untrusted?

Was it separated from trusted policy?

Was model output constrained?

Was the enforcement path deterministic?

Was the evidence sufficient for another analyst?

Did the control inspect what the browser rendered, or only what a parser extracted?

Did the test capture state changes after the first page load?

Did iframe context survive the evidence pipeline?

Did the system preserve enough detail to distinguish visual deception from model confusion?

These questions belong in the same professional testing culture as WSTG, but they require additional evidence.

## Relationship to Existing AI Security Guidance

This project does not need to invent the entire AI security field from scratch.

It should align with serious existing work and then specialize that work for browser-based AI systems.

OWASP's Top 10 for Large Language Model Applications identifies prompt injection and insecure output handling as major LLM application risks. OWASP describes prompt injection as manipulation of LLMs through crafted inputs, and insecure output handling as failure to validate LLM outputs before downstream use.

Those categories map directly into browser-AI testing.

A hostile web page is a crafted input.

A model verdict is output that may influence a downstream control.

A browser extension, remote browser isolation platform, secure web gateway, browser assistant, or AI-assisted SOC workflow may all sit between the page and the policy decision.

That is where the testing discipline has to focus.

NIST's AI Risk Management Framework is intended to improve the ability to incorporate trustworthiness considerations into the design, development, use, and evaluation of AI products, services, and systems. For this project, that translates into practical evaluation questions: what is measured, what is logged, what is controlled, and what can be reviewed.

MITRE ATLAS provides a living knowledge base of adversary tactics and techniques against AI-enabled systems, based on real-world observations and realistic demonstrations from AI red teams and security groups. For browser-AI systems, ATLAS-style adversary thinking should inform test design, but the lab artifacts must remain safe, local, synthetic, and authorized.

The objective is not to duplicate those frameworks.

The objective is to make them operational at the browser evidence layer.

## Evidence Capture Is Not Optional

The browser is not a simple text source.

A browser session can include raw markup, script-mutated DOM, visible text, hidden elements, canvas content, screenshots, nested frames, redirects, local file interactions, QR codes, and delayed state changes.

If a security control claims to reason about browser risk, it needs evidence from the browser.

Playwright is useful in this context because it can automate browser sessions and capture screenshots. Its documentation also describes trace viewing as a way to inspect recorded traces after a script has run, which is valuable when tests fail or need review. Playwright also documents direct screenshot capture and full-page screenshot capture.

The specific tooling may change over time.

The evidence requirement should not.

A serious browser-AI lab should preserve artifacts that let the tester answer:

What loaded?

What rendered?

What changed?

What was extracted?

What entered the model?

What did the model return?

What did policy decide?

What was enforced?

What can the analyst reconstruct?

Without those answers, the test is not mature enough.

## Safety Boundary

This lab program must remain safe by design.

The goal is to validate controls, not to arm attackers.

Every lab should use local targets, synthetic probes, inert files, seeded test data, localhost, or lab-owned domains.

The program should not include third-party targeting, credential harvesting, malware, destructive testing, real phishing operations, browser command and control, token theft, MFA bypass tooling, or instructions that enable abuse against real systems.

The public test suite already states a compatible safety boundary: it is for authorized testing, local validation, defensive research, and professional due diligence. It warns against unauthorized scanning, credential theft, cookie theft, token extraction, browser command and control, MFA bypass tooling, destructive tests, exploit automation, and third-party testing without written authorization.

That boundary should remain explicit in every lab.

A training program for elite practitioners does not need to be reckless to be serious.

It needs to be precise.

## Evaluation Standard

A lab does not pass because the model gave a sensible answer.

A lab passes only when the full pipeline is reviewable.

A passing test should show:

* what the browser loaded
* what the user could see
* what the DOM contained
* what changed after rendering
* what entered the AI context
* what the model returned
* what policy decided
* what enforcement occurred
* what evidence was saved
* what the analyst could reconstruct
* what would happen on retest

That is the standard.

If a model says "this page is suspicious," that is not enough.

If a control blocks a page but cannot show why, that is not enough.

If a report contains a verdict but no artifact manifest, that is not enough.

If the tester cannot replay the case after a model, browser, or policy update, that is not enough.

Browser-AI security claims need evidence that can survive a skeptical review.

## Capstone Outcome

The capstone requires a practitioner to run an end-to-end browser-AI validation exercise against the local lab target and produce a report that a red-team lead, SOC lead, product security engineer, vendor-risk reviewer, or security architect could use.

In the current suite, that capstone is represented by a deterministic capstone evidence package generator and a target-backed wrapper that verifies the local weak target, records target-contract readiness, captures browser evidence, preserves synthetic marker provenance, writes an artifact manifest, writes `SHA256SUMS.txt`, and creates a reviewer archive. It remains local-only and synthetic-only; it does not prove production security for any real product.

The report should include:

* scope
* rules of engagement
* lab target version
* test suite version
* browser version
* model version
* test cases executed
* artifacts collected
* failures
* false positives
* false negatives
* evidence gaps
* policy gaps
* analyst usability notes
* engineering recommendations
* retest requirements

The report should not read like a prompt-injection blog post.

It should read like control validation.

It should be possible for another tester to reproduce the environment, rerun the cases, inspect the artifacts, compare expected and actual outcomes, and challenge the conclusions.

That is what separates a useful professional lab from a clever demo.

## What This Program Should Produce

The practical track is designed to produce three kinds of outcomes.

First, it should teach practitioners how browser-based AI systems fail.

Not in theory.

In observable, artifact-backed test cases.

Second, it should teach practitioners how to validate defensive claims.

A vendor claim that says "we use AI to detect malicious pages" is not enough.

The test must ask:

What does the system observe?

What does it ignore?

What enters the model context?

What controls model output?

What owns the final decision?

What evidence is preserved?

What can the analyst review?

Third, it should teach practitioners how to communicate results.

A useful finding should be written in terms of pipeline failure, evidence gap, policy weakness, analyst impact, and retest condition.

That is more valuable than a payload string.

## The Standard for This Work

This work will be judged by people who have seen weak security content before.

They will not be impressed by AI novelty.

They will not be impressed by a screenshot of a model making a mistake.

They will not be impressed by a list of prompts.

They will ask whether the method is safe, whether the target is controlled, whether the evidence is real, whether the conclusions are reproducible, and whether the work helps defenders make better decisions.

That is the right standard.

This project should welcome it.

## References

* [Browser-Safe AI Systems series index](https://unattributed.blog/ai-security/browser-security/security-operations/red-team/2026/05/09/browser-safe-ai-systems-00-series-index.html)
* [AI Browser Security Test Suite](https://github.com/unattributed/ai-browser-security-test-suite)
* [Controlled local Ollama Web UI target](https://github.com/unattributed/ollama-webui)
* [OWASP Top 10 for Large Language Model Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
* [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
* [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
* [MITRE ATLAS](https://atlas.mitre.org/)
* [Playwright trace viewer documentation](https://playwright.dev/docs/trace-viewer)
* [Playwright screenshot documentation](https://playwright.dev/docs/screenshots)

## Closing Thesis

The project is moving from argument to validation.

The point is not to prove that AI can be fooled.

That has already been established by the field, and it is not the interesting part.

The point is to teach security professionals how to determine whether a browser-based AI control can observe the right evidence, constrain the model, enforce deterministic policy, and produce reviewable security outcomes.

That is the practical discipline.

Test the pipeline.

Capture the browser evidence.

Constrain the model.

Keep policy outside the model.

Make every important decision replayable.