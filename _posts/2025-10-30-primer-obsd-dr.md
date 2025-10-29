---
layout: post
title: "Zero-Cost DR Snapshots for OpenBSD iRedMail (GPG + Git LFS)"
date: 2025-10-30
author: unattributed
categories: [openbsd, email, dr]
tags: [postfix, dovecot, amavis, nginx, roundcube, sogo, mysql, gpg, git-lfs, backup]
---

# Disaster Recovery that costs \$0 and leaks \$0 plaintext

This post documents a reproducible DR workflow for an OpenBSD iRedMail stack (Postfix + Dovecot + Amavis/ClamAV + Nginx + Roundcube/SOGo + MariaDB/MySQL). It creates a **single encrypted snapshot** of configs, mailboxes, and SQL, and pushes the encrypted blob to a private Git repository tracked by **Git LFS**. No plaintext leaves the host. Commits are signed with OpenPGP.

All hostnames and fingerprints in this post are **illustrative** (`example.com`, etc.). The sample fingerprint is deliberately changed: `FPR: 0123456789ABCDEFCAFEBABEDEADBEEF01234567`.

---

## tl,dr

- One command takes a complete snapshot into `/root/irecovery-YYYYMMDD-HHMMSS/`, then tars it and **encrypts at source** with your OpenPGP key.
- A tiny ksh helper copies the `.tgz.gpg` into `./snapshots/` in a private Git repo and **pushes via Git LFS**.
- Recovery = `git clone` → `git lfs pull` → `gpg -d | tar -x` → restore configs/SQL with standard commands.

---

## Why this design

* **Zero cost**: uses free/private Git hosting + free LFS allowance for modest snapshot sizes (monitor your usage).
* **Zero plaintext**: encryption happens **before** anything touches Git.
* **Auditable & portable**: DR artifact is a single file with a matching `.sha256`. Git history and signed commits prove provenance.
* **Boring tech**: ksh, tar, gpg, git, git-lfs. Easy to review and maintain.

---

## What the snapshot contains

- System facts for forensics (`uname`, `rcctl ls on`, package list, disk layout)
- **Postfix** configs (full `/etc/postfix`, maps, historical backups if present)
- **Dovecot** (`/etc/dovecot/`), **Amavis/ClamAV** configs and DKIM key material
- **Web** tier (`nginx -T`, `/etc/nginx`, optional `/etc/httpd.conf`, SOGo/iRedAdmin/roundcube configs)
- **TLS/ACME** (`/etc/ssl`, `/etc/acme*`, plus live `s_client` probes on 25/465/587)
- **SQL dumps** for `vmail`, `iredadmin`, `iredapd`, `amavisd`, `roundcubemail`, `sogo`
- **Mailboxes** (`/var/vmail` tarball, gzip-compressed)
- **PF, cron, hosts, resolv.conf, /etc/mail`**
- Optional **DNS inventory** via your Vultr export tool

Nothing is pruned **before** encryption; you decide retention on the Git side.

---

## Prereqs

```sh
doas pkg_add gnupg git git-lfs
# (MariaDB/MySQL tools already on iRedMail hosts)
````

Import and trust your **signing/encryption** key (sample fingerprint redacted here):

```sh
# On the DR host (root), import your public and secret keys
gpg --import /root/keys/public.asc
gpg --import /root/keys/secret.asc

# Optional: trust (ownertrust) if needed, then confirm
gpg --list-keys
# pub   ed25519 2025-10-25 [SC]
#       0123456789ABCDEFCAFEBABEDEADBEEF01234567
# uid   you <ops@example.net>
# sub   cv25519 2025-10-25 [E]
```

Pinentry/agent (use curses on OpenBSD):

```sh
install -d -m 700 -o root -g wheel /root/.gnupg
cat > /root/.gnupg/gpg-agent.conf <<'EOF'
pinentry-program /usr/local/bin/pinentry-curses
default-cache-ttl 86400
max-cache-ttl 604800
EOF
gpgconf --kill gpg-agent; gpg-connect-agent reloadagent /bye
export GPG_TTY=$(tty)
```

---

## The two tiny scripts

You’ll use **two** ksh helpers: one to **create** the snapshot and encrypt it, and one to **push** the latest encrypted tarball via LFS. Place them as shown; both are OpenBSD/ksh-safe.

### 1) Snapshot & encrypt (`/root/bin/iredmail-dr-backup.sh`)

This collects everything listed above, tars to `/root/irecovery-*.tgz`, and, if a recipient is supplied, produces `/root/irecovery-*.tgz.gpg`.

Usage:

```sh
# Example with DNS export, Postfix chroot services sync, and encryption
/root/bin/iredmail-dr-backup.sh \
  --dump-dns --fix-postfix-services \
  --gpg-recipient "0123456789ABCDEFCAFEBABEDEADBEEF01234567" \
  example.com example.net example.org
```

> Tip: add `--rm-plaintext` to delete the unencrypted `.tgz` after a successful encrypt.

### 2) Push latest via LFS (`/root/obsd1-dr/bin/dr-push-latest.sh`)

This idempotently:

* ensures `*.tgz.gpg` is LFS-tracked,
* copies the **latest** `/root/irecovery-*.tgz.gpg` into `./snapshots/`,
* writes a matching `snapshots/<file>.sha256`,
* commits (signed) and `git push`.

Usage:

```sh
# Dry run
/root/obsd1-dr/bin/dr-push-latest.sh -n

# Real push
/root/obsd1-dr/bin/dr-push-latest.sh

# Keep only the newest 7 encrypted snapshots in the repo
/root/obsd1-dr/bin/dr-push-latest.sh --keep 7
```

---

## Repository hygiene (private Git + LFS)

Initialize once:

```sh
cd /root/obsd1-dr
git init
git lfs install
git remote add origin git@github.com:YOURORG/your-private-dr-repo.git

# Never commit plaintext
cat > .gitignore <<'EOF'
*.tgz
irecovery-*/
*.sql
*.log
EOF

# LFS for encrypted blobs
echo '*.tgz.gpg filter=lfs diff=lfs merge=lfs -text' > .gitattributes

git add .gitignore .gitattributes
git commit -S -m "init: ignore plaintext; track *.tgz.gpg with LFS"
git push -u origin main
```

---

## Daily operation

Create & push (one liner):

```sh
/root/bin/iredmail-dr-backup.sh \
  --dump-dns --fix-postfix-services \
  --gpg-recipient "0123456789ABCDEFCAFEBABEDEADBEEF01234567" \
  example.com example.net example.org \
  && /root/obsd1-dr/bin/dr-push-latest.sh --keep 14
```

Cron it (e.g., 02:30 daily):

```sh
# root's crontab
30 2 * * * export GPG_TTY=$(tty); /root/bin/iredmail-dr-backup.sh --dump-dns --fix-postfix-services --gpg-recipient 0123456789ABCDEFCAFEBABEDEADBEEF01234567 example.com example.net example.org && /root/obsd1-dr/bin/dr-push-latest.sh --keep 14
```

---

## Recovery procedure (bare-metal or new VM)

On a clean OpenBSD host:

```sh
# 1) tools
doas pkg_add gnupg git git-lfs

# 2) keys
gpg --import /root/keys/secret.asc
export GPG_TTY=$(tty)

# 3) get the DR repo
cd /root
git clone git@github.com:YOURORG/your-private-dr-repo.git obsd1-dr
cd obsd1-dr
git lfs pull

# 4) pick a snapshot and decrypt to a temp tgz
LATEST=$(ls -t snapshots/irecovery-*.tgz.gpg | head -1)
TMP=$(mktemp -t irecover.XXXXXX.tgz)
gpg -d "$LATEST" > "$TMP"

# 5) inspect before extracting
tar -tzf "$TMP" | head

# 6) extract under /root
tar -C /root -xzf "$TMP"

# 7) walk the tree and restore in order (examples)
ROOT_DIR=$(tar -tzf "$TMP" | head -1 | cut -d/ -f1)   # e.g. irecovery-20251029-165028

# postfix/dovecot/etc (merge carefully; keep your new host's rc & device specifics)
/bin/cp -Rp "/root/$ROOT_DIR/postfix/etc.postfix" /etc/postfix
/bin/cp -Rp "/root/$ROOT_DIR/dovecot/etc.dovecot" /etc/dovecot
/bin/cp -Rp "/root/$ROOT_DIR/etc/mail" /etc/mail
/bin/cp -Rp "/root/$ROOT_DIR/tls/etc.ssl" /etc/ssl
test -d "/root/$ROOT_DIR/tls/etc.acme" && /bin/cp -Rp "/root/$ROOT_DIR/tls/etc.acme" /etc/acme

# sql
for db in vmail iredadmin iredapd amavisd roundcubemail sogo; do
  mysql "$db" < "/root/$ROOT_DIR/sql/${db}.sql"
done

# mailboxes
tar -C / -xpf "/root/$ROOT_DIR/mail/var-vmail.tar.gz" 2>/dev/null || \
  (gunzip -c "/root/$ROOT_DIR/mail/var-vmail.tar.gz" | tar -C / -xpf -)

# permissions sanity (illustrative)
chown -R _vmail:_vmail /var/vmail
chmod -R go-rwx /var/vmail

# services up
rcctl enable mysqld postfix dovecot amavisd clamd nginx php83_fpm sogod
rcctl restart mysqld
rcctl restart postfix dovecot amavisd clamd nginx php83_fpm sogod
```

> Validate TLS: check `/root/$ROOT_DIR/reports/tls_summary.txt`, then re-probe with `openssl s_client` on 25/465/587. Update A/AAAA/MX/SPF/DKIM/DMARC if your IP or DNS endpoint changed.

---

## Security notes & caveats

* **Metadata**: commit times, object sizes, and filenames are visible to your Git host even though content is encrypted. If that matters, pad or chunk archives and randomize names.
* **Key custody**: store your private key offline and import a **subkey** onto the mail host where possible.
* **LFS usage**: LFS quotas exist. Snapshots compress well, but mailbox size drives cost. Use `--keep N` to prune.
* **Plaintext**: add `--rm-plaintext` to delete the `.tgz` after a successful encrypt.
* **Trust**: sign every commit and verify `git log --show-signature` during audits.

---

## Troubleshooting quick table

<div style="border:1px solid #d3d3d3;border-collapse:collapse">
<table style="border:1px solid #d3d3d3;border-collapse:collapse">
<thead><tr><th style="border:1px solid #d3d3d3;padding:6px">Symptom</th><th style="border:1px solid #d3d3d3;padding:6px">Likely cause</th><th style="border:1px solid #d3d3d3;padding:6px">Fix</th></tr></thead>
<tbody>
<tr><td style="border:1px solid #d3d3d3;padding:6px">`gpg: signing failed: Inappropriate ioctl for device`</td><td style="border:1px solid #d3d3d3;padding:6px">No pinentry TTY in cron/SSH</td><td style="border:1px solid #d3d3d3;padding:6px">Set `GPG_TTY=$(tty)`; use `pinentry-curses`; or sign only interactively</td></tr>
<tr><td style="border:1px solid #d3d3d3;padding:6px">`Permission denied (publickey)` on `git push`</td><td style="border:1px solid #d3d3d3;padding:6px">SSH key or deploy key missing on the Git host</td><td style="border:1px solid #d3d3d3;padding:6px">Register the repo SSH key, keep the repo **private**</td></tr>
<tr><td style="border:1px solid #d3d3d3;padding:6px">Large LFS usage</td><td style="border:1px solid #d3d3d3;padding:6px">Mailbox tarball dominates</td><td style="border:1px solid #d3d3d3;padding:6px">Use `--keep N`; exclude cold mailboxes; split per-domain repositories</td></tr>
</tbody>
</table>
</div>

---

## Closing

If you can explain a DR plan **on a whiteboard** in under five minutes, you can execute it under pressure. This approach stays simple: **encrypt first, publish the ciphertext, sign the history**. It’s repeatable, cheap, and easy to audit—exactly what you want on a bad day.