---
layout: post
title: "OSMAP V1 Closeout, and the Hard Reality of Writing Secure Software"
date: 2026-03-28
author: unattributed
categories: [email-security, self-hosting, openbsd, zero-trust, infrastructure]
tags: [osmap, openbsd, webmail, secure-development, rust, owasp, owasp-asvs, testing]
---

## OSMAP V1 Closeout, and the Hard Reality of Writing Secure Software

When I introduced OSMAP, I described it as a defensible OpenBSD webmail replacement. That was the right ambition, but ambition is not evidence.

Version 1 has now been closed out against its current boundary, and that matters because browser-facing mail access is not a low-consequence application category. It is one of the highest-value targets in most environments. Email remains the account-recovery channel, the legal-notice channel, the client-communications channel, and the operational heartbeat of a lot of infrastructure. When webmail fails securely, people are inconvenienced. When it fails insecurely, people can lose control of identity, confidentiality, and trust very quickly.

So this follow-up is not a victory post. It is a technical closeout note, and a candid one.

OSMAP V1 passed its current closeout gate on April 14, 2026, including a fresh host-side rerun against the hardened snapshot, with the resulting evidence archived in the repository. That does **not** mean the project is finished in some absolute sense. It means something more disciplined and more useful:

**the Version 1 boundary is now narrow enough, implemented enough, reviewed enough, and tested enough that I am willing to say what it is, what it is not, what risks were reduced, and what work is still intentionally deferred.**

That distinction matters.

* * *

## What V1 Closeout Actually Means

A lot of projects use the language of security closeout when what they really mean is that the code compiles, the interface works, and nobody has reported a disaster yet.

That is not good enough here.

For OSMAP, V1 closeout means the current release boundary has been held against its actual requirements:

- secure login
- TOTP-based multi-factor authentication
- bounded session handling and self-revocation
- mailbox browsing and message viewing
- compose, reply, and forward
- attachment upload and download
- required folder operations for ordinary use
- compatibility with the existing OpenBSD mail substrate
- audit-relevant logging of sensitive actions
- hardening and review of the most important trust boundaries

It also means the release-facing documentation, the host-side validation evidence, and the current repository state were brought back into alignment.

That might sound administrative. It is not. It is part of the security posture.

A secure project is not just secure code. It is secure code, accurate operational assumptions, current validation evidence, explicit residual risk, and documentation that does not lie about any of those things.

* * *

## The Hard Part Was Never Just “Avoid the OWASP Top 10”

OWASP Top 10, OWASP ASVS, and CWE are valuable. They should be used. They help force a shared language around common failure classes. They absolutely matter.

But they are not enough to produce a secure application in a high-consequence category.

The hardest mistakes in OSMAP were not, “did someone forget that injection exists?” They were questions like these:

- Where does authority actually come from at a trust boundary?
- Which process is trusted to speak for a user, and why?
- What happens when a deployment assumption becomes false?
- Does the implementation leak meaning through error semantics even when the HTTP status code looks fine?
- Are secret files merely present, or are they being loaded safely?
- Does a state store remain safe when two valid operations happen at once?
- Is same-origin behavior being enforced because it is designed, or only because nobody has tripped over the missing check yet?

These are the kinds of problems that survive superficial security language.

They are also exactly the kinds of problems that matter when the software is meant for people who are not chasing convenience, but trying to reduce real operational risk.

* * *

## Secure Software Is Mostly About Refusing to Lie

One lesson from OSMAP V1 is that secure software development is, at its core, a refusal to lie.

Do not lie about scope.

Do not lie about what a component is trusted to do.

Do not lie about what a deployment invariant must be.

Do not lie about whether a boundary is enforced in code or merely hoped for in documentation.

Do not lie about whether a feature belongs in the first release.

And do not lie to yourself by assuming that a good language, a clean architecture diagram, or a disciplined threat model has made the application safe by itself.

Rust helps. OpenBSD helps. Narrow scope helps. None of them eliminate the need to reason correctly.

In a project like this, security comes less from heroics than from repeated acts of restraint.

That means saying no to feature sprawl.

It means narrowing exposed functionality.

It means turning assumptions into invariants.

It means treating deployment as part of the trusted computing base instead of pretending the application floats above the host.

And it means accepting that a secure application is not one with no bugs, but one whose important failures are anticipated, bounded, and hard to silently reintroduce.

* * *

## What Nearly Went Wrong, and Why It Matters

Several of the most important V1 security corrections were not classic “headline vulnerabilities.” They were the sorts of mistakes that good teams still make when building real systems.

### 1. Trusting the wrong thing at the mailbox-helper boundary

One of the biggest V1 lessons was that a boundary is only as good as the authority it accepts.

In OSMAP’s mailbox-helper model, the browser-facing web runtime is intentionally separated from mailbox-reading operations. That is good architecture. But at one point, the helper boundary still accepted a caller-supplied mailbox identity in a way that made the trust model too loose.

The V1-safe correction was not to pretend this was fine. It was to narrow and enforce the actual boundary.

The helper now authenticates its trusted local caller, and startup now fails closed unless the derived trusted caller identity matches the explicitly configured dedicated OSMAP web-runtime UID. That is a much stronger and more honest V1 design.

Is it the strongest possible design? No.

The stronger long-term model is for the helper to derive mailbox identity from trusted server-side state rather than accepting caller-claimed authority input across the protocol at all.

That redesign is intentionally deferred to post-V1 architecture work.

This is the important point: secure development is not pretending every unresolved architectural improvement is release-blocking. It is making sure the current boundary is explicit, enforced, reviewable, and documented, and then recording what remains.

### 2. Authentication can leak meaning without leaking data

Another V1 correction was the login flow.

The problem was not that authentication was absent. The problem was that browser-visible failure semantics could reveal whether a password was correct before second-factor validation failed.

That is the kind of mistake many teams miss because everything still looks “secure enough” in a quick review. The endpoint returns `401`, the code is rate-limited, and MFA exists. But the sequence still leaks information.

Fixing that meant making failure semantics boring on purpose.

Secure login flows should not help an attacker sort invalid-password cases from valid-password-wrong-TOTP cases. That kind of semantic narrowing is not glamorous, but it is real security work.

### 3. Safe file access is not the same thing as reading the right file

TOTP secret handling was another good reminder that filesystem interactions need to be treated as part of application security, not just host hygiene.

A code path that reads a file successfully is not automatically a secure code path.

Questions that matter include:

- Is the path allowed to follow symlinks?
- Is the file owned by the expected principal?
- Are the mode bits tight enough?
- Is the file actually a regular file?

Those checks were tightened for V1. That was the right move because security-sensitive file reads should not quietly inherit trust from deployment habits alone.

### 4. Concurrency bugs can cross security boundaries

One of the more humbling examples was a settings persistence issue caused by a shared temporary filename.

That kind of bug does not sound dramatic, but it matters because concurrency mistakes can become isolation mistakes. If two users can interfere with one another’s persisted state because an internal write path assumes serial behavior, that is no longer “just a bug.” It is a boundary problem.

That too had to be fixed with explicit, testable behavior rather than good intentions.

### 5. “Defense in depth” only counts if it is actually there

Same-origin enforcement is a good example of where modern browser defaults and token-based CSRF protection can already be doing useful work, but where a defensible system still benefits from explicit checks.

This is where security engineering often becomes sloppy. Teams say “the browser probably helps us here” and move on.

OSMAP V1 needed the harder answer:

if same-origin behavior matters to the trust model, make it explicit.

Do not treat implied protection as equivalent to enforced policy.

* * *

## The Real Challenge Was Converting Design Into Evidence

If there is one sentence that best describes what makes writing secure applications difficult, it is this:

**secure design is only the beginning, not the conclusion.**

Most of the hard work is in converting design into evidence.

That means asking, for every important claim:

- Where is it enforced?
- How would we know if it stopped being true?
- Is there a test for it?
- Is there a host-side validation step for it?
- Would a future refactor silently weaken it?
- Would the docs still tell the truth if the code changed?

In OSMAP, that has led to a pattern I now consider essential:

**turn trust assumptions into executable invariants whenever possible.**

If a helper must only trust one specific local runtime identity, encode that.

If a secret file must have safe ownership and mode, check that.

If authenticated mutation routes must enforce same-origin expectations, verify that.

If login responses must not leak first-factor correctness, test that exact behavior.

The more security assumptions live only in a human head or a markdown document, the more likely they are to decay.

* * *

## What Automated Security Testing Needs to Look Like

This is where I want to be very clear.

A secure Rust application does not become secure merely because it has unit tests and uses a memory-safe language.

Rust removes entire categories of memory corruption risk. That is important. It does not remove logic errors, protocol mistakes, authority mistakes, parser mistakes, or deployment-model mistakes.

OSMAP’s existing automated testing posture is already much better than a casual prototype:

- repository-owned security checks
- custom policy gates for reviewed boundaries
- targeted regression tests for sensitive code paths
- signed, reviewable closeout commits
- live host validation against the actual OpenBSD deployment model

That is a good base.

But for a project like this, mature security testing has to go further.

### Parser fuzzing must become first-class

OSMAP consumes attacker-controlled input constantly:

- HTTP requests
- form data
- MIME structures
- headers
- attachment metadata
- mailbox protocol material
- rendered message content

That means fuzzing is not optional in the long term.

The goal is not simply to avoid crashes. The goal is to discover cases where malformed input violates assumptions, triggers degenerate behavior, or produces output that should not exist.

The obvious first fuzz targets are:

- HTTP request parsing
- form parsing
- MIME parsing
- mailbox helper protocol parsing
- message header decoding
- attachment metadata handling
- HTML mail sanitation boundaries

### Property and state-machine testing matter more than people think

A lot of security bugs are sequence bugs.

Not “input X causes output Y,” but “sequence A, then B, then C, under condition D, leaves the system in a state nobody intended.”

That is why property-based and state-machine testing are so valuable for a project like OSMAP.

High-value targets include:

- session issuance, revocation, expiration, and logout
- throttle bucket behavior under repeated and mixed failures
- settings persistence isolation between users
- helper authorization invariants
- authentication failure normalization
- mailbox and folder operation sequencing
- compose and send workflows under partial failure

These tests do something ordinary example-based tests often do not: they search the space between the obvious cases.

### Supply-chain policy needs to be treated as part of application security

Secure software is not only about your code. It is about the code you accept into the build, the workflows you trust to validate it, and the conditions under which change is allowed.

For OSMAP, that means the automated security posture should continue to grow around:

- scheduled CodeQL analysis
- dependency review on pull requests
- Rust advisory and license policy checks
- review of transitive dependency drift
- stronger release gating around security-relevant changes

This is not bureaucracy. It is how a security-sensitive project avoids becoming secure only in its own imagination.

### Host-side validation has to remain part of the story

One of the strengths of OSMAP V1 is that security closeout was not treated as purely local or purely synthetic. Host-side validation on the actual OpenBSD deployment model matters.

That should continue.

The application, the runtime model, the helper boundary, the confinement expectations, and the supporting mail substrate all interact. A project like this needs live proof, not just local test success.

Longer term, a hermetic or virtualized OpenBSD validation path should complement that work so the system can be reproduced more easily without depending on one long-lived environment alone.

* * *

## What V1 Is Not Claiming

It is important to say this plainly.

OSMAP V1 is **not** claiming that the secure webmail problem is solved forever.

It is not claiming that no design improvement remains.

It is not claiming that there is no future attack surface to reduce.

And it is not claiming that standards checklists alone prove security.

What it **is** claiming is narrower, and more credible:

- the Version 1 product boundary was intentionally constrained
- the current critical trust boundaries were reviewed and tightened
- important mistakes were corrected before release closeout
- the release-facing documentation now reflects the hardened snapshot
- host-side closeout evidence exists and is archived
- residual risks that remain have been named instead of hidden

That is the kind of claim I am willing to make.

* * *

## Why This Work Matters

There are people and organizations who need browser-based access to mail, but who are deeply uncomfortable with the security and operational assumptions baked into legacy webmail.

That discomfort is not paranoia. In many cases it is experience.

Some of the people who most need a secure browser-access layer are exactly the people who understand how bad compromise can get:

- small operators with high-consequence systems
- consultants and investigators
- privacy-focused professionals
- self-hosters who do not want the browser tier to be the weakest link
- organizations handling sensitive communications without a large internal engineering bench

Those users do not need marketing theater.

They need software that is narrow enough to defend, honest enough to describe its boundaries, and disciplined enough to say “not in V1” when necessary.

That is the standard OSMAP has tried to meet.

* * *

## Where OSMAP Goes After V1

The next security improvements should continue the same discipline that made V1 credible.

That means focusing on the work that increases assurance instead of broadening scope for its own sake.

The post-V1 security direction should include at least:

- helper-derived mailbox identity rather than caller-supplied identity across the helper protocol
- stronger fuzzing coverage for parser-heavy and mail-facing inputs
- deeper property and state-machine testing for session, auth, and mailbox workflows
- continued hardening of deployment invariants
- tighter supply-chain and dependency policy enforcement
- reproducible validation paths that complement live-host closeout testing

What should **not** happen is a slide back into convenience-driven sprawl.

If OSMAP becomes a feature-chasing suite, it will become easier to market and harder to defend.

That trade is not worth making.

* * *

## Final Thoughts

Version 1 closeout is an important milestone for OSMAP, but the real significance is not that the project can now claim “done.”

The real significance is that the project now has a firmer answer to the question that matters most:

**what does it take to write a secure application for people who genuinely need one?**

The answer is not novelty.

It is not branding.

It is not a checklist pasted into a README.

It is narrow scope, explicit trust boundaries, evidence-backed hardening, testable invariants, honest residual-risk statements, and the discipline to hold a line when the easier path would be to add more features and call that progress.

OSMAP V1 is closed out on that basis.

That does not make it sacred. It makes it reviewable.

And for software in this category, being reviewable, constrained, and operationally honest is much closer to real security than pretending perfection was ever on offer.

Repository: https://github.com/unattributed/OSMAP

Because the people who need a secure webmail replacement do not need more promises.

They need software that has done the hard work of becoming difficult to trust for the wrong reasons, and easier to trust for the right ones.