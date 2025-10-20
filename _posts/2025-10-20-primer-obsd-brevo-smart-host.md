---
layout: post
title: "Brevo as an Outbound Smart Host for OpenBSD Postfix (iRedMail/Amavis)"
date: 2025-10-20
author: unattributed
categories: [openbsd, email]
tags: [postfix, brevo, amavis, tls, sasl]
-----------------------------------------

# Using Brevo for Your Self-Hosted OpenBSD Email: A Concise, Reproducible Walkthrough

This post documents the exact steps we used to relay outbound mail from an OpenBSD/iRedMail stack (Postfix + Amavis/Dovecot) through **Brevo**’s SMTP service. It’s minimal, auditable, and avoids exposing secrets.

## tl,dr

Create a SASL map with your Brevo SMTP login/key, set `relayhost` to Brevo on port 587, loosen TLS **only** for local Amavis hops via a `tls_policy` map, then restart Postfix and verify in logs that Brevo returns `250 2.0.0 OK`.

---

## 0) Prereqs & sanity

On this host, `base64(1)` wasn’t present. We added a safe fallback using OpenSSL:

```sh
install -d -m 700 "$HOME/bin"
cat > "$HOME/bin/base64" <<'EOF'
#!/bin/sh
# Fallback base64 using OpenSSL; -A = single-line output
exec openssl base64 -A "$@"
EOF
chmod +x "$HOME/bin/base64"
hash -r
command -v base64
```

Create a private env file for Brevo (no world-read access):

```sh
install -m 700 -d "$HOME/.config/brevo"
cat > "$HOME/.config/brevo/api.env" <<'EOF'
# ~/.config/brevo/api.env
BREVO_API_KEY="YOUR_BREVO_API_KEY"                # for REST API (optional)
BREVO_SMTP_LOGIN="xxxxxxxx@smtp-brevo.com"        # SMTP login
BREVO_SMTP_KEY="xxxxxxxxxxxxxxxx"                 # SMTP master password/key
BREVO_DEFAULT_SENDERS="postmaster no-reply security"
EOF
chmod 600 "$HOME/.config/brevo/api.env"
```

(If you test the REST API and see `401 Key not found`, that affects only REST—SMTP works with the SMTP key.)

---

## 1) Postfix SASL credentials

Create the SASL password map for Brevo and lock it down:

```sh
doas sh -c 'printf "%s\n" "[smtp-relay.brevo.com]:587 xxxxxxxx@smtp-brevo.com:xxxxxxxxxxxxxxxx" > /etc/postfix/sasl_passwd'
doas postmap /etc/postfix/sasl_passwd
doas chmod 600 /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db
doas chown root:_postfix /etc/postfix/sasl_passwd /etc/postfix/sasl_passwd.db 2>/dev/null || true
```

---

## 2) Core relay + SASL settings

Tell Postfix to relay via Brevo on 587, enable SASL auth, and require no anonymous mechanisms:

```sh
doas postconf -e 'relayhost=[smtp-relay.brevo.com]:587'
doas postconf -e 'smtp_sasl_auth_enable = yes'
doas postconf -e 'smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd'
doas postconf -e 'smtp_sasl_security_options = noanonymous'
```

---

## 3) TLS policy for Amavis (iRedMail)

If you run the standard iRedMail/Amavis pipeline (127.0.0.1:10024/10025/10026), you may hit:

> **“TLS is required, but was not offered by host 127.0.0.1”**

Fix this by explicitly allowing **no TLS requirement** on those local hops, while **enforcing encryption** to Brevo. Use a `tls_policy` map:

```sh
doas sh -c 'cat > /etc/postfix/tls_policy << "EOF"
[smtp-relay.brevo.com]:587 encrypt
[127.0.0.1]:10024      none
[127.0.0.1]:10025      none
[127.0.0.1]:10026      none
EOF'
doas postmap /etc/postfix/tls_policy
doas chmod 600 /etc/postfix/tls_policy /etc/postfix/tls_policy.db
```

Enable and use the map. Set global security level to `may` (Brevo is forced to `encrypt` by the map):

```sh
doas postconf -e 'smtp_tls_policy_maps = hash:/etc/postfix/tls_policy'
doas postconf -e 'smtp_tls_security_level = may'
```

Remove deprecated `smtp_use_tls` if present:

```sh
doas postconf -X smtp_use_tls
```

---

## 4) Reload and basic health check

```sh
doas postfix check
doas rcctl restart postfix
```

Optional polish (nice EHLO string):

```sh
doas postconf -e 'smtp_helo_name = obsd1.blackbagsecurity.com'
doas rcctl reload postfix
```

---

## 5) Send a test and verify hand-off

Send from the shell (adjust sender/recipient):

```sh
RCPT="your.real.inbox@example.com"
FROM="postmaster@mail.blackbagsecurity.com"
/usr/sbin/sendmail -v -f "$FROM" "$RCPT" <<'EOF'
Subject: Brevo relay test (obsd1)

This is a test from obsd1 relaying through Brevo.
EOF
```

Tail logs and confirm encrypted hand-off to Brevo plus `250 2.0.0 OK`:

```sh
doas tail -f -n 0 /var/log/maillog | egrep -i 'postfix/.+smtp|brevo|status=|queued as'
```

**What you want to see:**

* `Trusted TLS connection established to smtp-relay.brevo.com:587 … TLSv1.3 …`
* `status=sent (250 2.0.0 OK: queued as <…@obsd1.blackbagsecurity.com>)`

---

## Files we touched (auditable)

* `/etc/postfix/sasl_passwd` + `/etc/postfix/sasl_passwd.db` (mode `600`)
* `/etc/postfix/tls_policy` + `/etc/postfix/tls_policy.db` (mode `600`)
* `main.cf` keys (via `postconf -e`):
  `relayhost`, `smtp_sasl_auth_enable`, `smtp_sasl_password_maps`,
  `smtp_sasl_security_options`, `smtp_tls_policy_maps`, `smtp_tls_security_level`, optional `smtp_helo_name`
* (Optional) `~/.config/brevo/api.env` for local testing

---

## Troubleshooting quick table

<div style="border:1px solid #d3d3d3;border-collapse:collapse">
<table style="border:1px solid #d3d3d3;border-collapse:collapse">
  <thead>
    <tr>
      <th style="border:1px solid #d3d3d3;padding:6px">Symptom</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Where to Look</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>TLS is required, but was not offered by host 127.0.0.1</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>/var/log/maillog</code> during Amavis hops</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Add <code>none</code> for <code>[127.0.0.1]:10024/10025/10026</code> in <code>/etc/postfix/tls_policy</code>, keep Brevo as <code>encrypt</code></td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>401 Key not found</code> on REST</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Curling <code>/v3/account</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">Unrelated to SMTP; confirm you’re using the **SMTP key** for Postfix. Generate a valid REST API key only if you need the API.</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">SASL auth fails to Brevo</td>
      <td style="border:1px solid #d3d3d3;padding:6px">Postfix log lines with <code>smtp/… SASL</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">Rebuild map (<code>postmap</code>), verify exact format in <code>/etc/postfix/sasl_passwd</code>, check file modes are <code>600</code></td>
    </tr>
  </tbody>
</table>
</div>

---

## Closing

The minimal set of changes above produces a secure, encrypted relay path from OpenBSD Postfix through Brevo, while keeping local Amavis hops happy and leaving the rest of your iRedMail stack untouched. From here, improve deliverability by authenticating your sending domain in Brevo (SPF/DKIM) and adding a DMARC policy—then watch your logs for the expected `250 2.0.0 OK`.

