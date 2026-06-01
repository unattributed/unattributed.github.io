---
layout: post
title: "OSMAP V3 Closeout: Evidence, Boundaries, and the Cost of Being Honest"
date: 2026-06-01
author: unattributed
categories: [security-engineering, openbsd, release-engineering, email-security]
tags: [osmap, openbsd, webmail, release-gates, wstg, evidence, secure-development]
---

OSMAP V3 is closed.

That sentence is intentionally narrow.

It does not mean OSMAP is finished forever. It does not mean browser-facing mail is now an easy problem. It does not mean every useful webmail feature has been added, or that every future attack surface has been exhausted.

It means something more defensible:

**the Version 3 boundary was implemented, tested, validated on the intended host, tagged, and archived with evidence strong enough that I am willing to call this release closed.**

The final release tag is:

```text
v3.0.0
```

The assessed commit is:

```text
2aefef21ea061440db284b22b3f7c1698e4afda8
```

The release candidate tag remains:

```text
v3.0.0-rc1
```

The important part is not the tag.

The important part is what had to be true before the tag was allowed to mean anything.

* * *

## What V3 Closeout Means

Version 3 was the daily-driver hardening release.

V1 proved a narrow browser-mail boundary could be made defensible. V2 moved that boundary through pilot use and operational readiness. V3 had to do something harder: preserve that security posture while adding enough workflow continuity that OSMAP could be used more naturally without drifting into broad webmail-suite sprawl.

That meant V3 was not allowed to become a bucket of convenience features.

The closeout boundary included:

- release-mode validation that fails closed
- authenticated WSTG evidence with real password-plus-TOTP proof
- supply-chain enforcement
- resource and timeout hardening
- MIME and HTML rendering proof
- session lifecycle evidence
- draft save, resume, delete, and send-cleanup evidence
- reply and forward source-attachment handling
- bounded search and bulk folder-action controls
- TLS posture validation
- host readiness and carry-forward V2 evidence
- sanitized release evidence archive generation
- pilot rehearsal evidence for selected daily-driver workflows

That list is dry, but it is the release.

For security-sensitive software, the feature is not done when the route exists. It is done when the route has a defined boundary, a failure mode, a test, host evidence where needed, and a release gate that will complain if any of those pieces go stale.

* * *

## The Final Gate Passed On The Real Host

The final closeout gate was run on:

```text
mail.blackbagsecurity.com
```

The release command was the strict release path:

```text
make release-check
```

That matters because the local workstation and the OpenBSD host are not the same environment.

The local workstation can be useful for development. It is not the final proof environment. The release gate has to survive the target host, target shell tools, target service layout, target permissions, target mail substrate, and target runtime assumptions.

The final mail-host release gate passed:

- locked Cargo build
- locked Cargo tests
- clippy
- formatting check
- RustSec advisory review
- cargo-deny source and license policy
- duplicate dependency backstop
- dependency inventory generation
- documentation governance guard
- TLS policy guard
- TLS standard validation
- V2 carry-forward evidence checks
- host-readiness evidence checks
- helper-boundary evidence checks
- resource and timeout evidence checks
- live MIME and HTML proof checks
- authenticated WSTG release evidence checks
- selected-cohort pilot rehearsal evidence checks
- sanitized release archive generation

The Rust test suite reported:

```text
432 passed
0 failed
4 ignored
```

The ignored tests are live-surface tests that require a host with the relevant Dovecot mailbox or auth surface. They are not silently counted as release proof. The release gate relies on the explicit host-backed evidence lanes for the live behavior it needs to prove.

* * *

## WSTG Became Accountability, Not Decoration

The final WSTG release run produced:

```text
pass: 46
fail: 0
warning: 0
skip: 0
release_errors: []
```

That is a stronger result than the earlier V3 foundation state.

At the beginning of V3, the WSTG pack was already useful, but it was not yet a complete closeout instrument. It needed to become more honest about what each row actually proved.

That distinction mattered most in the authenticated and input-validation rows.

### Command Injection Evidence Had To Stop Overclaiming

OSMAP has real command boundaries.

It calls local authentication and mail tooling. It hands messages to local submission paths. It talks to helper-backed mailbox operations. That is not something to wave away as "not applicable."

Earlier command-injection evidence had a subtle overclaim: some authenticated mutation probes used invalid CSRF tokens. That proved the CSRF gate rejected shell-shaped input before the downstream handler, but it did not prove the downstream command boundary for those mutation routes.

The fix was not to pretend the old claim was fine.

The fix was to classify the surfaces honestly:

- `command_reachable`
- `auth_gate`
- `csrf_gate`
- `auth_csrf_gate`

Authenticated read and search surfaces are command-reachable and were tested as such. Mutation routes with invalid CSRF are now recorded as precondition-gate evidence, not downstream command-boundary proof.

That is the kind of small wording change that matters. A senior appsec reviewer should be able to read the evidence and understand what was tested without having to infer the real boundary from the code.

### Input Validation Was Made More Specific

V3 added or tightened evidence around:

- SMTP header and newline injection
- recipient grammar
- subject newline rejection
- mailbox, UID, and search tampering
- attachment filename handling
- attachment content-type normalization
- HTTP method tampering
- unsupported content types
- duplicate parameters
- host-header injection
- HTTP splitting and smuggling shapes

The host-header work is a good example.

The untrusted Host probe now fails with:

```text
421 Misdirected Request
```

That is better than merely observing that the application did not reflect the hostile host string. It shows the public edge is participating in the boundary instead of leaving the Rust application alone to reason about a request that should not have been accepted as canonical in the first place.

### Throttling Had To Be Observable

Authentication throttling also needed evidence cleanup.

The final `ATHN-003` evidence records not only response statuses, but throttle signals:

```text
attempt_5:body_marker
attempt_6:body_marker
```

That matters because "six 401s" and "throttling was observed" are not the same claim unless the evidence records how throttling was observed.

Release evidence should not require charitable reading.

### Not Applicable Had To Be Defensible

The final `INPV-007` row covers remaining injection classes such as SQL, LDAP, XML, XPath, SSI, SSTI, SSRF, and related applicability decisions.

That row was hardened late in closeout because the original source scan only inspected top-level Rust files under `src/*.rs`.

That was not good enough.

The runner now recursively scans:

```text
src/**/*.rs
```

The same pass also made one important interpretive correction: OSMAP's command-execution boundaries are not treated as "not applicable." They are applicable, and they are covered by `OSMAP-WSTG-INPV-003`.

That is the difference between a checklist and a real review.

* * *

## The Authenticated Evidence Was Intentionally Human

The final WSTG run used prompt-based authentication.

That means the release evidence proved that real browser authentication occurred with:

- password entry
- current TOTP
- session issuance
- protected route access
- logout
- stale-cookie rejection
- authenticated browser flows

The password and TOTP seed were not stored in the repository.

That friction was deliberate.

Automating everything is attractive until "everything" includes long-lived credentials that turn the evidence harness into a secret store. For this project, the better pattern was:

- collect the raw proof interactively
- keep raw terminal prompts out of git
- sanitize the release summary
- archive only evidence that can survive disclosure
- make missing authenticated proof release-blocking

That pattern is slower than a headless CI job.

It is also much safer for a small, high-consequence mail system.

* * *

## What Was Archived

V3 closeout produced two kinds of artifacts.

The first kind is the source-control release marker:

```text
v3.0.0
```

That tag points at:

```text
2aefef21ea061440db284b22b3f7c1698e4afda8
```

The second kind is the generated release evidence bundle.

The final evidence artifacts were preserved outside the git tree:

```text
/home/foo/Workspace/OSMAP-release-artifacts/v3.0.0/
/home/foo/OSMAP-release-artifacts/v3.0.0/
```

The final archive checksum was:

```text
02c7a80c8c1350417434c5b418bc139f97c11947fe3f1de4494a015ca4239977  osmap-v3-release-evidence.tar.gz
```

The final artifact checksums were:

```text
eb1ddf2d485e29b6c3d1935f14a6faf0895e18b84afc9a3e0f0029c972e0e3c1  osmap-v3-release-evidence-summary.json
069ee61a4933c41cba21ab402799555842beb8fe8810054b93c63cb85da10c2d  osmap-v3-release-evidence-summary.md
02c7a80c8c1350417434c5b418bc139f97c11947fe3f1de4494a015ca4239977  osmap-v3-release-evidence.tar.gz
3ea99f8d0bfefd36e13bc4c8c93fdbfeea510f57889224cdf04635e08f3cea8a  osmap-wstg-release-summary.json
```

The evidence archive records:

- the assessed ref
- the host target
- release command
- Cargo build, test, clippy, and formatting status
- supply-chain status
- dependency inventory status
- WSTG summary status
- authenticated WSTG status
- V2 carry-forward evidence checked
- host-readiness evidence checked
- TLS CBC and TLS standard evidence checked
- resource-timeout evidence checked
- helper-boundary evidence checked
- V3 MIME and HTML proof evidence checked
- V3 pilot rehearsal evidence checked
- sanitized archive status
- skipped checks

The final release evidence reported no skipped checks.

* * *

## Why The Final Evidence Was Not Committed Again

There is an annoying but important release-engineering detail here.

Generated release evidence includes the commit it assessed.

If I commit that generated evidence, the repository head changes. Then the evidence no longer describes the new head. If I regenerate evidence and commit it again, I create another new head.

That can become an evidence-chasing loop.

The right answer for this closeout was:

- tag the validated source commit
- preserve the generated evidence bundle outside the source tree
- record checksums
- keep the repository clean
- avoid pretending a generated-evidence commit is the same thing as the assessed application commit

That may sound like bookkeeping.

It is actually part of the honesty model.

Evidence should identify what it assessed. A tag should identify what is being released. A generated archive should be preserved with enough integrity metadata to be reviewed later. Those are related objects, but they are not the same object.

* * *

## What V3 Added

The most visible V3 workflow additions were about continuity:

- save and resume drafts
- list drafts
- delete drafts
- send and clean up accepted drafts
- preserve failed sends for retry
- reply and forward with explicit source-attachment selection
- re-fetch selected source attachments at send time
- reject duplicate, tampered, stale, missing-CSRF, and cross-origin source-attachment cases
- support bounded search refinements and sorting
- support bounded bulk folder actions
- expose session/device policy more clearly

Those are user-facing improvements.

But V3's real value is that those improvements were forced through the same boundary discipline as the rest of OSMAP:

- authenticated routes require valid sessions
- state-changing routes require CSRF and same-origin metadata
- inputs are bounded
- duplicate fields are rejected
- stale sessions fail closed
- helper-backed operations stay budgeted
- evidence is redacted
- audit output avoids raw secrets

V3 did not try to become a full groupware platform.

It did not add calendars, contacts, a broad admin console, remote external content loading, a mobile app, OpenPGP, a JavaScript-heavy client, or unbounded mailbox-wide operations.

Those exclusions are not accidents. They are part of the release.

* * *

## What V3 Proved About The Host

OSMAP is not just a Rust binary.

It is a browser-facing access layer running in an OpenBSD mail environment with nginx, Dovecot, Postfix, Rspamd, privilege-separated service users, helper sockets, state directories, secret directories, audit logs, and service wrappers.

V3 evidence had to prove that the host still supported the intended boundary.

That included:

- nginx public-edge behavior
- loopback OSMAP binding
- service health
- PF posture
- file and directory permissions
- helper socket permissions
- TLS configuration
- no dangling takeover CNAMEs for relevant public names
- selected live validators running against the expected checkout

This is why the final closeout was not allowed to be local-only.

The deployment model is part of the trusted computing base. If the proof ignores the host, the proof is incomplete.

* * *

## What V3 Is Not Claiming

V3 is not claiming that OSMAP is perfect.

It is not claiming that standards compliance alone proves security.

It is not claiming that a small WSTG pack is the same thing as an independent manual penetration test.

It is not claiming that the project should now accelerate into broad feature accumulation.

The claim is narrower:

- the V3 boundary is implemented
- the release gate passed on the intended host
- the WSTG evidence is authenticated and current for the assessed release
- the major V3 workflow additions have tests and evidence
- the host posture was checked
- the release artifacts were sanitized and archived
- the final tag identifies the closed V3 release

That is enough to close V3.

It is not enough to stop being careful.

* * *

## Lessons From V3 Closeout

The first lesson is that stale evidence is a bug.

The code can be correct and the release can still be unready if the evidence points at the wrong commit, old behavior, or old wording.

That happened more than once during V3. The correct response was not to hand-wave it away. The correct response was to refresh, repin, and re-run.

The second lesson is that security evidence needs adversarial review too.

A test can pass and still overclaim. `INPV-003` was the clearest example. The runner was improved not because the application suddenly became insecure, but because the evidence needed to say exactly what it proved.

The third lesson is that release gates should be allowed to be annoying.

Prompt-auth WSTG runs, host-side toolchain checks, OpenBSD-specific validators, and sanitized evidence archives are all slower than a simple green CI badge.

That is fine.

OSMAP is not trying to optimize for the fastest possible release ceremony. It is trying to make browser-facing mail access more defensible.

The fourth lesson is that generated evidence and source history need a clean relationship.

For V3, the final evidence bundle was preserved as a release artifact with checksums instead of repeatedly committing generated files that would immediately make themselves stale. That pattern is worth keeping.

* * *

## Where V4 Starts

V4 should not begin as a feature wish list.

The right starting theme is:

**operational resilience and user confidence.**

That means V4 should begin with definition and roadmap work before code:

- `V4_DEFINITION.md`
- `V4_ROADMAP.md`
- explicit out-of-scope boundaries
- release gates
- evidence expectations
- slice ordering

The strongest initial V4 areas are likely:

- mailbox and search performance observability
- backup, restore, and disaster-recovery rehearsal
- operator diagnostics that do not expose secrets
- broader real-world message corpus coverage
- usability hardening for daily workflows

V4 should not begin by adding large new mail-client features.

The discipline that made V3 closable is the same discipline that should shape V4: narrow scope, clear threat boundaries, live evidence, and a refusal to confuse convenience with security.

* * *

## Closing Thought

The point of V3 was not to make OSMAP louder.

It was to make OSMAP more accountable.

The useful question at closeout was not:

Did the project add features?

The useful question was:

Can the project prove, on the real host, with authenticated evidence, that the new daily-driver workflows stayed inside the intended security boundary?

For V3, the answer is yes.

That does not make OSMAP finished.

It makes the V3 claim reviewable.

And for this kind of software, reviewable is a much better word than done.

Repository: <https://github.com/unattributed/OSMAP>