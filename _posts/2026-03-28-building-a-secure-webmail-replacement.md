---
layout: post
title: "Introducing OSMAP, a Defensible OpenBSD Webmail Replacement"
date: 2026-03-28
author: unattributed
categories: [email-security, self-hosting, openbsd, zero-trust, infrastructure]
tags: [osmap, openbsd, webmail, self-hosted, zero-trust, security-architecture, email-security]
---

## Introducing OSMAP, a Defensible OpenBSD Webmail Replacement

OSMAP, the **OpenBSD Secure Mail Access Platform**, exists because the usual answer to webmail security has been to accept too much risk for too little control.

This project is not a cosmetic refresh, not another plugin-heavy groupware suite, and not an attempt to rebuild the mail stack from scratch. OSMAP is an opinionated, security-first replacement for legacy webmail in hardened OpenBSD environments. It is being built to replace the browser-facing mail experience that operators have learned to tolerate, but should no longer have to trust.

Project repository: **https://github.com/unattributed/OSMAP**  
Backend mail stack project: **https://github.com/unattributed/openbsd-mailstack**

And yes, this is a shameless announcement: **OSMAP is the project to watch if you want a smaller, more defensible, more operationally honest path to browser-based mail access on OpenBSD.**

---

## Why OSMAP Exists

Email is still the master key to digital identity. Password resets, legal notices, financial workflows, client communications, infrastructure alerts, and account recovery paths all converge there. That makes webmail one of the most valuable targets in any environment.

The problem is simple. Many self-hosted operators work hard to secure the infrastructure layer, then leave users exposed through a legacy browser interface that was designed in a different era.

That model no longer holds.

Traditional webmail often brings:

- Broad browser-facing attack surface
- Session and token risk
- Dependency and patching burden
- Feature sprawl that operators did not ask for
- Long compatibility baggage
- Weak alignment with hardened, zero-trust-style operational thinking

OSMAP exists because hardened infrastructure deserves a hardened access layer.

---

## What OSMAP Is

OSMAP is a **security-focused web mail access platform for OpenBSD systems**.

It is being built to provide a safer browser-based interface to an existing mail environment without replacing the underlying mail transport core. In practical terms, that means OSMAP is intended to sit on top of an established stack, preserve compatibility with the current mail flow, and replace the legacy webmail role with something narrower, clearer, and more defensible.

This is the point of the project:

**keep the mail stack, replace the weak link, reduce the exposure, and make the whole system easier to reason about.**

---

## The Aims And Goals Of The Project

OSMAP is deliberately focused. Its goals are not vague aspirations, they are operational targets.

### Primary Aims

- Replace Roundcube in hardened OpenBSD environments
- Provide browser-based mail access with a materially smaller attack surface
- Operate more safely in internet-exposed or semi-exposed conditions
- Preserve compatibility with existing IMAP and SMTP backends
- Enforce stronger authentication and safer session handling
- Stay maintainable for a small operator team
- Support a disciplined, reviewable software supply chain
- Make reproducible builds and controlled deployments realistic

### Security Goals

OSMAP is being built around the idea that security is not a feature bolted on at the end. It is the design constraint.

The project prioritizes:

- Minimal exposed functionality
- Least privilege operation
- Explicit trust boundaries
- Defense in depth
- Auditability and observability
- Reversible deployments
- Reduced complexity
- Long-term maintainability over novelty

### Product Goals For Version 1

Version 1 is intentionally narrow. The objective is not to out-feature legacy webmail, it is to replace the essential browser workflows safely enough that operators can retire Roundcube without losing core usability.

That first-release target includes:

- Secure login
- TOTP-based multi-factor authentication
- Bounded session handling and revocation
- Mailbox browsing
- Message reading
- Message search
- Compose, reply, and forward
- Attachment upload and download
- Required folder operations for ordinary use
- Session visibility and self-management
- Audit-relevant logging of sensitive actions
- Compatibility with the existing IMAP and SMTP submission model

In plain English, OSMAP is not trying to be everything. It is trying to be the part that matters, and to do that part well.

---

## What OSMAP Is Not

OSMAP is not a mail-server replacement.

It is not trying to replace Postfix, Dovecot, nginx, Rspamd, MariaDB, or the OpenBSD host itself. It is not a general collaboration suite. It is not a plugin marketplace. It is not a SaaS product. It is not a multi-tenant hosting platform. And it is not pretending to be Proton Mail with a different logo.

That restraint is a strength, not a limitation.

OSMAP rejects feature bloat on purpose.

Out of scope for Version 1 are:

- Calendar and groupware features
- Mobile applications
- Plugin ecosystems
- Multi-tenant public SaaS hosting
- Replacement of the core mail transport stack
- Broad enterprise identity federation
- Feature-maximal convenience platforms

The project is opinionated because secure software should be.

---

## Why This Matters

A lot of software promises security by adding more controls. OSMAP takes the more uncomfortable, and usually more effective, path of refusing unnecessary scope.

That matters because the browser-facing mail interface is often where the strongest infrastructure meets the weakest assumptions.

OSMAP is built for operators and users who understand that:

- Internet exposure changes the threat model
- VPN access alone is not a complete trust boundary
- Session theft is real
- Mail access is a high-consequence target
- Smaller systems are easier to defend, audit, and maintain

This is exactly why OSMAP is worth paying attention to. It is not chasing mass-market appeal. It is addressing a real, painful, high-value security problem with a narrower and more honest design.

---

## Who OSMAP Is For

OSMAP is aimed at environments where compromise costs more than inconvenience.

That includes:

- Security-conscious self-hosters
- Small teams with elevated security expectations
- OpenBSD operators
- Consultants and professionals handling sensitive communications
- Organizations that need browser mail access but want tighter control over risk
- Users who still want native clients like Thunderbird to remain fully supported

If the priority is fewer surprises, clearer boundaries, and better operational control, OSMAP is built for that audience.

---

## The Operating Philosophy

OSMAP is grounded in a simple belief:

**security-preserving simplicity beats convenience-driven complexity.**

The project aligns itself with well-known defensive thinking, including OWASP Top 10, CWE Top 25, MITRE ATT&CK from the defender perspective, and relevant NIST guidance. More importantly, it applies those ideas to a bounded real-world problem instead of using them as branding.

This is not security theater. It is disciplined scope control.

---

## Current Direction

OSMAP has already moved beyond a pure planning exercise. The repository documents a working Rust-based prototype and a phased program covering architecture, security model, SDLC, implementation planning, hardening, migration, and deployment discipline.

That matters because many “secure” projects never get past abstract design language. OSMAP is being shaped as an implementation-minded, operator-aware platform with an explicit OpenBSD-first posture.

That is exactly the kind of project this space needs more of.

---

## The Announcement Version

So here it is plainly:

**OSMAP is an ambitious, disciplined attempt to build the secure OpenBSD webmail replacement that legacy platforms never were.**

It is deliberately narrow. It is intentionally opinionated. It is designed for hostile environments, not ideal ones. And it is built around the idea that mail access can be made materially safer without pretending the rest of the world will suddenly become trustworthy.

If you care about self-hosted mail, OpenBSD, security architecture, least privilege, zero-trust-style access control, and reducing web-facing complexity where it actually counts, OSMAP deserves your attention.

Repository: **https://github.com/unattributed/OSMAP**

Because the future of secure webmail should not be another legacy compromise dressed up as convenience.

It should look a lot more like OSMAP.