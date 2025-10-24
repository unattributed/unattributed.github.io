---
layout: post
title: "Primer: multi-domain dynamic DNS on Vultr (no ddclient)"
date: 2025-10-24
author: unattributed
categories: [openbsd, ddns]
tags: [vultr, dyn-dns, openbsd, isp, python]
---

# Solving dynamic DNS on Vultr for multiple domains (OpenBSD, reproducible)

I run several domains on Vultr's DNS from a single OpenBSD host and need A/AAAA records to track my WAN IP. `ddclient` doesn't support Vultr's DNS API, and the one-off scripts I found were single-domain only. This post documents a production-ready, multi-domain updater with exact file paths, permissions, logging + rotation, cron wiring, and verification.

It targets OpenBSD, Vultr DNS v2 API, repeated host labels across domains (for example `@`, `mail`, `obsd1`), and safely **skips GitHub Pages apex** records when requested. IPv4-only by default; IPv6 supported in a separate mode.

## tl;dr

A small Python 3 program calls Vultr's v2 DNS API. It reads two `.env` files (credentials/settings; domain/hosts), supports **multiple domains**, **per-domain TTLs**, a **cache** to skip no-op runs, a **GitHub Pages apex guard**, **/var/log** logging with `newsyslog` rotation, and simple flags:

- default: IPv4 A-records only
- `--ipv6-only`: AAAA only
- `--force`: ignore cache
- `--status`, `--clear-cache`, `--touch`: inspect or manage cache
- `-v` / `-q`: verbosity

---

## Why not ddclient?

- Vultr's managed DNS isn't supported by ddclient.
- Most DIY scripts update a single record or a single zone.
- I needed: *N* domains, the same labels in each zone, reproducible file paths, robust logging, and a guard for GitHub Pages apex.

---

## Install prerequisites

```sh
# OpenBSD
doas pkg_add python%3 py3-requests
# (or ensure python3 + requests are available)
```

---

## Configuration files

Two `.env` files live under `~/.config/vultr/` for whichever account is running the job (below I show **foo**). These are simple `KEY=VALUE` shell-style files (quotes OK).

### `~/.config/vultr/api.env`

```sh
# ~/.config/vultr/api.env
# Required
VULTR_API_KEY="REDACTED_YOUR_VULTR_BEARER_TOKEN"
VULTR_API_URL="https://api.vultr.com/v2"

# Optional mail summary (via /usr/sbin/sendmail)
MAIL_NOTIFY="blah@unattributed.blog"
MAIL_FROM="blah@unattributed.blog"

# Optional: skip apex '@' for these (e.g., GitHub Pages)
GITHUB_PAGES_DOMAINS="unattributed.blog"

# Default TTL (seconds)
DEFAULT_TTL="300"

# (Optional explicit pointers; helpful if this script runs as root)
VULTR_API_ENV=/home/foo/.config/vultr/api.env
VULTR_DDNS_ENV=/home/foo/.config/vultr/ddns.env
```

### `~/.config/vultr/ddns.env`

```sh
# Which zones to update (space-separated)
VULTR_DOMAINS="example1.com example2.io example3.ca example4.energy example5.com unattributed.blog example6.com"

# Host labels per domain (space or comma separated). Use "@" for apex.
VULTR_HOSTS_example1.com="@ mail obsd1"
VULTR_HOSTS_example2.io="@ mail obsd1"
VULTR_HOSTS_example3.ca="@ mail obsd1"
VULTR_HOSTS_example4.energy="@ mail obsd1"
VULTR_HOSTS_example5.com="@ mail obsd1"
VULTR_HOSTS_unattributed.blog="mail obsd1"   # no apex here; GH Pages guard also protects
VULTR_HOSTS_example6.com="@ mail obsd1"

# TTLs (optional). You can also use underscore-style keys; both are accepted.
VULTR_TTL_DEFAULT=300
#VULTR_TTL_example_com=180
```

> **Note:** Keys may use dots or underscores (both work). The script normalizes either style.

---

## The updater script

Save the script as `/usr/local/sbin/vultr_ddns_multi.py` and make it executable. (I keep the canonical copy in git, but this post assumes you've placed it on the host.) Features:

- IPv4-only by default; `--ipv6-only` mode for AAAA
- Match-and-update (or create) records for each label in each domain
- Per-domain TTLs
- Tiny cache in `~/.cache/vultr-ddns/` to skip no-op runs
- GitHub Pages apex guard: skips `@` for domains listed in `GITHUB_PAGES_DOMAINS`
- Logging to `/var/log/vultr_ddns.log` with fallback to `~/.cache/vultr-ddns/vultr_ddns.log`
- Mail summary when `MAIL_FROM` and `MAIL_NOTIFY` are set
- Root/cron friendly: will honor `VULTR_API_ENV` / `VULTR_DDNS_ENV` if set **in the environment or inside the files**

Install and test:

```sh
doas install -o root -g wheel -m 0755 vultr_ddns_multi.py /usr/local/sbin/vultr_ddns_multi.py

# First run (verbose, IPv4-only)
vultr_ddns_multi.py -v

# Force re-check even if IP hasn't changed (ignores cache)
vultr_ddns_multi.py --force -v
```

Sample "all green" output:

```
Mode: IPv4-only
IPv4=203.0.113.44
[example.com] hosts: @, mail, obsd1 (ttl=300)
[example.com] OK: A @ = 203.0.113.44 (ttl=300)
[example.com] OK: A mail = 203.0.113.44 (ttl=300)
[example.com] OK: A obsd1 = 203.0.113.44 (ttl=300)
...
No changes (records already up-to-date).
```

---

## Logging & rotation

The script appends to `/var/log/vultr_ddns.log` (fallbacks to `~/.cache/vultr-ddns/vultr_ddns.log` if permissions deny). On OpenBSD, add a `newsyslog` rule so it rotates daily and keeps 7 gzips:

```
# /etc/newsyslog.conf
# logfile                    owner:group  mode  count  size  when   flags
/var/log/vultr_ddns.log      root:wheel   640   7      *     @T00   Z
```

You likely already have this hourly cron entry, which is sufficient:

```
0 * * * * /usr/bin/newsyslog
```

---

## Cron

If you run it as **foo**:

```sh
crontab -e
*/5 * * * * /usr/local/sbin/vultr_ddns_multi.py -q
```

If you run it as **root** but want it to read foo's env files, either export these:

```cron
VULTR_API_ENV=/home/foo/.config/vultr/api.env
VULTR_DDNS_ENV=/home/foo/.config/vultr/ddns.env
*/5 * * * * /usr/local/sbin/vultr_ddns_multi.py -q
```

…or rely on the fact that the script will follow `VULTR_API_ENV`/`VULTR_DDNS_ENV` if those keys exist **inside `/etc/vultr/*.env` or `/home/foo/.config/vultr/*.env`**.

---

## IPv6 (optional)

If your ISP gives you public IPv6, add a separate cron for AAAA:

```sh
*/5 * * * * /usr/local/sbin/vultr_ddns_multi.py --ipv6-only -q
```

You can also refresh the caches without touching the API:

```sh
vultr_ddns_multi.py --touch -v
vultr_ddns_multi.py --ipv6-only --touch -v
```

---

## Verifying against Vultr's auth NS

I always check the authoritative nameservers, not the resolver cache:

```sh
for d in example1.com example2.io example3.ca example4.energy example5.com unattributed.blog example6.com; do
  echo "=== $d"
  drill -t -Q @ns1.vultr.com A $d           2>/dev/null || true
  drill -t -Q @ns1.vultr.com A mail.$d      2>/dev/null || true
  drill -t -Q @ns1.vultr.com A obsd1.$d     2>/dev/null || true
done
```

You should see the WAN IP reflected on each host label.

---

## Troubleshooting

- **`VULTR_API_KEY missing`** — confirm the key is in `api.env`. If running as root via cron, ensure the script can find the right `api.env` (see *Env discovery* section).
- **`No host list for domain`** — add a `VULTR_HOSTS_*` line for that zone (either dotted or underscore style).
- **Mail not sending** — fix `MAIL_FROM` (`ops@example.io` style) and ensure `/usr/sbin/sendmail` is present.
- **Log not in /var/log/** — run via root (or syslog method), or accept the fallback in `~/.cache/vultr-ddns/`.
- **GitHub Pages apex** — list the domain in `GITHUB_PAGES_DOMAINS` and do **not** put `@` for that zone in `ddns.env`.

---

## Why this design works

- **Idempotent**: Re-runs are cheap (`OK:` lines, no API calls on unchanged IP via cache).
- **Explicit**: All paths and flags are plain text files you can commit to infra-config.
- **Safe**: Apex guard prevents clobbering GitHub Pages; per-domain TTLs avoid surprises.
- **Portable**: Only needs Python 3 + `requests` and `sendmail` for the optional email.

---

## Appendix: flags cheat sheet

- `-n, --dry-run` — print intended actions, no API writes
- `-q, --quiet` / `-v, --verbose` — console verbosity
- `-d, --domain DOMAIN` — restrict to one or more zones
- `--ipv6-only` — operate on AAAA records (no A)
- `--force` — ignore IP cache; always check/update
- `--status` — show cached IPs
- `--clear-cache` — delete cache files
- `--touch` — refresh cache from current public IP(s) without calling Vultr API
- `--no-gh-guard` — temporarily allow apex updates for GH Pages-listed domains

---

If you want the exact script I used here, it's installed as `/usr/local/sbin/vultr_ddns_multi.py` in my setup and lives alongside the `api.env` and `ddns.env` examples above.
**Attribution:** unattributed read Andy J Smith's github script ddns.py before I wrote 1 ln of code, it's available on https://github.com/andyjsmith/Vultr-Dynamic-DNS which is well written and works perfectly!