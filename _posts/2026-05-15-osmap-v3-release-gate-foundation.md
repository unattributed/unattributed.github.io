---
layout: post
title: "OSMAP V3 Release-Gate Foundation: Building Evidence Before Trust"
date: 2026-05-15
author: unattributed
categories: [security-engineering, openbsd, release-engineering]
tags: [osmap, release-gates, wstg, evidence, openbsd, supply-chain]
---

OSMAP V3 was not only a feature release.

It was a release-gate exercise.

The work was about forcing the project to prove that security controls were present, live, repeatable, and backed by evidence before treating the implementation as releasable.

That sounds straightforward until the evidence has to be collected from a real host, through real authentication, with real service boundaries, while still avoiding secret leakage into the repository.

The result was a V3 gate that now requires authenticated WSTG evidence, human password-plus-TOTP proof, supply-chain checks, live host readiness, TLS validation, helper-boundary validation, resource-control evidence, MIME and HTML rendering evidence, and a sanitized release archive.

## The Release Gate Had To Fail Closed

The most important question was simple:

**Does release mode fail when authenticated WSTG evidence is missing?**

It was not enough for WSTG checks to exist.

Release mode had to reject:

* skipped authenticated tests
* missing authenticated coverage
* selected-test release runs
* missing human credential proof
* missing TOTP proof
* unauthenticated summaries
* warning or skip states in release-blocking tests

The gate now requires a full WSTG release run and validates that the command path included the human prompt-auth flow.

The successful authenticated WSTG run produced:

* `26` passing WSTG checks
* `0` failures
* `0` warnings
* `0` skips
* authenticated login proof
* TOTP proof
* protected route access proof
* session issuance proof
* logout proof
* session invalidation proof

That matters because unauthenticated security evidence is often a false comfort.

A login form can be secure while the authenticated application behind it is weak.

## Human Proof Was Deliberately Awkward

Human credential and TOTP proof was intentionally not reduced to a permanent automation secret.

The operator had to run release WSTG with prompt-based authentication.

That created friction, but it also avoided baking a reusable password or TOTP seed into the release tooling.

The release gate then checked for evidence that the human path really happened.

This is a useful pattern:

* keep the secret out of automation
* capture the fact that human proof occurred
* redact the raw interaction
* commit only sanitized summaries
* make missing proof release-blocking

The raw proof directories were left untracked and ignored.

The committed artifact is the sanitized release summary, not the terminal session containing prompts.

## OpenBSD Versus Linux Was Not A Footnote

Development happened from a Parrot OS workstation.

The target host was OpenBSD.

That split matters.

Shell utilities, OpenSSL behavior, service management, privilege boundaries, filesystem ownership, and socket behavior are not identical across the two environments.

One concrete example was helper-boundary proof.

A live validator generated an HMAC signature for a mailbox-helper request. The first implementation used an OpenSSL command form that worked poorly across the target environment:

```sh
openssl enc -A -hex
```

On the OpenBSD host, that produced OpenSSL usage output instead of the lower-case hexadecimal digest the helper expected.

The fix was to avoid that OpenSSL-specific conversion and use a simpler portable binary-to-hex path:

```sh
od -An -tx1 | tr -d ' \n'
```

The lesson is not that OpenSSL is bad.

The lesson is that live release evidence should run where the release will operate.

If the production host is OpenBSD, the proof must survive OpenBSD.

## The Helper Boundary Became A Real Boundary

V3 hardened the mailbox-helper boundary.

Helper-backed mailbox operations now require a permission-restricted request grant key.

That exposed older live validators that started isolated helper-backed runtimes without providing grant keys.

The failure was good.

It meant the new boundary was actually enforced.

But it also meant the V2 carry-forward readiness evidence had to be updated so every live validator that starts an isolated helper either:

* creates paired web and helper grant keys, or
* provides a web-side grant key for negative backend-unavailable tests

This affected several validators:

* login-send
* inline image metadata
* all-mailbox search
* archive shortcut
* session surface
* send throttle
* move throttle
* request guardrails
* mailbox backend unavailable
* helper peer authentication

That was an important compatibility lesson.

Security hardening often breaks evidence tooling first.

The correct answer is not to weaken the control.

The correct answer is to upgrade the proof harness.

## Supply-Chain Gates Needed Host-Local Tooling

The release gate required pinned supply-chain tooling.

The local workstation had the tools.

The OpenBSD host-side validation environment did not initially see them because the host validation wrapper intentionally used its own cargo home:

```text
/home/foo/tmp-osmap-host-validation/cargo-home
```

That isolated cargo home needed the pinned versions of:

* `cargo-deny 0.18.3`
* `cargo-audit 0.22.1`

This was another useful failure.

The validation wrapper was doing the right thing by isolating build state.

The missing part was remembering that isolated state also isolates installed cargo binaries.

## Throttling Had To Be Observable

WSTG authentication throttling initially produced a warning.

The bounded probe did not observe throttling within the attempt budget.

That turned into two changes:

* use a local-domain throttle probe identity
* count backend-unavailable login attempts into throttle buckets

The important release property was not simply that throttling existed somewhere in code.

The release property was that the bounded WSTG probe could observe it without unsafe extra attempts.

That is the difference between a control and release evidence for a control.

## Resource And Timeout Hardening Had To Be Live

V3 added release evidence for bounded resources and timeouts.

The gate required live proof for:

* mailbox worker budgets
* search worker budgets
* route-level expensive request timeouts
* helper-backed operation boundaries
* budget acquisition and release logging
* failure behavior under constrained budgets

The point was not just denial-of-service resistance.

The point was also operational explainability.

When the application refuses work because a budget is exhausted, the event should be bounded, observable, and safe to investigate.

## MIME And HTML Correctness Had To Be Proven With Mail

MIME and HTML handling is easy to get wrong.

V3 evidence included live validation for rendering and attachment behavior, including:

* conservative HTML sanitization
* remote content suppression
* forced-download attachment behavior
* inline image metadata surfacing
* bounded MIME parsing
* selected source-attachment handling
* redaction of sensitive evidence

The release gate required live MIME and HTML proof because fixture-only parsing tests are not enough.

The browser route, mailbox helper, session handling, message fetching, and attachment path all have to agree.

## The Release Evidence Was Sanitized

The final committed release evidence included sanitized artifacts under `maint/live`.

The raw human WSTG proof captures were not committed.

That distinction matters.

Raw proof can include terminal prompts, session output, timing, local paths, or other context that should not become permanent repository history.

The release archive and summaries are meant to answer:

* what was checked
* when it was checked
* what host was assessed
* what command generated the evidence
* which checks passed
* which evidence files were included
* whether any release errors remained

They are not meant to preserve secrets.

## What Passed

The final V3 release gate passed:

* cargo build with locked dependencies
* cargo tests
* clippy
* formatting
* supply-chain checks
* dependency inventory
* documentation governance checks
* TLS policy checks
* authenticated WSTG release coverage
* TLS standard validation
* resource and timeout evidence
* helper-boundary evidence
* MIME and HTML proof evidence
* sanitized release evidence archive generation

The authenticated WSTG summary ended with:

```text
pass: 26
fail: 0
warning: 0
skip: 0
release_errors: []
```

The host checkout was synced to the pushed main branch, and the OpenBSD services were verified healthy.

## Lessons

The main lesson from V3 is that release gates should test the release process, not only the application.

A good gate should catch:

* missing evidence
* stale evidence
* partial test runs
* unauthenticated proof
* host-local tool drift
* cross-platform shell assumptions
* helper-boundary regressions
* warnings that would otherwise be rationalized away

It should also force a team to decide what evidence is safe to commit.

That last point is easy to overlook.

Security evidence can become a security problem if it captures too much.

The pattern that worked for V3 was:

* collect raw proof locally
* redact and summarize
* commit sanitized release evidence
* ignore raw human proof directories
* make missing proof release-blocking
* rerun on the real host

That is slower than a green checkmark.

It is also much more useful.

## Closing Thought

V3 was less about adding one control and more about making controls accountable.

The useful question changed from:

**Did we write the feature?**

to:

**Can the release gate prove the feature is present, live, bounded, authenticated, and safe to inspect?**

That is the shape of release engineering I want for security-sensitive software.
