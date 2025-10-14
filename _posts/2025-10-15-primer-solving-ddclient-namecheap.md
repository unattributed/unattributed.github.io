---
layout: post
title: "Primer ddclient multi-domain support"
date: 2025-10-15
author: unattributed
categories: [openbsd, ddns]
tags: [ddclient, namecheap, openbsd]
---
# Solving ddclient updates for multiple domains on Namecheap [OpenBSD specific, reproducible]

I run several domains on Namecheap, on a single OpenBSD host to keep A records in sync with my WAN IP. I started with a single `/etc/ddclient/ddclient.conf` that listed all domains and hosts. Only the last domain updated. The logs insisted everything was fine, but authoritative DNS did not move for the earlier domains.

This post documents the root cause and a production ready fix, including exact file paths, permissions, service wiring, and verification. It targets ddclient 3.9.1 on OpenBSD, Namecheap Dynamic DNS, and multiple domains with repeated host labels, for example `@`, `mail`, `obsd1`.

## tl,dr

ddclient 3.9.1 keys its in memory config by host label, not by the pair [domain, host]. If you repeat labels across domains inside one config file, the last domain block wins. The fix, split one config per domain, give each a unique cache file, run them serially with a tiny driver, and log everything.

---

## Symptoms

* Only the last domain in `/etc/ddclient/ddclient.conf` updates
* `ddclient -debug` shows `config{mail}{login}` set to the last domain for all labels
* Logs show `good: IP address set ...` but authoritative DNS stays unchanged for earlier domains
* Intermittent `FATAL: Cannot create file '/var/cache/ddclient/ddclient.cache'` when cache permissions are wrong

### Minimal reproduction

```sh
# one file with many domains that share labels [@, mail, obsd1]
# ddclient only acts on the last block
/etc/ddclient/ddclient.conf
```

### Correct mental model

One config entry per [domain, host] pair, unique cache per domain, iterate configs.

---

## Final layout

We will replace the single file with:

* One driver: `/usr/local/sbin/ddclient-multi.sh`
* One config per domain: `/etc/ddclient/<domain>.conf`
* One cache per domain: `/var/cache/ddclient/<domain>.cache`
* rcctl flags that run the driver every 300 seconds, the driver runs each config once

### 1) Driver [serial executor, syslog, robust]

**File path**
`/usr/local/sbin/ddclient-multi.sh`

**Change description**
add driver that iterates per domain configs, calls ddclient for each, logs to daemon facility

**Git commit comment**

```
add ddclient driver to run one config per domain and log to daemon
```

```sh
#!/bin/sh
set -eu
CONF_DIR="/etc/ddclient"
BIN="/usr/local/sbin/ddclient"
LOGTAG="ddclient-multi"

if ! command -v "$BIN" >/dev/null 2>&1; then
  logger -p daemon.notice -t "$LOGTAG" "error, ddclient not found at $BIN"
  echo "error, ddclient not found at $BIN" >&2
  exit 1
fi

found=0
for cfg in "$CONF_DIR"/*.conf; do
  [ -f "$cfg" ] || continue
  found=1
  logger -p daemon.notice -t "$LOGTAG" "running $cfg"
  "$BIN" -file "$cfg" -daemon=0 -syslog
done

if [ "$found" -eq 0 ]; then
  logger -p daemon.notice -t "$LOGTAG" "warning, no config files found under $CONF_DIR"
  echo "warning, no config files found under $CONF_DIR" >&2
fi
```

```sh
doas install -o root -g wheel -m 0755 /usr/local/sbin/ddclient-multi.sh
```

### 2) Per domain configs

Each file includes: its own cache path, Namecheap protocol and server, the domain login, the domain specific password, and the host labels to update.

**Common prework, cache and pid directories**

```sh
doas install -d -o _ddclient -g _ddclient -m 0750 /var/cache/ddclient
doas install -d -o _ddclient -g _ddclient -m 0755 /var/run/ddclient
```

#### Example, `waywardclowns.com`

**File path**
`/etc/ddclient/waywardclowns.com.conf`

**Change description**
add ddclient config for waywardclowns.com with unique cache and hosts

**Git commit comment**

```
add waywardclowns.com ddclient config with per-domain cache
```

```conf
daemon=0
syslog=yes
ssl=yes
use=web, web=checkip.amazonaws.com, web-skip='^Address'

cache=/var/cache/ddclient/waywardclowns.com.cache
pid=/var/run/ddclient/ddclient.pid

protocol=namecheap
server=dynamicdns.park-your-domain.com
login=waywardclowns.com
password=REDACTED_waywardclowns_com
@, mail, obsd1
```

Repeat for your other domains. Use the same structure, only change the names and passwords, and adjust the host list. For a domain that uses GitHub Pages on the apex, do not include `@`.

#### Template for the rest

Replace `<domain>` and `<password>` and host list as needed.

**File path**
`/etc/ddclient/<domain>.conf`

**Change description**
add ddclient config for <domain> with per-domain cache

**Git commit comment**

```
add <domain> ddclient config with per-domain cache
```

```conf
daemon=0
syslog=yes
ssl=yes
use=web, web=checkip.amazonaws.com, web-skip='^Address'

cache=/var/cache/ddclient/<domain>.cache
pid=/var/run/ddclient/ddclient.pid

protocol=namecheap
server=dynamicdns.park-your-domain.com
login=<domain>
password=<password>
@, mail, obsd1
```

**Permissions, ownership, empty caches**

```sh
doas chown _ddclient:_ddclient /etc/ddclient/*.conf
doas chmod 0600 /etc/ddclient/*.conf

for f in /etc/ddclient/*.conf; do
  base="$(basename "$f" .conf)"
  doas sh -c ": > /var/cache/ddclient/${base}.cache"
  doas chown _ddclient:_ddclient "/var/cache/ddclient/${base}.cache"
done
```

### 3) Service wiring [rcctl]

**Change description**
configure ddclient service to run the driver every 300 seconds

**Git commit comment**

```
wire ddclient to driver using rcctl flags with 5 minute interval
```

```sh
doas rcctl set ddclient flags "-daemon=300 -exec /usr/local/sbin/ddclient-multi.sh"
doas rcctl restart ddclient
doas rcctl get ddclient flags
doas rcctl check ddclient
```

### 4) Remove the old monolithic file

If you leave `/etc/ddclient/ddclient.conf` in place, your driver will also try to run it, which reintroduces the generic cache path, and the last domain wins bug.

**Change description**
disable legacy config so the driver cannot run it

**Git commit comment**

```
disable legacy single ddclient.conf to prevent fallback
```

```sh
doas test -f /etc/ddclient/ddclient.conf && doas mv /etc/ddclient/ddclient.conf /etc/ddclient/ddclient.conf.disabled
```

---

## Verification, end to end

### Authoritative DNS, query Namecheap name servers

```sh
for d in waywardclowns.com blackbagsecurity.io blackbagsecurity.com stumblesthedrunk.com redactedsecurity.ca redactedsolar.energy; do
  echo "=== $d"
  drill -Q -t -4 @dns1.registrar-servers.com A $d || true
  drill -Q -t -4 @dns1.registrar-servers.com A mail.$d || true
  drill -Q -t -4 @dns1.registrar-servers.com A obsd1.$d || true
done

# example for a domain with GitHub Pages apex, only check dynamic hosts
echo "=== unattributed.blog"
drill -Q -t -4 @dns1.registrar-servers.com A mail.unattributed.blog || true
drill -Q -t -4 @dns1.registrar-servers.com A obsd1.unattributed.blog || true
```

You should see the WAN IP for each checked host, not `127.0.0.1`, not `10.10.10.10`.

### Logs, driver plus ddclient

The driver logs to the daemon facility. Watch both daemon and messages, depending on your `syslogd.conf`.

```sh
doas tail -n 200 /var/log/daemon   | egrep 'ddclient-multi|SETDNSHOST|good: IP address set' || true
doas tail -n 200 /var/log/messages | egrep 'ddclient-multi|ddclient' || true
```

Look for `running /etc/ddclient/<domain>.conf`, followed by three `SETDNSHOST` calls for each domain.

### Manual one shot, helpful for first run

```sh
doas /usr/local/sbin/ddclient-multi.sh
```

---

## Why the single file failed

`ddclient -debug` reveals the problem clearly. `config{@}{login}`, `config{mail}{login}`, and `config{obsd1}{login}` all held the same domain, the last block in the file. That happens because ddclient maps entries by host label only, so repeated labels collide. The per domain split prevents collisions, each process uses a different config and a different cache.

---

## Namecheap API probe [independent of ddclient]

If a specific host refuses to move, verify credentials and host existence with the raw API. Replace variables accordingly.

```sh
DOMAIN=example.com
HOST=obsd1
PASS='your_namecheap_dynamic_dns_password_for_example.com'
IP=$(ftp -o - https://checkip.amazonaws.com | tr -d ' \n\r')

ftp -o - "https://dynamicdns.park-your-domain.com/update?host=${HOST}&domain=${DOMAIN}&password=${PASS}&ip=${IP}"
```

You want `<ErrCount>0</ErrCount>` and `<Done>true</Done>`. If you see “A Record not found”, create an “A + Dynamic DNS” host in Namecheap first, save with a placeholder, then run ddclient again.

---

## Troubleshooting matrix

<div style="border:1px solid #d3d3d3;border-collapse:collapse">
<table style="border:1px solid #d3d3d3;border-collapse:collapse">
  <thead>
    <tr>
      <th style="border:1px solid #d3d3d3;padding:6px">Symptom</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Likely cause</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">Only last domain updates</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Config collision on repeated labels</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Split per domain configs, unique caches, run with driver</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">`FATAL, Cannot create ... ddclient.cache`</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Cache path unwritable, or legacy single file still in use</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Create per domain caches owned by `_ddclient`, remove legacy file</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">`good: IP address set`, DNS unchanged</td>
      <td style="border:1px solid #d3d3d3;padding:6px">You looked at resolver cache or public resolvers with lag</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Query `@dns1.registrar-servers.com` and peers directly</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">A host sticks at 127.0.0.1 or 10.10.10.10</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Host is not “A + Dynamic DNS” at Namecheap</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Create “A + Dynamic DNS” for that host, then rerun</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">No log lines in `/var/log/daemon`</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Syslog routes to `/var/log/messages` on your host</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Tail both files, or change `logger -p daemon.notice` in driver as desired</td>
    </tr>
  </tbody>
</table>
</div>

---

## Security notes

* Store per domain configs as `_ddclient:_ddclient`, mode 0600
* Do not commit real passwords, use your secret store, or template the files at deploy time
* The driver runs as root via rc, ddclient itself drops privileges to `_ddclient` while writing caches if installed from packages

---

## Closing

The fix is simple once you know the constraint, treat each domain separately, keep caches separate, iterate with a small driver, and query the authoritative DNS to verify. This has been running cleanly for me on OpenBSD, with clear logs and no collisions.

If you have an alternative approach that keeps a single process without collisions, for example a newer ddclient or a patch that keys by [domain, host], I would love to compare notes.
