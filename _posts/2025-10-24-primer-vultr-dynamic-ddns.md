---
layout: post
title: "Primer: multi-domain dynamic DNS on Vultr (no ddclient) — hardened & audited"
date: 2025-10-24
author: unattributed
categories: [openbsd, ddns]
tags: [vultr, dyn-dns, openbsd, isp, python, security]
---

# Solving dynamic DNS on Vultr for multiple domains 

I run several domains on Vultr’s DNS from a single OpenBSD host and need A/AAAA records to track my WAN IP. `ddclient` doesn’t support Vultr’s DNS API, and most DIY snippets only touch one zone. This post is the **hardened** version of my updater: **safe WAN IP detection**, **strict file perms**, **stable logging with rotation**, **cron wiring that actually works**, plus **built‑in tests** so you can prove it’s doing the right thing.

Targets: OpenBSD, Vultr DNS v2 API, repeated labels across zones (e.g., `@`, `mail`, `obsd1`), GitHub Pages apex protection. IPv4-only by default; IPv6 supported with a flag.

---

## Why not ddclient?

- Vultr’s managed DNS isn’t supported by ddclient.
- I need multiple zones with identical labels, reproducible paths & perms, logging in `/var/log/`, and a **GitHub Pages apex guard**.

---

## Prereqs

```sh
# OpenBSD
doas pkg_add python%3 py3-requests
# (or ensure python3 + requests are available)
```

---

## Configuration

Two shell‑style `.env` files live under `~/.config/vultr/` for the user who runs the job (below I show **foo**). Quotes are OK.

### `~/.config/vultr/api.env`

```sh
# ~/.config/vultr/api.env
# Required
VULTR_API_KEY="REDACTED_YOUR_VULTR_BEARER_TOKEN"
VULTR_API_URL="https://api.vultr.com/v2"

# Email summary (optional; via /usr/sbin/sendmail)
MAIL_NOTIFY="ops@example.io"
MAIL_FROM="ops@example.io"

# Optional: skip apex '@' for these domains (e.g., GitHub Pages)
GITHUB_PAGES_DOMAINS="unattributed.blog"

# Optional: only accept IPv4 from these CIDRs (space- or comma-separated).
# Leave empty to accept any public IPv4.
ALLOWED_IPV4_CIDRS="124.121.0.0/16"

# Default TTL (seconds)
DEFAULT_TTL="300"

# Optional explicit pointers (handy if cron runs as root)
VULTR_API_ENV=/home/foo/.config/vultr/api.env
VULTR_DDNS_ENV=/home/foo/.config/vultr/ddns.env
```

### `~/.config/vultr/ddns.env`

```sh
# Zones to update (space-separated)
VULTR_DOMAINS="example1.com example2.com example3.ca example4.energy example5.com unattributed.blog example6.com"

# Host labels per domain (space or comma separated). Use "@" for apex.
VULTR_HOSTS_example1.com="@ mail obsd1"
VULTR_HOSTS_example2.com="@ mail obsd1"
VULTR_HOSTS_example3.ca="@ mail obsd1"
VULTR_HOSTS_example4.energy="@ mail obsd1"
VULTR_HOSTS_example5.com="@ mail obsd1"
VULTR_HOSTS_unattributed.blog="mail obsd1"   # no apex; GH Pages guard also protects
VULTR_HOSTS_example6.com="@ mail obsd1"

# TTLs (optional). Underscore or dot forms both work.
VULTR_TTL_DEFAULT=300
#VULTR_TTL_blackbagsecurity_com=180
```

**Permissions: lock them down.**

```sh
chmod 700 ~/.config/vultr
chmod 600 ~/.config/vultr/*.env
```
If you run from **root’s cron**, you can move these to `/etc/vultr/` (`root:wheel`, `600`) or keep them under `/home/foo` but make them **root‑owned**.

---

## The updater

Installed as `/usr/local/sbin/vultr_ddns_multi.py`. Highlights:

- Default: **IPv4 (A)** only; add `--ipv6-only` for AAAA.
- **Consensus IP** across multiple echo services; **public‑only**.
- **Create or update** each requested label in each domain; per‑domain **TTL**.
- **Apex guard**: skips `@` for domains listed in `GITHUB_PAGES_DOMAINS`.
- **Cache** in `~/.cache/vultr-ddns/` to skip no‑op runs.
- **Logs** to `/var/log/vultr_ddns.log`; fallback to `~/.cache/vultr-ddns/vultr_ddns.log` (forced `0600`).
- **Email summary** when `MAIL_FROM` + `MAIL_NOTIFY` are valid.
- **API pinning** to `api.vultr.com` unless `--allow-non-vultr-api` is set.
- **Diagnostics:** `--self-test`, `--diagnose-ipv4`, `--diagnose-ipv6`.

Install & smoke test:

```sh
doas install -o root -g wheel -m 0755 vultr_ddns_multi.py /usr/local/sbin/vultr_ddns_multi.py

# Built-in unit checks (consensus/email/API pin)
/usr/local/sbin/vultr_ddns_multi.py --self-test  # expect: SELF-TEST: OK

# See echo-site votes and consensus (no DNS writes)
/usr/local/sbin/vultr_ddns_multi.py --diagnose-ipv4
```

Dry run (no writes), then real run:

```sh
/usr/local/sbin/vultr_ddns_multi.py --force -n -v
/usr/local/sbin/vultr_ddns_multi.py -q
```

---

## Logging & rotation

The script appends to `/var/log/vultr_ddns.log`. On OpenBSD, rotate daily and keep 7 gzips:

```
# /etc/newsyslog.conf
# logfile                    owner:group  mode  count  size  when   flags
/var/log/vultr_ddns.log      root:wheel   640   7      *     @T00   Z
```

If you run as a non‑root user and can’t write `/var/log`, the script falls back to `~/.cache/vultr-ddns/vultr_ddns.log` with perms **0600**.

---

## Cron that works (PATH / shebang)

On OpenBSD, `python3` is in **/usr/local/bin**. If your script uses `#!/usr/bin/env python3`, make sure cron’s PATH includes `/usr/local/bin`.

**Option A (edit root’s crontab PATH):**
```cron
PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin
*/5 * * * * /usr/local/sbin/vultr_ddns_multi.py -q
```

**Option B (pin the shebang to absolute Python):**
```sh
doas sed -i.bak '1s|/usr/bin/env python3|/usr/local/bin/python3|' /usr/local/sbin/vultr_ddns_multi.py
```

Simulate cron’s environment once (sanity check):

```sh
doas env -i SHELL=/bin/sh PATH=/usr/local/bin:/bin:/sbin:/usr/bin:/usr/sbin HOME=/var/log   /usr/local/sbin/vultr_ddns_multi.py -q
```

Restart cron only if you want to be sure:
```sh
doas rcctl restart cron
doas rcctl status cron
```

---

## Verification (auth NS, not cache)

Query Vultr’s authoritative nameserver directly:

```sh
for d in example1.com example2.com example3.ca example4.energy example5.com unattributed.blog example6.com; do
  echo "=== $d"
  drill -t -Q @ns1.vultr.com A $d           2>/dev/null || true
  drill -t -Q @ns1.vultr.com A mail.$d      2>/dev/null || true
  drill -t -Q @ns1.vultr.com A obsd1.$d     2>/dev/null || true
done
```

---

## Built‑in tests & operations

- **Self‑test** (offline logic: consensus, email regex, API pin):
  ```sh
  /usr/local/sbin/vultr_ddns_multi.py --self-test  # expect OK
  ```

- **Diagnose IP** (show raw votes + the chosen IP):
  ```sh
  vultr_ddns_multi.py --diagnose-ipv4
  # vultr_ddns_multi.py --diagnose-ipv6
  ```

- **Status / cache control**:
  ```sh
  vultr_ddns_multi.py --status
  vultr_ddns_multi.py --touch -v              # refresh cache only (no API)
  vultr_ddns_multi.py --clear-cache
  ```

- **Safety rails**:
  - `--allow-non-vultr-api` (only if you truly need to override API URL pinning)
  - `--no-gh-guard` (temporarily allow apex updates on a GH Pages domain)
  - `--ipv6-only` (operate on AAAA records only)

---

## Threat model & mitigations (concise)

- **Stolen API key → DNS takeover**  
  *Mitigate:* env files `600`, owner‑only; (optionally) move to `/etc/vultr/` root‑owned.

- **Tampered IP‑echo → site hijack**  
  *Mitigate:* consensus across multiple services; only accept **public** IPs; optional CIDR allowlist.

- **Config tampering (when run as root)**  
  *Mitigate:* store configs root‑owned or run from the owning user’s cron.

- **API URL exfiltration**  
  *Mitigate:* pin to `api.vultr.com` by default; require `--allow-non-vultr-api` to override.

- **Email header/newline shenanigans**  
  *Mitigate:* validate addresses before calling `sendmail`.

- **Log snooping**  
  *Mitigate:* fallback log forced to `0600`; `/var/log/vultr_ddns.log` is `640` root:wheel; rotate with `newsyslog`.

---

## Flags cheat sheet

- `-n, --dry-run` — print intended actions, no API writes  
- `-q, --quiet` / `-v, --verbose` — console verbosity  
- `-d, --domain DOMAIN` — restrict to one or more zones  
- `--ipv6-only` — AAAA only  
- `--force` — ignore IP cache; always check/update  
- `--status` — show cached IPs  
- `--clear-cache` — delete cache files  
- `--touch` — refresh caches from current public IP(s), no API calls  
- `--diagnose-ipv4`, `--diagnose-ipv6` — show echo votes + consensus  
- `--self-test` — offline unit checks (consensus/email/API pin)  
- `--no-gh-guard` — allow apex updates for GH Pages‑listed domains  
- `--allow-non-vultr-api` — opt‑out of API URL pinning (not recommended)

---

**Attribution:** Andy J Smith’s `ddns.py` informed this work: <https://github.com/andyjsmith/Vultr-Dynamic-DNS>.
