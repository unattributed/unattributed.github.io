---
layout: post
title: "OSMAP V4: Hostile Content Containment Without Pretending Email Is Safe"
date: 2026-06-13
author: unattributed
categories: [security-engineering, openbsd, release-engineering, email-security]
tags: [osmap, openbsd, webmail, hostile-content, mime, html-sanitization, release-gates, evidence]
---

OSMAP V4 is closed.

That sentence is intentionally narrow.

It does not mean email is safe. It does not mean hostile attachments are harmless. It does not mean rich HTML mail is solved. It does not mean OSMAP is trying to become Roundcube with a smaller logo.

It means something more specific:

**OSMAP V4 contains hostile message content inside the browser-mail boundary, with evidence strong enough that I am willing to treat the V4 hostile-content claim as closed.**

That distinction matters.

Email is attacker-controlled input. In a webmail application, that input is eventually placed near an authenticated browser session. That makes message rendering one of the most important parts of the application boundary.

V3 made OSMAP more usable as a daily-driver webmail system without letting convenience overwhelm the security model.

V4 had a different job.

V4 had to answer this question:

**Can OSMAP let a user view hostile mail without giving that mail active browser execution, automatic remote fetches, invisible unsafe navigation, or unsafe attachment serving by default?**

For V4, the answer is yes.

Not absolutely.

Not magically.

Not outside the OSMAP boundary.

But inside the browser-mail boundary that OSMAP actually owns, V4 makes the hostile-content claim reviewable.

* * *

## What V4 Provides

Version 4 is a hostile-content containment release.

The important word is containment.

OSMAP does not claim to make hostile email globally safe. It does not claim to disinfect files after they leave the application. It does not claim to inspect malware. It does not claim that every external link is trustworthy.

Instead, V4 tightens the places where attacker-controlled message content reaches the browser-facing application:

- MIME body selection
- sanitized HTML rendering
- external-link treatment
- automatic remote-content suppression
- attachment download behavior
- evidence redaction
- hostile-content regression coverage
- live-host proof

That is the release.

The value of V4 is not that it adds another user-visible mail feature. The value is that it makes a sharper security claim about hostile content and then forces the code, tests, live evidence, and documentation to match that claim.

* * *

## The V4 Boundary

The V4 boundary is:

**OSMAP contains hostile message content inside the browser-mail boundary.**

That means hostile mail should not be able to turn the authenticated message view into an active browser execution environment.

In practical terms, V4 expects hostile HTML to lose the parts that make it dangerous in a webmail context:

- script payloads
- event handlers
- forms and credential-harvest controls
- unsafe URL schemes
- relative and protocol-relative links
- SVG and MathML browser surfaces
- frames, objects, embeds, templates, media, and source tags
- CSS-based fetch and tracking surfaces
- metadata refresh behavior
- inline remote images and tracking pixels
- inline `cid:` image rendering
- comments and hidden active markup that would confuse review

V4 also expects preserved links to be visible and disclosed. If OSMAP keeps a reviewed external link, the destination should be visible to the user rather than hidden behind styling or invisible markup.

That is an important difference from a naive sanitizer.

A naive sanitizer asks:

Did we remove the obviously dangerous tags?

V4 asks:

Can the user review what remains, and can the release evidence prove the removed payload classes did not survive browser rendering?

That is a better question.

* * *

## Why Hostile Mail Is A Different Problem

A normal web page is expected to run code.

A webmail message is not.

That makes webmail unusual. It has to render attacker-controlled content inside an authenticated application while avoiding the assumptions that make ordinary web pages work.

The sender does not get to run JavaScript in the recipient's mail session.

The sender does not get to silently load remote tracking resources.

The sender does not get to smuggle form controls into the message view.

The sender does not get to turn an attachment route into active browser content.

The sender does not get to make the evidence trail leak private message bodies or secrets.

Those are not cosmetic requirements.

They are the heart of the browser-mail boundary.

OSMAP already avoided large parts of the modern webmail attack surface by staying server-rendered, dependency-light, and no-JavaScript for the mail interface. V4 takes that philosophy and applies it directly to hostile message content.

That is where V4 provides real value.

It does not make OSMAP more flashy.

It makes the dangerous part of webmail less ambiguous.

* * *

## Sanitized HTML Had To Become More Defensive

V3 already included MIME and HTML proof.

V4 pushes that further.

The goal was not simply to render HTML pleasantly. The goal was to make hostile HTML inert before it reached the browser.

That meant the sanitizer had to handle more than obvious `<script>` tags.

Hostile mail rarely arrives as one clean payload. It arrives as mixed-case schemes, entity-obfuscated links, malformed markup, SVG tricks, CSS fetch surfaces, relative URLs, protocol-relative links, hidden form controls, autofocus payloads, tracking pixels, and weird MIME structures that try to force the renderer into a confusing decision.

V4 treats those as release concerns.

The hostile-content matrix now covers classes such as:

- raw and encoded script payloads
- mixed-case and entity-obfuscated URL schemes
- `javascript:`, `data:`, `blob:`, `cid:`, `file:`, relative, and protocol-relative targets
- form and input credential-harvest payloads
- CSS import and background URL behavior
- SVG, MathML, iframe, object, embed, template, audio, video, and source tags
- tracking pixels and inline image references
- malformed multipart messages
- nested MIME structures
- suspicious charsets
- header-count and part-count abuse
- spoofed filenames
- attachment deception
- unicode subject deception

That list is not glamorous.

It is exactly the kind of list a mail client has to care about.

* * *

## Remote Content Had To Stay Suppressed

Remote content is one of the oldest privacy failures in mail clients.

An image or tracking pixel can disclose that a message was opened. It can disclose timing. It can disclose network information. It can also become part of a larger attack chain when a client treats remote content as ordinary display material.

OSMAP's posture remains simple:

**remote message resources should not load automatically.**

V4 reinforces that posture.

The live hostile-content proof records that hostile HTML markers intended to trigger remote fetches do not survive the rendered message body. The V4 assurance report also records zero observed remote fetch surfaces, zero beacon requests, zero WebSocket requests, and zero service worker registrations.

That matters because "we stripped the tag" is not quite the same as "the browser had no observed auto-fetch surface in the route-backed message view."

The first is an implementation statement.

The second is release evidence.

V4 needed the second.

* * *

## Attachments Had To Be Treated As Downloads, Not Previews

Attachment handling is another place where webmail systems can quietly expand their attack surface.

A user sees an attachment. The browser sees a response with a content type, headers, filename, and bytes. If the application serves browser-executable content too casually, a downloaded attachment can become active browser content.

V4 hardens that boundary.

For browser-executable attachment types such as HTML, SVG, XML, script-like content, and related risky media, OSMAP's expected behavior is:

- force download
- emit `Content-Disposition: attachment`
- include `X-Content-Type-Options: nosniff`
- downgrade risky served content to `application/octet-stream`
- preserve `Cross-Origin-Resource-Policy: same-origin`
- avoid trusting deceptive filenames as security decisions
- avoid leaking attachment bodies into committed evidence

The live V4 proof validated HTML, SVG, and JavaScript attachment downloads on the real host. The current hostile assurance report records five attachment routes forcing download with `nosniff`, with active attachment media downgraded.

That does not mean the file is safe after the user opens it elsewhere.

It means OSMAP is not serving that file as active browser content by default.

That is the correct claim.

* * *

## MIME Ambiguity Had To Fail Closed

MIME is one of the most error-prone parts of email security.

The problem is not only malicious HTML. It is also deciding which part of a strange message should be displayed, which charset should be trusted, how deeply to parse nested structures, how many parts to tolerate, how many headers are too many, and what to do when a message is malformed enough that a forgiving renderer might make a dangerous choice.

V4 adds stronger evidence around malformed, ambiguous, unsupported, and oversized MIME inputs.

The expected behavior is not heroic recovery.

The expected behavior is safer:

- fail closed
- withhold unsafe or unsupported bodies
- render explicit placeholders where appropriate
- enforce bounded depth
- enforce bounded part counts
- enforce bounded header counts
- avoid panics
- avoid private-data leakage
- avoid rendering unsafe content simply because the parser found something displayable

The hostile assurance report records bounded handling for malformed boundaries, invalid transfer encodings, deep nesting, header count, part count, and boundary length checks.

That is the right kind of boring.

For a secure mail application, boring failure behavior is a feature.

* * *

## The Hostile Corpus Became Release Evidence

V4 added a version-controlled hostile mail corpus under:

```text
tests/testdata/hostile-mail-corpus/
```

The corpus includes twelve fixtures across eleven required categories.

Those categories include hostile HTML, CSS abuse, tracking attempts, CID abuse, unicode deception, suspicious links, malformed headers, nested MIME structures, suspicious charsets, spoofed filenames, and attachment deception.

The corpus is not just documentation.

It feeds the V4 hostile assurance gate:

```text
maint/security/osmap-v4-hostile-assurance-gate.sh
```

That gate validates fixture metadata, executes the V4 hostile assurance test, writes a machine-readable report, and archives the evidence bundle.

The current report records:

```text
status: passed
```

It also records:

```text
12 fixtures cover 11 required categories
```

and:

```text
rendered_message_routes: 3
attachment_download_routes: 5
remote_fetches: 0
beacon_requests: 0
websocket_requests: 0
service_worker_registrations: 0
```

Those numbers are useful because they make the V4 claim more concrete.

The claim is not simply "we added tests."

The claim is that hostile fixtures were mapped to browser and attachment behavior, route-backed observations were collected, unsafe network surfaces were checked, and an evidence archive was produced.

That is what turns a security intention into a release gate.

* * *

## The Live Proof Still Had To Run On The Real Host

As with V3, local tests were not enough.

OSMAP runs in a real OpenBSD mail environment. The browser-facing route, mailbox helper, Dovecot-backed message access, local service users, nginx edge behavior, permissions, headers, and runtime layout all matter.

The V4 live proof was run against:

```text
mail.blackbagsecurity.com
```

The live hostile-content validator was:

```text
maint/live/osmap-live-validate-v4-hostile-content.ksh
```

The sanitized report was:

```text
maint/live/latest-host-v4-hostile-content-report.txt
```

That report records that the host build passed, the helper runtime passed, the browser runtime passed, the health check returned `HTTP/1.1 200 OK`, the hostile HTML message view returned `HTTP/1.1 200 OK`, and the executable attachment download paths returned `HTTP/1.1 200 OK`.

More importantly, it records the hostile-content properties that matter:

- sanitized HTML mode was present
- safe text survived
- allowed safe links survived
- link destination disclosure was present
- unsafe schemes were absent
- relative and protocol-relative URLs were absent
- remote-content markers were absent
- form and input payloads were absent
- iframe, SVG, MathML, object, embed, template, video, audio, source, and image payloads were absent
- autofocus and event-handler payloads were absent
- executable attachments were forced downloads
- executable attachments were downgraded to `application/octet-stream`
- `nosniff` was present
- `Cross-Origin-Resource-Policy: same-origin` was present
- private body and attachment markers were absent from the evidence
- password, TOTP material, session cookies, CSRF tokens, provider secrets, and host secrets were not included

The result marker was:

```text
result=v4_hostile_content_live_proof_passed
```

That is the kind of evidence V4 needed.

A hostile-content release should not close because the sanitizer looks reasonable in code review.

It should close because the browser route, attachment route, host runtime, and evidence path all agree.

* * *

## The Claim Matrix Matters

One of the best V4 improvements is not a mail feature.

It is the security claim matrix.

V4 now maps hostile-content claims to:

- implementation
- automated test coverage
- validation evidence
- residual risk
- documented limitation
- explicit non-goal

That is exactly the right pattern for this project.

Security claims become dangerous when they are broad, implied, or detached from evidence. A project can accidentally overstate itself simply by using comfortable language like "safe HTML" or "secure attachments."

V4 reduces that risk by forcing the claim to stay attached to the boundary.

The matrix does not let OSMAP say:

**hostile email is safe.**

It lets OSMAP say something closer to:

**these hostile-content classes are contained at these browser-mail boundary points, with these tests, this evidence, these limitations, and these residual risks.**

That is a much better claim.

It is less impressive in a marketing sense.

It is more useful in a security sense.

* * *

## Release Tuple Reconciliation Was Necessary

V4 also added a release tuple reconciliation gate.

That sounds like bookkeeping, but it matters.

Generated evidence often names the commit it assessed. If later assurance work refreshes reports, archives, or metadata, there is a risk that readers confuse current-code assurance evidence with the frozen release tuple.

V4 handles that distinction explicitly.

The frozen `v4.0.0` release evidence and later V4 hostile-assurance reports are related, but they are not the same thing. The release tuple gate makes sure those relationships remain honest.

That is the same lesson V3 taught in another form:

stale or ambiguous evidence is a bug.

For V4, the project now has a stronger mechanism to prevent a later report from being mistaken for the original release proof, or the original release proof from being mistaken for current-code assurance.

That is not flashy work.

It is important work.

* * *

## Evidence Redaction Remained Part Of The Feature

Security evidence can become a security problem.

That was true in V3, and it remains true in V4.

A hostile-content validator has to inspect message views and attachment behavior. That creates risk if the evidence path captures raw message bodies, attachment bodies, credentials, TOTP material, session cookies, CSRF tokens, provider secrets, or host secrets.

V4 treats redaction as part of the release.

The evidence is allowed to contain synthetic labels, pass markers, route status lines, host identity, commit identity, command identity, sanitized result paths, and bounded metadata.

It is not allowed to become a mailbox dump.

That matters for OSMAP because the project is meant to be reviewable. Reviewable evidence has to be safe enough to preserve, share, and inspect later.

The V4 report explicitly records that private message bodies, attachment bodies, session material, credentials, and host secrets are excluded.

That is not a side note.

That is part of the security model.

* * *

## What V4 Is Not Claiming

V4 is not claiming that OSMAP is perfect.

It is not claiming that email content is safe.

It is not claiming that a downloaded file is safe after a user opens it outside OSMAP.

It is not claiming malware prevention.

It is not claiming URL reputation.

It is not claiming rich HTML mail compatibility.

It is not claiming attachment preview safety.

It is not claiming remote-content loading.

It is not claiming JavaScript-based mail rendering.

It is not claiming Roundcube parity.

Those are deliberate non-claims.

V4 is narrower:

- hostile HTML is sanitized before browser rendering
- unsafe browser execution surfaces are stripped from message bodies
- automatic remote-content surfaces are suppressed
- preserved links are visibly disclosed
- malformed or ambiguous MIME fails closed or withholds unsafe bodies
- browser-executable attachments are forced to download
- risky attachment responses are downgraded and protected with `nosniff`
- hostile-content fixtures are covered by a release gate
- live-host proof exists for the real deployment boundary
- evidence is redacted
- residual risk is named

That is enough to close V4.

It is not enough to stop being careful.

* * *

## What V4 Adds To The Project

V4 changes OSMAP in an important way.

Before V4, OSMAP had a defensible architecture, operational gates, authenticated WSTG evidence, daily-driver workflow hardening, and MIME and HTML proof.

After V4, OSMAP has a much stronger hostile-content story.

That matters because hostile mail is not a corner case.

It is the normal threat model of mail.

Every message body is untrusted. Every attachment name is untrusted. Every MIME boundary is untrusted. Every link is untrusted. Every charset declaration is untrusted. Every remote resource reference is untrusted. Every hidden form, event handler, and browser-fetch surface is hostile until proven otherwise.

V4 gives the project a way to say:

**we know where hostile message content reaches the browser, we know what must not survive, we have fixtures for the payload classes, we have route-backed observations, we have live-host proof, and we have a claim matrix that prevents the wording from outrunning the evidence.**

That is a major improvement.

It is not a broad feature milestone.

It is a trust-boundary milestone.

* * *

## Lessons From V4

The first lesson is that hostile content containment is not one control.

It is a chain.

The parser has to behave. The sanitizer has to behave. The template has to behave. The headers have to behave. The attachment route has to behave. The browser has to receive inert content. The evidence path has to avoid leaking secrets. The documentation has to avoid overclaiming.

A failure in any part of that chain weakens the claim.

The second lesson is that the best security wording is often narrower than the engineering effort behind it.

A lot of work went into V4, but the correct claim is still modest:

OSMAP contains hostile message content inside the browser-mail boundary.

That wording is intentionally less dramatic than "safe email."

It is also much more defensible.

The third lesson is that live proof matters for browser-facing mail.

A local unit test can prove a sanitizer rule.

It cannot prove the whole deployed route.

The live validator had to observe the real message view and real attachment responses on the intended host. That made the evidence more expensive to collect, but also more meaningful.

The fourth lesson is that residual risk should be written down, not hidden.

External links remain user-driven risk.

Files opened outside OSMAP remain user-driven risk.

V4 does not erase those risks. It makes the application boundary clearer so those risks are not accidentally absorbed into a false claim.

The fifth lesson is that evidence structure is itself a control.

The hostile corpus, assurance report, archive, release tuple gate, and claim matrix are not just paperwork. They reduce the chance that future work silently weakens the V4 boundary while the project continues repeating the old claim.

* * *

## Where V5 Starts

V5 should not start by undoing V4.

That means no broad rich-mail rendering sprint, no JavaScript-heavy mailbox client, no remote-content convenience toggle, no attachment preview feature, and no plugin-style expansion unless the security boundary is redefined first.

The right starting point for V5 is whatever improves operational resilience, user confidence, and maintainability without expanding the trust boundary carelessly.

The V4 lesson should carry forward:

define the claim first, then build only what can be proven.

OSMAP does not need to become a general-purpose groupware suite to be useful.

It needs to remain a focused, reviewable, OpenBSD-native browser-mail application with claims that are smaller than its ambitions and evidence that is stronger than its wording.

* * *

## Closing Thought

The point of V4 was not to make hostile email safe.

The point was to prevent hostile email from becoming active browser behavior inside OSMAP.

That is a narrower statement.

It is also the statement that matters.

The useful question at V4 closeout was not:

Did the project add more rendering features?

The useful question was:

Can the project prove that hostile message content stays inert inside the browser-mail boundary, that risky attachments are served as downloads rather than active browser content, that remote fetch surfaces stay suppressed, and that the evidence does not leak the very secrets it was meant to protect?

For V4, the answer is yes.

That does not make OSMAP finished.

It makes the hostile-content claim reviewable.

And for browser-facing mail, reviewable is still the word that matters.

Repository: <https://github.com/unattributed/OSMAP>