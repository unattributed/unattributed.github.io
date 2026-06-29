---
layout: post
title: "Controlled Agentic Offensive Security for AWS-Hosted Systems: Series Overview"
date: 2026-06-29
author: unattributed
categories: [ai-security, offensive-security, cloud-security, security-architecture, secure-sdlc]
tags: [agentic-security, agentic-orchestration, offensive-security, adversarial-testing, cloud-security, aws-security, aws-threat-hunting, application-security, secure-sdlc, evidence-driven-engineering, red-team, threat-hunting, attack-path-intelligence, human-review, ai-agents]
description: "A technical series overview for building a controlled agentic offensive security platform for AWS-hosted systems, combining campaign orchestration, cloud security due diligence, application security testing, human review, evidence capture, and secure SDLC integration."
excerpt: "Static prompts cannot run offensive security campaigns. This series defines the architecture, evidence model, orchestration layer, and governance controls required to build a controlled agentic offensive security platform for AWS-hosted systems and cloud-native applications."
series: "Controlled Agentic Offensive Security"
series_part: 0
series_total: 19
series_role: overview
robots: index,follow
draft: false
---

# Controlled Agentic Offensive Security for AWS-Hosted Systems

> Series: Controlled Agentic Offensive Security, Overview and reader guide.

This document introduces a forthcoming technical series on building a controlled agentic offensive security platform for AWS-hosted systems and cloud-native applications.

The intended audience is collaborating developers, forward agentic engineers, infrastructure engineers, SRE professionals, application security engineers, cloud security engineers, offensive security practitioners, security architects, and technical stakeholders who need to understand the thesis, design, operating model, and evidence doctrine before contributing to the platform or reviewing its claims.

This is not a series about using a chatbot for security testing.

It is a series about designing a governed campaign execution system that can perform repeatable offensive security due diligence over application code, cloud infrastructure configuration, identity and access control, API surfaces, CI/CD trust boundaries, hosted runtime configuration, telemetry coverage, remediation quality, and fix validation.

Series navigation: forthcoming.

* * *

## Abstract

Static prompts cannot run offensive security campaigns.

A real campaign is a long-running, stateful, evidence-producing workflow. It must design a scenario, define scope, gather context, assign agents, execute bounded testing, review outputs, research missing information, revise hypotheses, re-execute safely, confirm or reject findings, support remediation, verify fixes, and preserve enough evidence for independent review.

Skill files are useful. They define how a specific task should be performed. A skill file can describe how to inspect an IAM trust relationship, review a GraphQL resolver, validate CloudTrail coverage, assess a CI/CD deployment path, test an authorization boundary, normalize a proof of concept, or convert a confirmed vulnerability into reproducible engineering steps.

But skill files are not the platform.

The hard technical problem is the agentic orchestrator. The orchestrator schedules and watches work, gathers context, selects skills, assigns roles, authorizes tools, validates inputs and outputs, requests collaborative review, preserves evidence, gates unsafe actions, maintains campaign state, and decides whether the next action is research, execution, review, revision, replay, remediation, fix validation, or stop.

This series breaks that thesis into a buildable design.

## Central thesis

The future of AI-enabled offensive security is not better prompting.

The future is controlled campaign orchestration.

A controlled agentic offensive security platform must combine:

* offensive security methodology
* cloud-native infrastructure understanding
* application security testing
* repository-aware secure SDLC integration
* agentic orchestration
* skill-based task execution
* context engineering
* human review
* evidence capture
* auditability
* safety gates
* attack-path replay
* remediation support
* fix validation

The platform is successful only when its work is transparent enough that a competent third party, who was not present during the campaign, can review the scope, assumptions, context, actions, tool outputs, findings, rejected false positives, approvals, remediation guidance, replay records, and closeout package to determine whether proper due diligence was performed.

The output of an agentic offensive security campaign is not a chat transcript.

The output is a defensible evidence package.

## Why this series exists

Modern security teams are being asked to do more than run periodic tests. They need continuous visibility over fast-changing systems, codebases, cloud environments, deployment pipelines, APIs, identity paths, data flows, and detection coverage.

At the same time, AI agents are becoming capable enough to perform meaningful units of security work: read code, reason about architecture, execute tools, summarize logs, generate tests, write findings, and propose remediation.

That capability creates a serious architectural problem.

If agents are left as static prompts, they cannot run campaigns. If they are allowed to run freely, they can drift from scope, misuse stale context, accept weak evidence, generate false confidence, or perform unsafe actions. If they are governed only by human memory and chat history, the work is not reliably reviewable.

The missing system is a controlled agentic offensive security platform.

Such a platform must be able to answer basic due diligence questions:

* What was authorized?
* What was in scope?
* What was out of scope?
* What context was used?
* Was the context current?
* Which agent acted?
* Which skill was selected?
* Which tools were allowed?
* Which commands or API calls were executed?
* What evidence was created?
* What was reviewed by another agent?
* What required human approval?
* What was confirmed?
* What was rejected as noise?
* What remediation was recommended?
* What fix was validated?
* What remains unresolved?

A platform that cannot answer those questions is not ready to perform serious offensive security work.

## Professional doctrine

The operating doctrine for this series is transparent execution, accountable decision-making, and evidence sufficient for independent review.

Every meaningful claim should be traceable to scope, context, tool output, evidence, peer review, human approval where required, and a closeout record.

This doctrine comes from practical offensive security work: evidence matters. A finding that cannot be reproduced, reviewed, and explained is not useful to an engineering team. A campaign that cannot show what it did and did not test is not useful to leadership. A remediation claim that has not been replayed or otherwise validated is not a closure record.

In this series, agentic security work must satisfy the same professional bar:

* every agentic action should be attributable
* every input should be traceable
* every output should be reviewable
* every finding should be reproducible or explicitly rejected
* every safety boundary should be recorded
* every approval should be attached to the campaign record
* every remediation claim should include fix validation
* every campaign should close with an evidence package

The platform should not say, "the agent found a vulnerability."

It should say:

* what hypothesis was tested
* what context was used
* what scope authorized the action
* what tool or skill produced the observation
* what evidence supports the observation
* what peer or human review confirmed it
* what impact was validated
* what remediation was proposed
* what fix was verified
* what replay or regression path now exists

That is the evidence standard.

## Platform scope

The platform described in this series is designed for AWS-hosted systems and solutions. That scope matters because the security surface is not only application code.

A serious offensive due diligence platform must reason across:

| Surface | Due diligence questions |
| --- | --- |
| Application code | Is the application written securely, with defensible authorization, input handling, session management, and data access boundaries? |
| APIs and GraphQL | Are routes, resolvers, object-level authorization checks, schema exposure, and mutation paths properly constrained? |
| Identity and access control | Can IAM users, roles, service principals, assumed-role paths, or workload identities reach sensitive systems unexpectedly? |
| Cloud infrastructure configuration | Are accounts, regions, VPCs, subnets, security groups, load balancers, storage services, KMS keys, and managed services configured securely? |
| Network exposure | Are ingress, egress, peering, private endpoints, service endpoints, and public surfaces understood and intentionally exposed? |
| CI/CD and deployment paths | Can build systems, deployment roles, artifacts, secrets, or pipeline permissions become an attack path? |
| Data protection | Are data stores, object buckets, encryption keys, retention policies, and sensitive-data boundaries mapped and tested? |
| Hosted runtime configuration | Are containers, serverless functions, managed runtimes, environment variables, metadata access, and runtime policies secure? |
| Telemetry and detection coverage | Would meaningful attacker activity be logged, detected, correlated, and reviewed? |
| Remediation and fix validation | Can the platform prove that a fix addresses root cause and does not merely suppress a symptom? |

A useful offensive security platform must test both whether applications are written securely and whether they are hosted securely.

Those are different questions. Both must be answered.

## Platform design layers

The design is organized into eight layers.

| Layer | Purpose |
| --- | --- |
| Human Review Portal | Provides intake, triage, findings review, evidence viewing, approval gates, attack-path replay, risk scoring, engineer-ready reporting, remediation collaboration, fix validation, and analyst feedback. |
| AI Orchestration Layer | Schedules and watches workflows, assigns agents, binds context, selects skills, authorizes tools, validates outputs, routes review, and controls stop or re-execution decisions. |
| Encrypted Knowledge Layer | Stores vector context, findings, attack graphs, evidence, architecture models, scenario libraries, metadata, provenance, session links, retrieval policies, versioning, lineage, and deduplication state. |
| Security, Privacy, and Governance Controls | Enforces identity, access, encryption, network isolation, data protection, policy approvals, model governance, audit, recovery, resilience, and supply-chain assurance. |
| AWS Infrastructure Execution Layer | Provides the cloud-native substrate for workflow execution, model calls, isolated task runners, evidence storage, state management, audit logging, and integrations. |
| Safe Execution Environments | Provides isolated test accounts, isolated VPCs, ephemeral environments, sandbox browser and web test labs, isolated code analysis environments, synthetic data, mock services, and replay validation environments. |
| Guardrails and Policies | Defines scope boundaries, approved tools, no direct production exploitation without explicit approval, replay and persistence gates, sensitive data redaction, retention and deletion rules, session isolation, and context separation. |
| Monitoring and Audit | Captures workflow logs, per-agent traces, model and token use, tool-call audit trails, evidence timestamps and checksums, approval logs, stale-context checks, campaign KPIs, and risk metrics. |

The design should be read as a system, not a list of components. The orchestrator needs context from the knowledge layer. The knowledge layer needs provenance and encryption. Tool execution needs safe environments. Unsafe transitions need the human portal. Every action needs auditability. Findings need remediation and validation paths. The SDLC needs issues, branches, pull requests, tests, and evidence bundles.

## AWS execution substrate

The AWS execution layer is not the thesis, but it is the practical substrate for the system.

A mature platform can use AWS-native services such as:

| AWS component | Platform purpose |
| --- | --- |
| Step Functions | Campaign workflow orchestration and state transition tracking. |
| EventBridge | Event routing, scheduled checks, and workflow triggers. |
| SQS or SNS | Queueing, decoupling, notifications, and asynchronous agent work routing. |
| Amazon Bedrock | Managed access to foundation models where appropriate. |
| ECS on Fargate | Isolated agent task execution, scanning containers, browser runners, and tool workers. |
| Lambda | Lightweight event handlers, validation functions, and glue logic. |
| CodeBuild | Isolated code analysis, build validation, and repository security checks. |
| S3 | Evidence storage, artifact storage, export bundles, and immutable campaign records where configured. |
| DynamoDB | Campaign state, loop state, idempotency records, task state, and approval metadata. |
| OpenSearch | Search across evidence, findings, logs, metadata, and knowledge artifacts. |
| KMS | Encryption keys, envelope encryption, and evidence protection. |
| Secrets Manager | Controlled storage of credentials required for approved testing workflows. |
| VPC and PrivateLink | Network isolation, private service access, and reduced public exposure. |
| VPC endpoints | Private access to AWS APIs and internal platform services. |
| Security groups and NACLs | Network containment for runners and service boundaries. |
| CloudWatch | Metrics, logs, alarms, workflow telemetry, and operational visibility. |
| CloudTrail | Control-plane audit evidence for AWS API activity. |
| AWS Config | Configuration history, compliance evaluation, and infrastructure evidence. |
| GuardDuty | Threat detection signals that can support or challenge campaign assumptions. |
| Security Hub | Aggregation of security findings and posture signals. |

The architecture must be careful with authority. A task runner that can analyze code should not automatically be allowed to perform cloud actions. A recon agent should not automatically be allowed to run exploitation tools. A model should not decide its own permissions. The orchestrator must bind each role to scoped permissions, approved tools, allowed data, and explicit stop conditions.

## Core campaign loop

Every article in the series returns to the same loop:

```text
design scenario
→ define scope and safety boundary
→ gather context
→ assign agents and skills
→ execute bounded testing
→ capture evidence
→ review and score outputs
→ research missing context
→ revise workflow or hypothesis
→ safely re-execute
→ confirm finding or reject as noise
→ produce engineer-ready report
→ support remediation
→ validate fix
→ replay as regression
→ close campaign with evidence
```

The loop is intentionally explicit because offensive security work must be stoppable. When authority is missing, the loop stops. When context is stale, the loop stops. When evidence is insufficient, the loop stops. When exploitation would cross a safety boundary, the loop stops. When a finding requires human risk acceptance, the loop stops.

A safe campaign engine does not keep trying forever.

A safe campaign engine stops early and records why.

## Blind third-party reviewability

The platform is designed around blind third-party reviewability.

A blind third party is a competent reviewer who was not present during the work but can inspect the campaign record and decide whether proper due diligence was performed.

A defensible campaign evidence package should include:

```text
campaign evidence package
├── scope and rules of engagement
├── approved safety boundaries
├── asset and context inventory
├── context freshness and provenance records
├── campaign hypothesis
├── agent role assignments
├── skill and tool execution records
├── model and tool-call logs
├── timestamps and actor attribution
├── raw outputs and normalized findings
├── rejected false positives
├── peer review notes
├── human approval records
├── reproduction steps
├── proof-of-impact artifacts
├── remediation guidance
├── fix verification evidence
├── replay or regression workflow
├── closeout statement
└── checksum manifest
```

This is the standard the platform should be judged against.

If the evidence package is weak, the campaign claim is weak.

## The role of GitHub, repository controls, and SDLC integration

GitHub is not the offensive testing platform. It is part of the collaboration and change-control plane.

Repository-owned controls define how agents are allowed to participate in engineering work. That includes:

* `AGENTS.md`
* project charter
* secure SDLC guidance
* agent role matrix
* agent loop control model
* sprint branching and merge policy
* human approval gates
* evidence requirements
* discussion protocol
* Wiki operating model
* risk register
* issue templates
* pull request templates
* CI and validation gates

GitHub Discussions can coordinate live work. GitHub Wiki can preserve durable operating memory. Issues can bind tasks. Branches can isolate change. Pull requests can enforce review. CI can validate behavior. Evidence can prove or reject claims.

The rule is simple:

Prompts are not governance.

Repository controls are governance.

## Reader path through the series

The series is designed to be read in four movements.

First, it establishes the thesis: campaigns require orchestration, state, evidence, and human review.

Second, it defines the platform architecture: orchestrator, human portal, knowledge layer, AWS execution layer, safe environments, and governance controls.

Third, it applies the model to offensive due diligence: cloud infrastructure configuration, hosted application security, attack-path intelligence, telemetry, finding quality, remediation, and fix validation.

Fourth, it closes with implementation discipline: repository-owned controls, SDLC integration, metrics, OSMAP as a reference implementation, and the complete platform blueprint.

## Forthcoming series

### Part 01, Static Prompts Cannot Run Campaigns

This article establishes the core thesis. It explains why offensive security campaigns cannot be completed through static prompts, why skill files are necessary but insufficient, and why the central product is the agentic orchestrator.

It introduces campaign state, scope, context, safety, review, evidence, remediation, replay, and closeout as first-class platform concepts.

### Part 02, The Offensive Campaign State Machine

This article defines the campaign as a finite state machine. It shows how the platform moves from a campaign objective to scoped testing, context acquisition, agent assignment, execution, evidence capture, review, revision, re-execution, validation, remediation, replay, and closeout.

It defines where the platform must stop rather than continue.

### Part 03, The AI Orchestration Layer

This article explains the orchestrator as the core technical product. It defines how work is scheduled, watched, assigned, context-bound, tool-authorized, reviewed, and stopped.

It makes the argument that the model is replaceable, but campaign state, evidence, policy, and orchestration are durable.

### Part 04, Skill Files Are Necessary but Insufficient

This article explains skill files as bounded task procedures. It shows how they help agents perform repeatable work but cannot decide authority, context sufficiency, safety, campaign state, or evidence quality by themselves.

It includes offensive skill examples for repository review, GraphQL assessment, IAM trust review, CloudTrail coverage validation, finding confirmation, proof-of-concept normalization, and fix verification.

### Part 05, Context Engineering for Clearbox Testing

This article explains why knowledge acquisition and assumption removal must come before agentic execution.

Clearbox testing requires current, scoped, provenance-tracked context from repositories, architecture, service ownership, IAM trust relationships, data flows, network paths, runtime configuration, logs, prior findings, and approved scope.

### Part 06, The Human Review Portal as a Security Control

This article defines the human review portal as a safety, quality, and authority boundary.

The portal supports intake, triage, findings review, evidence inspection, attack-path replay approval, risk scoring, remediation collaboration, fix validation, and analyst feedback.

### Part 07, The Encrypted Knowledge Layer

This article designs the knowledge and memory layer that allows campaigns to persist, retrieve, link, deduplicate, and audit information safely.

It covers vector context, finding databases, attack graphs, evidence stores, architecture models, scenario libraries, metadata indexing, provenance, session linking, versioning, lineage, retrieval policy, retention, redaction, and encryption.

### Part 08, Attack-Path Intelligence

This article explains how the platform turns context, recon, code review, cloud posture, and findings into attack-path intelligence.

It models paths such as exposed route to authorization flaw to sensitive data, CI/CD trust boundary to secret exposure, IAM trust path to data access, and GraphQL resolver flaw to object-level authorization failure.

### Part 09, Governed Exploitation and Safety Boundaries

This article explains how a platform can validate impact without becoming unsafe.

It defines governed exploitation as bounded, approved, isolated, instrumented, redacted, and reviewable.

### Part 10, AWS Execution Architecture

This article defines the AWS-native execution layer for controlled agentic adversarial testing.

It covers workflow orchestration, event routing, agent runtimes, isolated runners, storage, search, encryption, secrets, networking, audit, integrations, and safe execution environments.

### Part 11, Testing Cloud Infrastructure Configuration

This article applies the platform to cloud control-plane due diligence.

It focuses on IAM, STS, KMS, S3, VPCs, CloudTrail, Config, GuardDuty, Security Hub, CloudWatch, ECR, ECS, Lambda, CI/CD roles, network exposure, logging coverage, and configuration evidence.

### Part 12, Testing Hosted Application Security

This article applies the platform to application security for AWS-hosted applications.

It covers secure code review, API testing, GraphQL testing, authentication, session management, authorization, input handling, secrets exposure, deployment paths, runtime hardening, and fix verification.

### Part 13, Telemetry, Evidence, and Audit Trails

This article defines the audit model for AI-driven offensive security work.

It tracks campaign execution, agent decisions, tool calls, evidence creation, approvals, rejections, replay attempts, fix verification, model usage, and stale-context checks.

### Part 14, From Noisy Agent Output to Engineering-Ready Findings

This article explains how agent output becomes a validated finding or gets rejected as noise.

It covers deduplication, exploitability, reproducibility, blast radius, business impact, root cause, remediation mapping, and fix validation.

### Part 15, Repository-Owned Controls for Agentic Security Workflows

This article explains how repository-owned control documents keep agentic offensive workflows inside an auditable secure SDLC.

It covers agent instructions, role matrices, loop control, discussion protocols, Wiki operating models, human approval gates, evidence requirements, risk registers, issue templates, pull request templates, and CI gates.

### Part 16, Making Agentic Adversarial Testing a Routine Part of the Secure SDLC

This article explains how the platform integrates into engineering instead of producing isolated security reports.

It shows how campaigns produce issues, branches, pull requests, tests, documentation updates, remediation collaboration, validation replay, and release confidence.

### Part 17, Metrics for Agentic Offensive Security

This article defines how to measure signal, safety, coverage, remediation, and learning.

It covers confirmed finding rate, false positive rate, time to confirmation, replayability, evidence completeness, coverage by asset class, coverage by trust boundary, agent rejection rate, human intervention rate, stale context rate, and remediation verification rate.

### Part 18, OSMAP as a Reference Implementation for Controlled Agentic Acceleration

This article uses OSMAP as a concrete reference for disciplined agentic development, evidence-first engineering, repository-owned controls, validation gates, documentation alignment, and claim boundaries.

It does not claim OSMAP is the offensive testing platform. It shows how the development discipline transfers into controlled offensive security platform engineering.

### Part 19, The Full Platform Blueprint

This capstone article synthesizes the entire series into a buildable platform blueprint.

It presents the full path from campaign objective to attack-path replay, confirmed finding, remediation, fix validation, regression replay, maturity model, MVP architecture, control plane, evidence plane, human review plane, AWS execution layer, knowledge layer, and SDLC integration.

## Collaboration model

This series is also intended to support collaboration.

Different contributors will naturally enter the design from different perspectives:

| Collaborator | Useful entry points |
| --- | --- |
| Forward agentic engineers | Orchestrator design, skill registry, context packages, output schemas, scheduling, watcher loops, failure handling, and model/tool routing. |
| Collaborating developers | Repository controls, issue templates, PR gates, secure SDLC integration, remediation workflows, fix validation, and regression tests. |
| Infrastructure engineers | AWS execution architecture, network isolation, service boundaries, IAM, KMS, Secrets Manager, VPC endpoints, logging, and deployment models. |
| SRE professionals | Reliability, idempotency, observability, failure handling, replay safety, runbooks, rollback, queue depth, retry budgets, and platform health. |
| Application security engineers | Code review workflows, API and GraphQL testing, auth/session boundaries, vulnerability validation, finding quality, and remediation support. |
| Cloud security engineers | IAM graph analysis, control-plane testing, configuration evidence, logging coverage, detection validation, and policy review. |
| Offensive security practitioners | Campaign design, attack-path modeling, safe probing, validation, proof of impact, post-exploitation limits, and replay. |
| Security leadership | Risk scoring, metrics, evidence sufficiency, approval gates, governance, maturity, and prioritization. |

The series is written so that each group can challenge the design. That is intentional. A platform that cannot withstand peer review from these groups is not ready to perform meaningful offensive security work.

## What this series does not claim

This series does not claim that AI agents should be allowed to run unbounded offensive operations.

It does not claim that a model can replace human judgment.

It does not claim that synthetic validation is equivalent to production testing.

It does not claim that scanner output is a finding.

It does not provide authorization to test third-party systems.

It does not provide exploit instructions against real targets.

It does not claim that a platform is mature because it can generate plausible reports.

The platform described here is useful only when it remains scoped, governed, observable, reviewable, and evidence-driven.

## What success looks like

The platform is successful when it can:

* design realistic, scoped offensive scenarios
* gather and bind current context
* assign bounded agent work
* execute approved tools in safe environments
* stop when authority, context, evidence, or safety is missing
* separate high-impact findings from noise
* preserve evidence sufficient for independent review
* produce engineering-ready findings
* support remediation
* validate fixes
* replay attack paths as regression tests
* integrate with secure SDLC workflows
* report meaningful metrics on signal, safety, coverage, and learning

Success is not more agent output.

Success is better security evidence.

## Closing thesis

Static prompts cannot run campaigns.

Skill files are necessary but insufficient.

The model is not the platform.

The orchestrator, control plane, knowledge layer, human review portal, AWS execution substrate, safe execution environments, evidence model, and SDLC integration are the platform.

The future of AI-enabled offensive security is controlled campaign orchestration: agents, skills, cloud context, application context, evidence, human review, safety gates, replay workflows, and engineering integration working together to produce findings that are defensible, reproducible, and useful.

Then, and only then, should the system accelerate.

## References

* AWS Documentation, "What is AWS Step Functions?"
* AWS Documentation, "What is Amazon EventBridge?"
* AWS Documentation, "What is Amazon Bedrock?"
* AWS Documentation, "What is AWS CloudTrail?"
* AWS Documentation, "What is AWS Config?"
* AWS Documentation, "What is Amazon GuardDuty?"
* AWS Documentation, "What is AWS Security Hub?"
* GitHub Docs, "About pull requests"
* GitHub Docs, "About wikis"
* GitHub Docs, "Using the GraphQL API for Discussions"
