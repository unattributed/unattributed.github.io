---
layout: post
title: "OSMAP V5: Identity, Origin, and Response Boundaries in Production"
date: 2026-06-14
author: unattributed
categories: [security-engineering, openbsd, release-engineering, email-security]
tags: [osmap, openbsd, webmail, identity-boundary, origin-policy, host-header, response-headers, release-gates, evidence]
---

OSMAP V5 is closed.

That sentence is intentionally narrow.

It does not mean OSMAP is finished. It does not mean browser-facing mail is now a solved problem. It does not mean every future request shape, deployment mistake, proxy behavior, or operational edge case has been exhausted.

It means something more specific:

**OSMAP V5 strengthened the identity, host, origin, response-header, session-record, and HTTP-framing boundaries around the browser-facing mail application, and that boundary-hardening work is now deployed, verified, and recorded.**

That distinction matters.

V4 focused on hostile message content.

V4 asked whether OSMAP could render hostile mail without allowing that mail to become active browser behavior inside the authenticated message view.

V5 asked a different question:

**Does OSMAP still know who the authenticated mailbox identity is, which browser origin is allowed to act, which host name is canonical, which response headers are safe to emit, and which HTTP request shapes should be rejected before they become application state?**

For V5, the answer is now evidence-backed.

Not absolute.

Not magical.

Not a claim that OSMAP is secure against everything.

But inside the OSMAP trust boundary, V5 makes the surrounding webmail boundary more explicit, more testable, and more operationally defensible.

* * *

## What V5 Provides

Version 5 is an identity, origin, host, and response-boundary hardening release.

The visible user experience should not feel dramatically different.

That is deliberate.

V5 was not a feature sprint. It was not about making OSMAP look more like Roundcube. It was not about adding plugins, JavaScript-heavy interface behavior, remote content toggles, attachment previews, or broad groupware features.

The V5 work focused on the controls that sit around the mail view:

- canonical mailbox identity validation
- session-record identity validation
- configured host enforcement
- stronger Origin and Referer handling
- same-origin expectations for state-changing routes
- safer response-header construction
- consistent security headers on plain-text and HTML responses
- stricter HTTP request parsing and framing rejection
- production deployment of the new boundary policy
- post-deployment evidence and documentation

That is the release.

The value of V5 is that OSMAP now has a clearer answer when asked:

**What stops a browser-facing mail request from being accepted under the wrong identity, wrong host, wrong origin, unsafe response shape, or ambiguous HTTP framing?**

Before V5, several of those answers existed in parts of the system.

After V5, they are much more directly expressed in code, tests, deployment configuration, and production evidence.

* * *

## Why V5 Follows V4

V4 closed the hostile-content containment claim.

That was an important milestone because email content is attacker-controlled input. A webmail application cannot treat message bodies, MIME structures, links, charsets, attachment names, or HTML as trusted.

But hostile content is not the only boundary that matters.

A browser-facing mail application also has to answer more basic questions:

- Which mailbox identity is authenticated?
- Is the identity returned by the backend shaped like a mailbox identity OSMAP is willing to trust?
- Is the session record still valid, or has it been tampered with?
- Is this request addressed to the canonical service host?
- Is this state-changing request same-origin?
- Are proxy-derived client addresses trusted only across the intended loopback boundary?
- Can a response accidentally emit unsafe headers?
- Can ambiguous HTTP framing confuse the request parser?
- Does a production deployment actually enforce the host policy that the code expects?

V5 was about those questions.

V4 made hostile message content less ambiguous.

V5 makes the surrounding browser-mail trust boundary less ambiguous.

That is why V5 is a natural follow-on release.

A webmail application can strip hostile HTML and still be weak if it accepts the wrong Host header, trusts malformed session records, emits unsafe response headers, or lets ambiguous request framing reach protected routes.

V5 reduces those gaps.

* * *

## Canonical Identity Became A First-Class Boundary

Mail systems are full of identity strings.

Some are user-submitted. Some are returned by authentication tooling. Some are stored in session state. Some are logged. Some are used to scope mailbox operations.

That makes identity validation a security boundary.

V5 added a canonical mailbox identity layer so OSMAP is stricter about what it will treat as an authenticated mailbox identity.

The important idea is simple:

**a backend authentication success is not enough if the returned identity is malformed, hostile, or not shaped like a mailbox identity OSMAP is willing to bind to a session.**

V5 therefore rejects hostile canonical identity values before they become trusted browser session state.

That includes identity shapes that could confuse logs, poison session records, smuggle control characters, resemble shell-shaped input, or otherwise escape the conservative mailbox identity model.

This is not glamorous work.

It is the kind of work that matters in a small mail application.

A mail session should not be a loose string bag. It should have a bounded user identity with a predictable shape and a narrow meaning.

V5 makes that clearer.

* * *

## Session Records Had To Defend Their Own Boundary

Session state is part of the authenticated browser boundary.

If a session record is malformed, tampered with, or contains an identity value that OSMAP would not have accepted during login, the correct behavior is not to keep going.

The correct behavior is to reject it.

V5 added stronger validation of stored session identity fields. That means session records are no longer treated as safe merely because they exist on disk in the expected location.

The identity inside the record still has to be valid.

That matters for two reasons.

First, it reduces the chance that a malformed or hostile identity value can survive across requests through persisted session state.

Second, it keeps the identity model consistent. The same conservative mailbox identity expectations apply when a session is issued and when a session is later validated.

That is how security boundaries should behave.

They should not be strong on entry and forgiving afterward.

* * *

## The Host Boundary Became Explicit

V5 added explicit allowed-host enforcement.

The production policy is:

```text
OSMAP_ALLOWED_HOSTS=mail.blackbagsecurity.com
```

This is not an IP pin.

That point is important because the production host uses DDNS and also supports WireGuard split DNS.

When WireGuard is down, the public name resolves to the current WAN address.

When WireGuard is up, the same name can resolve privately to the WireGuard address.

In both cases, the browser still requests:

```text
mail.blackbagsecurity.com
```

The HTTP `Host` value remains the same. The TLS name remains the same. The browser-facing authority remains the same.

That is the value OSMAP should validate.

OSMAP should not be configured with the current ISP-assigned WAN IP. That address can change. OSMAP should also not need to accept direct browsing to `10.44.0.1` unless direct IP browsing is intentionally part of the boundary.

For this deployment, it is not.

The correct host boundary is the DNS name:

```text
mail.blackbagsecurity.com
```

The production validation confirmed the intended behavior:

```text
valid Host: mail.blackbagsecurity.com -> 200
invalid Host: attacker.invalid -> 421
```

The public edge also rejects wrong-host traffic before it reaches the application.

That gives OSMAP two useful layers:

- nginx rejects non-canonical public hosts
- OSMAP rejects unconfigured hosts at the application boundary

That is the right model.

The edge should help.

The application should still know its own canonical host.

* * *

## Origin And Referer Checks Became Stricter

Cookies alone are not enough for browser-facing state changes.

A browser may attach cookies to requests that did not originate from the intended page. That is why OSMAP already treated CSRF and same-origin behavior as part of the application boundary.

V5 tightened that boundary further.

State-changing routes now have stronger expectations around Host, Origin, Referer, and Fetch Metadata behavior.

That matters for routes such as:

- login
- logout
- session revocation
- settings changes
- draft actions
- message movement
- sending mail
- other authenticated mutations

The important claim is not that Origin and Referer headers are perfect.

They are not.

The important claim is that OSMAP is no longer treating state-changing requests as valid merely because a cookie is present and a route exists.

V5 makes the browser request context part of the decision.

That is the right posture for a no-JavaScript, server-rendered, authenticated mail interface.

The browser is allowed to submit OSMAP forms from OSMAP.

It is not allowed to silently turn another origin into an OSMAP command surface.

* * *

## Response Headers Became A Guarded Output Surface

Security work often focuses on input.

V5 also focuses on output.

HTTP response headers are part of the browser security boundary. A bad header can create cache exposure, content-type confusion, framing problems, cross-origin surprises, or even header-splitting risk if construction is too loose.

V5 added central response-header validation and extended the coverage so directly constructed responses are also checked.

That last detail matters.

It is not enough to have a safe helper if some routes can bypass the helper with manually constructed response objects. Security helpers become weaker when they are optional.

V5 therefore added validation around response serialization itself.

That means invalid header names, CRLF header-value splitting, and unsafe directly constructed response headers are rejected by tests before they become a production pattern.

V5 also made security headers more consistent on plain-text responses such as `/healthz`.

The public health check now includes headers such as:

```text
cross-origin-resource-policy: same-origin
referrer-policy: no-referrer
x-content-type-options: nosniff
```

That does not make `/healthz` a sensitive route.

It makes the response policy less inconsistent.

Consistency matters.

Security headers should not depend on whether a route happens to return HTML.

* * *

## HTTP Framing Became Less Forgiving

OSMAP is intentionally small, but it still accepts HTTP traffic.

That means it has to decide what to do with ambiguous or suspicious HTTP shapes.

V5 strengthens rejection behavior around request parsing and framing issues, including cases such as:

- missing Host on HTTP/1.1 requests
- empty Host headers
- Host headers with path characters
- duplicate headers
- duplicate cookies
- duplicate query parameters
- duplicate Content-Length behavior
- unsupported Transfer-Encoding
- GET requests with bodies
- POST requests without required content length
- extra bytes after the declared body length
- pipelined second requests
- request targets with fragments
- request targets with dot segments
- request targets with non-normalized slashes
- oversized request targets
- oversized cookie headers

That list is not exciting.

It is exactly what a browser-facing application should care about.

Ambiguous HTTP input should not be normalized into something convenient after it has already crossed the boundary. The safer default is to reject shapes the application does not need.

This fits OSMAP's overall philosophy:

do less, accept less, prove more.

* * *

## The Deployment Lesson Was Part Of V5

V5 was not only a code exercise.

It was deployed to the real OpenBSD mail host:

```text
mail.blackbagsecurity.com
```

The deployed V5 boundary-hardening commit was:

```text
927516f77dd7a92e199ced8f5f90fe894e584a48
```

The live production binary checksum after cutover was:

```text
3b72992bb468ee08f5db120a4c1c64e6a681cbbae4b7c3dfee10a96edf032f61
```

The final service state was:

```text
osmap_serve(ok)
osmap_mailbox_helper(ok)
```

The public validation passed:

```text
https://mail.blackbagsecurity.com/healthz -> HTTP/2 200
https://attacker.invalid/healthz resolved to the same address -> HTTP/2 421
```

The deployment also exposed a useful operational lesson.

The first cutover attempt mixed binary replacement, service restart, and environment-file changes. The service environment file permissions became part of the problem.

The correct production permission model is:

```text
/etc/osmap/osmap-serve.env
root:osmaprt
0640
readable by _osmap
```

That matters because the OpenBSD `rc.d` service runs the browser-facing launcher as `_osmap`. If the environment file is replaced with the wrong group ownership, the service user cannot read the configuration it needs at startup.

The final deployment corrected that.

The binary and environment file were treated as one deployment unit.

Rollback artifacts were retained for both:

```text
backup binary:
/usr/local/bin/osmap.pre-v5-retry-20260614T132818Z

backup env:
/etc/osmap/osmap-serve.env.pre-v5-retry-20260614T132818Z
```

That is an important V5 outcome.

The security boundary is not only in Rust code.

It is also in the OpenBSD service model, file permissions, env ownership, restart order, and rollback plan.

* * *

## The Evidence Was Recorded In The Project

After production validation, the project recorded the V5 deployment completion in source history.

The documentation commit was:

```text
4961d099dc09b53e1792a5992d652fd43cc98b93
```

The record added:

```text
docs/V5_PRODUCTION_DEPLOYMENT_COMPLETE.md
```

and updated:

```text
docs/DECISION_LOG.md
```

That record captured:

- deployment target
- deployed V5 commit
- live binary checksum
- production host policy
- service state
- local valid-host check
- local invalid-host check
- public valid-host check
- public invalid-host check
- rollback artifact paths
- operational lesson about env ownership and rollback units

This matters for the same reason it mattered in V3 and V4.

A security milestone should not live only in terminal scrollback.

It should be preserved in a form the project can review later.

* * *

## CodeQL Found A Test Hygiene Issue

After V5 was merged and deployed, GitHub CodeQL flagged a hard-coded cryptographic value in a test.

The finding was on a test credential fixture used in an authentication test. It was not production credential material. The test was checking rejection of a hostile backend canonical identity value, not validating a real password.

From a production-risk perspective, the finding was a false positive.

But it was still worth fixing.

The first fix changed the literal `"password"` to a clearer non-secret test fixture. CodeQL still tracked the literal into the password parameter.

The second fix removed the literal credential fixture entirely and generated the throwaway test value at runtime.

The final cleanup commit was:

```text
d08be38191371e3a766a02b18c38bda0e4a4746f
```

The alert state became:

```text
fixed
```

No production redeploy was required because this was test-only cleanup.

This is worth mentioning because it reflects the project posture.

Not every scanner alert is a real production vulnerability.

But a false positive can still be an opportunity to make intent clearer, reduce future reviewer noise, and keep the security dashboard honest.

That is what happened here.

* * *

## What V5 Is Not Claiming

V5 is not claiming that OSMAP is perfect.

It is not claiming that every possible proxy behavior has been modeled.

It is not claiming that every possible browser edge case is exhausted.

It is not claiming that host-header enforcement alone is sufficient.

It is not claiming that Origin and Referer checks are a complete CSRF defense by themselves.

It is not claiming that response headers replace safe application logic.

It is not claiming that stricter HTTP framing is the same thing as a full independent protocol audit.

It is not claiming that the production environment can never drift.

It is not claiming Roundcube parity.

Those are deliberate non-claims.

The V5 claim is narrower:

- OSMAP validates canonical mailbox identity before trusting authenticated session state
- tampered session identity records are rejected
- production Host policy is explicit
- invalid Host values are rejected
- state-changing routes have stronger same-origin request metadata checks
- response headers are centrally validated
- direct response construction is covered by tests
- plain-text responses receive security headers
- ambiguous HTTP request shapes are rejected
- deployment evidence exists on the real OpenBSD host
- the production configuration works with DDNS and WireGuard split DNS
- the deployment lesson about env ownership and rollback was recorded
- CodeQL test-fixture noise was cleaned up

That is enough to close V5.

It is not enough to stop being careful.

* * *

## What V5 Adds To The Project

V5 changes OSMAP by making the browser-facing boundary more complete.

Before V5, the project already had:

- a narrow OpenBSD-native design
- a privilege-separated mailbox helper model
- public deployment readiness
- daily-driver workflow evidence
- hostile-content containment evidence
- WSTG-aligned testing
- live-host proof patterns
- release-gate discipline

After V5, OSMAP has a stronger surrounding boundary for the authenticated browser session.

That matters because hostile mail is not the only attacker-controlled input.

The request itself is input.

The Host header is input.

The Origin header is input.

The Referer header is input.

The request target is input.

The cookie header is input.

The session record is input.

The backend identity is input.

The response object is an output surface that has to remain bounded.

V5 makes those assumptions more explicit.

That is a major improvement.

It is not a broad feature milestone.

It is a trust-boundary milestone.

* * *

## Lessons From V5

The first lesson is that production deployment is part of the security boundary.

A binary that passes tests can still fail if the service account cannot read the env file. A host policy can be correct in theory and still not active in the running process until the service restarts cleanly.

The deployment process has to verify both code and host reality.

The second lesson is that rollback must include configuration.

Rolling back only the binary was not enough while the service env still carried the V5-specific configuration shape and permission assumptions.

The correct rollback unit is larger:

```text
/usr/local/bin/osmap
/etc/osmap/osmap-serve.env
osmap_mailbox_helper
osmap_serve
```

The third lesson is that split DNS and DDNS do not conflict with Host enforcement.

The correct OSMAP allowed-host value is the canonical browser host:

```text
mail.blackbagsecurity.com
```

not the dynamic WAN IP and not the WireGuard IP.

That makes the boundary more stable, not less.

The fourth lesson is that scanner noise should be reduced where it is cheap and honest to do so.

The CodeQL hard-coded credential alert was not a production vulnerability, but leaving it open would have made the dashboard less useful. Cleaning it up improved reviewer signal without changing runtime behavior.

The fifth lesson is that V5 continues the same pattern as V3 and V4:

define the claim, implement the boundary, test it locally, prove it on the host when needed, document the result, and keep the wording narrower than the engineering effort.

That pattern is becoming the most important part of OSMAP.

* * *

## Where V6 Starts

V6 should not begin by expanding the trust boundary.

The safest next work is not a large feature sprint.

The strongest starting point for V6 is probably operational reliability, deployment repeatability, and post-deployment observability.

V5 exposed the need for better upgrade automation.

A future release should consider:

- deployment runner with automatic binary and env rollback
- service permission preflight
- OpenBSD `rc.d` timeout behavior review
- post-cutover public and local health validation
- evidence archive generation for production upgrades
- explicit split-DNS and DDNS validation gates
- log review that separates scanner noise from meaningful boundary failures
- operational dashboards that avoid exposing secrets
- backup and restore rehearsal for OSMAP state
- disaster-recovery proof for mail access continuity

Those are not flashy features.

They are the right kind of next work.

OSMAP does not need to become a broad groupware suite to become more useful.

It needs to become easier to operate safely.

* * *

## Closing Thought

The point of V5 was not to make OSMAP louder.

It was to make the browser-facing trust boundary harder to confuse.

The useful question at V5 closeout was not:

Did the project add more mail features?

The useful question was:

Can the project prove that authenticated identity, session records, Host policy, same-origin expectations, response headers, HTTP framing, and deployment configuration now behave as explicit boundaries on the real service?

For V5, the answer is yes.

That does not make OSMAP finished.

It makes the V5 boundary reviewable.

And for a secure webmail replacement, reviewable is still the word that matters.

Repository: <https://github.com/unattributed/OSMAP>