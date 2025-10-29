---
layout: post
title: "Primer: Razor2 + SpamAssassin on OpenBSD (with Amavis) — defensible mail pipeline"
date: 2025-10-29
author: unattributed
categories: [openbsd, email]
tags: [razor2, spamassassin, amavis, postfix, openbsd, pf]
---

# Razor2 + SpamAssassin on OpenBSD (with Amavis): A Practical, Defensible Setup for self hosted Mail filtering

## TL;DR

If you run an OpenBSD mail stack (Postfix → Amavis → SpamAssassin → Dovecot), enabling **Vipul’s Razor (Razor2)** adds a fast, low-false-positive, collaborative signal that complements DNSBL/DMARC/Bayes. Run Razor as the Amavis account (`_vscan`), allow outbound TCP **2703** in PF (optionally constrained to the amavis UID), point SpamAssassin’s Razor2 plugin at `/var/amavis/.razor/razor-agent.conf`, and verify with GTUBE + Razor agent logs. References and primary docs are linked throughout. ([wiki.debian.org][1])

---

## Why Razor2 still matters (and where it fits)

Razor2 is a **distributed checksum reputation system**: clients hash message content and consult community consensus maintained by the Razor network (now operated by Cloudmark). This provides a near-real-time signal that’s orthogonal to DNSBLs and cryptographic authentication (SPF/DKIM/DMARC) and complements statistical filters (Bayes). In practice, it catches campaign spam quickly with little tuning. ([forum.centos-webpanel.com][2])

Academic surveys of anti-spam approaches have long contrasted collaborative checksum systems like **Razor** and **DCC** with content classifiers; they consistently find **ensemble strategies** (multiple independent signals) reduce both false positives and false negatives—precisely what we target here. For background on the **DCC** model and collaborative detection, see Schryver’s overview and later evaluations. ([Linux Documentation][3])

---

## Target architecture

OpenBSD stack:

```
[Internet] → Postfix (25/587) → Amavis (10024/10025) → SpamAssassin (+Razor2) → Dovecot
                                       ↘ ClamAV
```

Amavis embeds SpamAssassin’s libraries; Razor runs client-side under the same unprivileged account you run Amavis with (on OpenBSD packages: `_vscan`, UID 530). ([amavis.org][4])

---

## Implementation steps (OpenBSD)

### 1) Create the Razor home and seed config (as `_vscan`)

```sh
doas install -d -o _vscan -g _vscan -m 0750 /var/amavis/.razor

# initialize & discover (verbosity -d is optional but helpful first run)
doas -u _vscan razor-admin -home=/var/amavis/.razor -create
doas -u _vscan razor-admin -home=/var/amavis/.razor -discover

# optional in 2025, but supported: create a local identity
doas -u _vscan razor-admin -home=/var/amavis/.razor -register
```

You should see `identity` (symlink → `identity-*`), `razor-agent.conf`, `servers.*.lst`, and per-server `.conf` files under `/var/amavis/.razor`. Razor uses outbound TCP **2703** to Cloudmark endpoints (e.g., `c30[1-3].cloudmark.com`, `n00[1-4].cloudmark.com`). ([wiki.debian.org][1])

> Note: `razor-admin` has no `-ping` option—errors like “Unknown option: ping” simply reflect the tool’s actual interface. Use `-discover` and `razor-check` instead. ([Wikipedia][5])

---

### 2) Allow outbound egress to Razor from the amavis user only (PF)

A tight PF rule keeps egress minimal and auditable:

```pf
# (fragment) — /etc/pf.conf
# NAT and general egress as you already use ...
# Add explicit egress for Razor client, constrained to amavis UID (530):
pass out on egress proto tcp from (egress) to any port 2703 user 530 flags S/SA
```

Reload and confirm:

```sh
pfctl -nf /etc/pf.conf && pfctl -f /etc/pf.conf
pfctl -sr | grep 2703
```

See `pfctl(8)` and `pf.conf(5)` for rule semantics and the `user` constraint. ([amavis.org][6])

---

### 3) Enable the Razor2 plugin in SpamAssassin

Ensure the plugin is loaded (usually via the packaged `v310.pre`) and explicitly configure in `local.cf`:

```
# /etc/mail/spamassassin/local.cf
loadplugin Mail::SpamAssassin::Plugin::Razor2
use_razor2 1
razor_config /var/amavis/.razor/razor-agent.conf
```

Keep one `use_razor2` stanza (duplicate lines won’t help). After changes:

```sh
spamassassin --lint   # should be clean
doas rcctl restart amavisd
```

Rationale and plugin semantics are documented in the SpamAssassin distribution and Razor agent manpages. ([wiki.debian.org][1])

---

### 4) Functional tests (no guessing—verify signals)

**A. Agent pathing / network**
Send a small RFC822 message to `razor-check` as `_vscan`:

```sh
printf 'From:a@b\nTo:c@d\nSubject:test\n\nbody\n' \
| doas -u _vscan razor-check -home=/var/amavis/.razor -d
```

Look for connections to `c30x.cloudmark.com` and updates to `server.c30x.cloudmark.com.conf` and `servers.*.lst` in `/var/amavis/.razor`. ([Wikipedia][5])

**B. Pipeline sanity (SpamAssassin/Amavis)**
Inject a **GTUBE** message to confirm SA is executing in the Amavis path:

```sh
cat <<'MSG' | /usr/sbin/sendmail you@yourdomain
From: test@local
To: you@yourdomain
Subject: GTUBE test

XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X
MSG
```

In `/var/log/maillog` you should see `GTUBE=1000` (or similar) in SA test summaries via Amavis. **GTUBE** is the canonical SA test string—seeing it fire proves your SA/Amavis integration is live. (GTUBE itself won’t trigger a Razor query; it’s synthetic.) ([Wikipedia][7])

**C. Observe Razor actually firing**
Once real mail flows, look for `RAZOR2_CHECK`, `RAZOR2_CF`, or similar rules in Amavis/SA logs. (Exact rule names can vary by ruleset version.) You can also tail the agent log:

```sh
tail -f /var/amavis/.razor/razor-agent.log
```

---

## Operational hardening & gotchas

* **Run as `_vscan` only.** Don’t create `~root/.razor`; keep all identities/config under `/var/amavis/.razor` with `_vscan:_vscan` and `0750`. This avoids permission issues when SA is invoked from Amavis. ([wiki.debian.org][1])

* **Egress least-privilege.** The PF `user 530` limiter drastically narrows exposure if a local process goes rogue. It’s a simple, effective control that pairs well with OpenBSD’s default `syscalls+pledge/unveil` posture. ([amavis.org][6])

* **Don’t chase ‘-ping’.** The Razor client interface doesn’t include `-ping`; use `-discover` and observe server state SRL updates in the agent log to validate reachability. ([Wikipedia][5])

* **Use ensembles, not magic bullets.** Razor’s collaborative checksum reputation is best combined with SPF/DKIM/DMARC, DNSBLs, and Bayes. That mixture is what literature frequently finds most robust in production. ([Linux Documentation][3])

---

## Example: minimally complete config snapshot

```text
# Ownership/paths
/var/amavis/.razor (0750, _vscan:_vscan)
  ├── identity -> identity-XXXXXXXX
  ├── razor-agent.conf
  ├── servers.discovery.lst
  ├── servers.catalogue.lst
  ├── servers.nomination.lst
  └── server.c303.cloudmark.com.conf (and peers)

# PF egress (fragment)
/etc/pf.conf:
  pass out on egress proto tcp from (egress) to any port 2703 user 530 flags S/SA

# SpamAssassin
/etc/mail/spamassassin/local.cf:
  loadplugin Mail::SpamAssassin::Plugin::Razor2
  use_razor2 1
  razor_config /var/amavis/.razor/razor-agent.conf
```

---

## Troubleshooting checklist

* **`razor-check` fails to connect:** confirm PF egress rule and upstream firewall/NAT; verify DNS to `*.cloudmark.com`. ([Wikipedia][5])
* **Amavis path ok but no Razor hits:** use real spam samples; GTUBE won’t trigger Razor. Check that `servers.*.lst` exist and are fresh; re-run `-discover`. ([Wikipedia][7])
* **`spamassassin --lint` complains:** duplicate or malformed `use_razor2`/`razor_config` lines—reduce to a single clean block and restart Amavis.
* **Permissions errors:** everything under `/var/amavis/.razor` must be `_vscan:_vscan`, `0750` dir, `0644/0600` files. ([wiki.debian.org][1])

---

## References & further reading (primary/authoritative)

* **Razor agent & configuration manpages** (options, files, network behavior). ([wiki.debian.org][1])
* **SpamAssassin GTUBE test** (official). ([Wikipedia][7])
* **Amavis architecture & SA integration** (official docs).
* **OpenBSD pfctl/pf.conf** (policy syntax; `user` match). ([amavis.org][6])
* **Collaborative spam detection & ensemble efficacy** (research/position): DCC overview; subsequent evaluations comparing collaborative systems (Razor/DCC) with classifiers. ([Linux Documentation][3])

---

## Closing note

In 2025, the most durable mail defenses are **layered**: cryptographic identity (SPF/DKIM/DMARC), **reputation** (DNSBL, Razor/DCC), and **content** (Bayes + rules). OpenBSD gives you the right primitives (PF, privilege separation), while Amavis/SpamAssassin make composition practical. Razor2 adds a low-cost, high-signal layer that’s easy to audit and—when you pin egress to user 530 over port 2703—securely bounded by design.

[1]: https://wiki.debian.org/DebianSpamAssassin?utm_source=chatgpt.com "DebianSpamAssassin"
[2]: https://forum.centos-webpanel.com/e-mail/install-razor2-for-postfixdovecot-spam-filtering-along-with-spamassassin/?utm_source=chatgpt.com "Install Razor2 for Postfix/Dovecot Spam Filtering along with ..."
[3]: https://linux.die.net/man/5/razor-agents?utm_source=chatgpt.com "razor-agents(5) - Linux man page"
[4]: https://www.amavis.org/?utm_source=chatgpt.com "amavisd-new"
[5]: https://en.wikipedia.org/wiki/GTUBE?utm_source=chatgpt.com "GTUBE"
[6]: https://amavis.org/amavisd-new-docs.html?utm_source=chatgpt.com "amavisd-new documentation bits and pieces"
[7]: https://de.wikipedia.org/wiki/GTUBE?utm_source=chatgpt.com "GTUBE"
