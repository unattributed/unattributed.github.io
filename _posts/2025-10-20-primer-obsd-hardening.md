---
layout: post
title: "Building an Internet-Exposed OpenBSD Server: The Authoritative Guide"
date: 2025-10-20
author: unattributed
categories: [openbsd, security]
tags: [pf, httpd, relayd, sshd, security]
---

# Building an Internet-Exposed OpenBSD Server: The Authoritative Primer [Official Sources Only quoted]

When exposing any server to the public internet, the initial configuration sets the security baseline. For OpenBSD, this means starting with the system's built-in defenses and following the explicit guidance from the developers who build them.

This post consolidates the official OpenBSD approach to building a secure, public-facing server. Every recommendation comes directly from OpenBSD documentation, manual pages, or the researchers and developers who create these security features.

## tl,dr

Start with a minimal install. Configure `pf` for default-deny. Harden `sshd` to use keys only. Use the built-in `httpd` and `relayd` for web services. Leverage `sysctl` for additional kernel hardening. Keep the system updated with `syspatch`. The entire approach emphasizes using what's already in the base system, designed to work together securely.

---

## Philosophy: Secure by Default, Simpler by Design

The OpenBSD project's focus on security and code correctness provides the foundation. The guiding principles for a public server are:

* **Minimalism:** Install only what you need. If you don't need a compiler or X11 on a server, don't install those sets.
* **Simplicity:** Use the included tools (`httpd`, `relayd`, `smtpd`, `pf`). Their configurations are easier to audit and maintain.
* **Layered Defenses:** A firewall is not enough. Combine it with service hardening, privilege separation, and kernel security features.

---

## Core Hardening: The Base System

### 1. Packet Filter (`pf`) - The Front Line

The firewall is your first and most critical layer. The official `pf.conf(5)` man page and [PF User's Guide](https://www.openbsd.org/faq/pf/) are required reading.

**A minimal, secure ruleset for a web/SSH server:**

```sh
# /etc/pf.conf

# Macros
ext_if = "em0" # Your external interface
web_ports = "{ http, https }"
ssh_ports = "{ ssh }"

# Tables for brute-force protection
table <ssh_bruteforce> persist

# Default Deny
block all

# Pass loopback
set skip on lo

# Normalize traffic
match in all scrub (no-df)

# SSH with brute-force protection
pass in on $ext_if proto tcp to port $ssh_ports \
    flags S/SA keep state \
    (max-src-conn-rate 15/60, overload <ssh_bruteforce> flush global)

# Web traffic
pass in on $ext_if proto tcp to port $web_ports

# Outbound traffic from the server itself
pass out on $ext_if inet keep state
```

**Enable and test:**
```sh
doas pfctl -nf /etc/pf.conf  # Check syntax
doas pfctl -f /etc/pf.conf   # Load rules
doas rcctl enable pf         # Enable at boot
```

### 2. Secure Shell (`sshd`) - Remote Access

Configure `sshd` to reject passwords and root logins. The `sshd_config(5)` man page is the definitive source.

**Essential `/etc/ssh/sshd_config` edits:**
```conf
# Disable password authentication
PasswordAuthentication no
ChallengeResponseAuthentication no

# Disable root login
PermitRootLogin no

# Restrict supported key types
PubkeyAcceptedKeyTypes ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-512

# Optional: Restrict users/groups that can log in
AllowUsers your_username
```

**Apply changes:**
```sh
doas rcctl restart sshd
```

### 3. Kernel Security (`sysctl`)

OpenBSD's default `/etc/sysctl.conf` is already secure. Verify or add these network-hardening settings:

```sh
# /etc/sysctl.conf
net.inet.ip.redirect=0        # Disable ICMP redirects
net.inet6.ip6.redirect=0      # Disable IPv6 ICMP redirects
net.inet.tcp.drop_synfin=1    # Drop TCP packets with SYN+FIN
```

Enable immediately: `doas sysctl net.inet.tcp.drop_synfin=1`

---

## Service Configuration: Using the Built-in Tools

### 1. Web Services: `httpd` + `relayd`

The built-in web stack runs in a `chroot` by default and uses `pledge(2)` and `unveil(2)`. Follow `httpd(8)`, `relayd(8)`, and [FAQ 13](https://www.openbsd.org/faq/faq13.html).

**A simple `httpd` setup:**
```sh
# /etc/httpd.conf
server "example.com" {
    listen on * port 80
    root "/htdocs/example.com"
}
```

**With `relayd` for TLS termination:**
```sh
# /etc/relayd.conf
http protocol "https" {
    tls keypair "example.com"

    # Security headers
    match request header append "X-Frame-Options" value "SAMEORIGIN"
    match request header append "X-Content-Type-Options" value "nosniff"
}

relay "www" {
    listen on 0.0.0.0 port 443 tls
    protocol "https"
    forward to 127.0.0.1 port 8080
}
```

**Enable the services:**
```sh
doas rcctl enable httpd relayd
doas rcctl start httpd relayd
```

### 2. Mail: `smtpd`

OpenSMTPD is designed for simplicity and security. Use `smtpd(8)` and the [official documentation](https://www.opensmtpd.org/documentation.html).

**A basic receiving MTA configuration:**
```sh
# /etc/smtpd.conf
table aliases file:/etc/mail/aliases

listen on egress

action "local" mbox alias <aliases>
action "relay" relay

match from local for local action "local"
match from local for any action "relay"
```

---

## Operational Security: Maintenance and Monitoring

### 1. System Updates

OpenBSD provides binary patches for the base system.

```sh
doas syspatch    # Apply available security patches
doas pkg_add -u  # Update installed packages
```

### 2. Logging and Monitoring

Configure `syslogd` to log to a remote server if possible. Monitor key logs:

```sh
# Firewall states
doas pfctl -s info

# SSH authentication logs
doas tail -f /var/log/authlog

# General system messages
doas tail -f /var/log/messages
```

### 3. Service Management

Use the built-in `rcctl(8)` for service management:

```sh
doas rcctl ls on          # List services enabled at boot
doas rcctl check sshd     # Verify service status
doas rcctl restart httpd  # Restart a service
```

---

## Security Feature Leverage

The work of OpenBSD researchers and developers provides features you should prefer:

* **`pledge(2)` and `unveil(2)`:** Many base system programs use these to restrict their own capabilities. When choosing software from ports, prefer applications that support these features.
* **LibreSSL:** The default SSL/TLS library, born from the cleanup of OpenSSL by Bob Beck and others. You're using it automatically.
* **`malloc(3)` security features:** The system allocator includes guard pages and randomization.

---

## Troubleshooting and Verification

<div style="border:1px solid #d3d3d3;border-collapse:collapse">
<table style="border:1px solid #d3d3d3;border-collapse:collapse">
  <thead>
    <tr>
      <th style="border:1px solid #d3d3d3;padding:6px">Check</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Command</th>
      <th style="border:1px solid #d3d3d3;padding:6px">Expected Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">Firewall Rules</td>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>doas pfctl -s rules</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">Your configured ruleset, no errors</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">SSH Connectivity</td>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>ssh -o PasswordAuthentication=no user@host</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">Key-based login succeeds, password login rejected</td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">Service Status</td>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>doas rcctl check httpd relayd</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">All services report <code>ok</code></td>
    </tr>
    <tr>
      <td style="border:1px solid #d3d3d3;padding:6px">Open Ports</td>
      <td style="border:1px solid #d3d3d3;padding:6px"><code>doas netstat -ln -f inet</code></td>
      <td style="border:1px solid #d3d3d3;padding:6px">Only expected services listening</td>
    </tr>
  </tbody>
</table>
</div>

---

## Closing

An OpenBSD server exposed to the internet starts from a position of strength. The path to maintaining that security is clear: use the built-in tools, follow the official documentation, and embrace the simplicity of the integrated system. The work of the OpenBSD developers—from `pf` and `httpd` to LibreSSL and the security features in the kernel—provides a coherent, auditable, and maintainable foundation.

This approach has proven itself in practice: a secure default configuration, minimal ongoing maintenance, and clear operational visibility.

For any service not covered here, start with the man page. It's the most current, accurate, and authoritative source available, written by the people who build the system you're running.

*Someday ... really some day* I will write a complete A-Z 0-1 guide on every aspect of using Openbsd as an edge device in an unfriendly world, someday.