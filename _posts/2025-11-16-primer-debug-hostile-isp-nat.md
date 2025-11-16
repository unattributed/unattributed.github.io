---
layout: post
title: "Primer: debugging remote access under hostile ISP NAT (pivoting to IPv6 and WireGuard)"
date: 2025-11-16
author: unattributed
categories: [openbsd, networking, firewall]
tags: [pf, ipv6, wireguard, ssh, isp, cgnat]
---

# When your ISP fights you: remote SSH under hostile NAT

I run a hardened mail and web stack on an OpenBSD host behind an ISP router. I expect three things to be true:

1. I can reach the server from the local LAN.
2. I can reach it over an authenticated VPN tunnel.
3. I can, under strict firewall rules, reach it directly from the public Internet for specific services like SSH and HTTPS.

Recently, item 3 quietly broke.

This post walks through the actual debugging process and the remediation, with system details anonymised. The tools are standard OpenBSD userland and firewall components documented in the OpenBSD manuals (`ifconfig(8)`, `netstat(1)`, `pf(4)`, `pf.conf(5)`, `ssh(1)`), plus a basic ISP router web interface and a WireGuard tunnel as described in the WireGuard project docs.

The outcome:

- Incoming IPv4 is effectively unusable because of the ISP and their upstream NAT.
- Incoming IPv6 works reliably if the client has working IPv6.
- A WireGuard tunnel provides a predictable management plane regardless of the ISP.
- The firewall (`pf`) was updated to handle IPv6 explicitly while keeping the hardening goals.

---

## Environment (high level)

Very roughly:

- **Server:** OpenBSD host running mail, web, SSH and VPN services.  
  Services and PF behavior are documented in the OpenBSD manual pages, for example `sshd(8)` and `pf.conf(5)`.
- **Firewall:** `pf` with anchors for self hosting, spam defences and ACME automation, as described in the OpenBSD `pf` and `anchors` documentation.
- **Access VPN:** WireGuard server on the OpenBSD box. WireGuard protocol and configuration syntax are documented in the official WireGuard documentation.
- **Router:** ISP supplied DSL router, configured with:
  - A private WAN IP on a PPP style interface (10.x address).
  - One internal LAN network.
  - A supposed DMZ target pointing to the OpenBSD host.
  - Some explicit port forwards for things like SSH and HTTPS.

DNS for public hostnames is managed off site, with dynamic IPv4 updates via API and static or controlled AAAA records for IPv6.

---

## Symptom: LAN is fine, Internet cannot reach SSH

From the local LAN:

- SSH to the server works over IPv4.
- Mail and web work as expected.
- Internal monitoring looks healthy.

From outside the LAN:

- Connecting to the public hostname on port 22 simply times out over IPv4.
- Adding port forwards and a DMZ entry on the router does not help.
- There are no `pf` logs showing any inbound connection attempts, even with a `log` keyword on the relevant rules.

So either:

1. The router is not forwarding at all, or  
2. Something upstream of the router is dropping or redirecting traffic before it ever reaches the DMZ.

---

## Step 1: confirm what the server thinks its public IP is

On the OpenBSD host, I first confirmed outbound connectivity and the perceived public IPv4 address using standard tools:

- A DNS based method, such as querying a resolver that reports the client address.
- A simple HTTP based echo service, such as a basic `/ip` endpoint.

These are conceptually the same as the `myip.opendns.com` trick and simple `ifconfig.me` style services, both of which are described in public documentation by their respective providers.

The result: the **public IPv4** that the outside world sees is a certain address `X.Y.Z.W`.

The ISP router status page, however, shows the WAN side as a **private 10.x address** on its PPP interface. That is a strong hint that carrier grade NAT or at least an extra layer of provider NAT is in play.

The OpenBSD host has:

- A single IPv4 on its LAN interface, in a private RFC1918 range.
- A default route via the router.
- No additional public address directly on the kernel.

So inbound IPv4 would have to traverse:

> Internet → Provider edge → Provider NAT → DSL router private WAN → DSL router NAT → OpenBSD host

and there is no guarantee that the provider is forwarding unsolicited inbound traffic at all.

---

## Step 2: verify the server is actually listening

Before blaming anything else, I confirmed that the host is listening where it should be.

On the OpenBSD host, `netstat -an` shows that `sshd` is listening on:

- `*.22` for IPv4.
- `tcp6` `*.22` for IPv6 in the same way that OpenSSH documents in `sshd_config(5)`.

Other services (HTTPS, IMAP, SMTP, etc.) are also listening on both IPv4 and IPv6 addresses, but SSH is the primary probe.

The host based firewall is `pf`, so I checked the active ruleset:

- `pfctl -sr` for global rules.
- `pfctl -a <anchor> -sr` for specific anchors (for example self hosting and spamd).

The anchor that handles public facing services allows inbound SSH on IPv4 and, after later modification, also on IPv6. The rules use `pass in quick on egress ... port 22` style lines, consistent with the OpenBSD `pf.conf` manual examples.

From the server toward an external test system, outbound SSH works fine. That confirms outbound path and DNS resolution.

---

## Step 3: test from another network and capture traffic

From an external client on another network with standard IPv4 only access:

- An SSH attempt to the public hostname over IPv4 simply times out.
- `tcpdump` on the OpenBSD host interface (LAN side) sees no inbound SYN packets for port 22, 80, 443, or the WireGuard UDP port.
- `tcpdump` on the host sees only local LAN traffic (for example existing SSH sessions from inside the LAN) and its own outbound flows.

On the router, DMZ and port forwards are pointed at the correct LAN IP of the OpenBSD host, but nothing reaches it. That aligns with the carrier grade NAT hypothesis: the router never sees the incoming packets, or the ISP router is not truly in full cone mode.

At this point, incoming IPv4 over the public Internet looks effectively blocked by the ISP path, independent of my own NAT and DMZ settings.

---

## Step 4: bring IPv6 into the picture

The ISP router has an IPv6 configuration page which supports:

- Enabling IPv6.
- Receiving a delegated prefix on the WAN side.
- Advertising that prefix to the LAN via router advertisements.

Once IPv6 is enabled and the router rebooted, the OpenBSD host shows, via `ifconfig(8)` as documented in the OpenBSD manual:

- A link local address on the LAN interface.
- One or more global IPv6 addresses in the delegated prefix, one of which is marked temporary and one stable.
- A default IPv6 route pointing to the router link local.

The kernel routing table (`netstat -rn -f inet6`) shows a default route and the on link prefix, in line with the OpenBSD networking documentation.

Outbound IPv6 now works: the host can reach IPv6 capable mirrors and echo services. However, the firewall still needs to be explicit about how IPv6 is handled.

---

## Step 5: teach `pf` about IPv6, minimally but correctly

The initial ruleset targeted IPv4 first, with a very strict IPv6 stance that essentially blocked everything, as advised in many OpenBSD hardening examples.

To support controlled IPv6 traffic, I adjusted the base ruleset along lines that are consistent with the OpenBSD `pf.conf(5)` guidance:

- Allow essential IPv6 ICMP on egress and on the VPN interface, with `pass quick on egress inet6 proto ipv6-icmp ... keep state`.  
  This matches how the OpenBSD documentation describes the importance of ICMPv6 for path MTU and neighbour discovery.
- Allow outbound IPv6 TCP and UDP on egress with state, similar to the IPv4 rules.
- Allow outbound IPv6 on the WireGuard interface for future use.
- Keep the anchors for self hosting, spam handling and ACME grouped and unchanged in structure.

For inbound traffic:

- Add explicit IPv6 versions of the SSH, HTTPS and other required service rules, using `inet6` and targeting `(egress)` or the host IPv6 in the same way as their IPv4 counterparts.
- Keep default deny and logging, so that attempts which do arrive can be observed.

The details are specific to each deployment, but align with the combination of OpenBSD `pf(4)` semantics and the OpenSSH `sshd(8)` default listen behaviour.

---

## Step 6: IPv6 testing from various clients

With IPv6 enabled and `pf` updated, I tested from three perspectives.

### 1. Local LAN

From another host on the same LAN:

- SSH over IPv4 works.
- SSH over IPv6 using the global IPv6 address also works.
- `tcpdump` shows the expected SYN, SYN-ACK, ACK handshake for both families.

This confirms that the OpenBSD host and its firewall rules for IPv6 are correct and that the router forwards LAN IPv6 to the host.

### 2. A typical external IPv4 only path

From a laptop connected to a different IPv4 only network:

- The DNS A record for the mail host resolves to a public IPv4.
- SSH to that IPv4 times out.
- The AAAA record is either absent or not reachable because the client has no usable IPv6 connectivity.
- `dig` with IPv4 only queries returns the A record, but IPv6 queries have no working resolver or route.

This is consistent with the ISP environment: IPv4 inbound is not usable, and the client network offers no IPv6 route to experiment with.

### 3. A VPN that supports IPv6

From a mobile device using a third party VPN provider:

- The VPN interface on the device provides both IPv4 and IPv6 connectivity, described in the VPN provider documentation.
- The device can query AAAA records and reaches the IPv6 Internet via the VPN exit node.
- An `ssh -6` command to the mail host hostname now reaches the OpenBSD server on its global IPv6 address and successfully completes key based authentication.

This end to end test proves:

- The AAAA record is correct.
- The ISP router is forwarding IPv6 packets from the Internet to the OpenBSD host.
- The `pf` ruleset allows SSH over IPv6 as configured.

IPv4 inbound remains broken from that same VPN, which strongly reinforces the theory that IPv4 is blocked or filtered somewhere upstream by the ISP or their carrier grade NAT.

---

## Step 7: what about WireGuard

The deployment also uses WireGuard as an access VPN, with the OpenBSD host running a WireGuard server. WireGuard behaviour and configuration are based on the official WireGuard documentation.

After the IPv6 changes, the WireGuard path showed a separate problem: one test laptop could not reach the WireGuard endpoint, even though local configuration had not changed. This turned out to be a consequence of the same IPv4 inbound situation: if the WireGuard UDP port is only reachable over IPv4, and IPv4 inbound is blocked upstream, then the WireGuard control plane from the outside cannot reach the server.

This leads to a clear separation:

- **Primary management path:** IPv6 plus WireGuard when available.
- **Public path:** IPv6 directly from the Internet.
- **IPv4 path:** Only usable from inside the LAN or from special environments where the ISP allows it.

The exact division of roles will differ for each deployment, but the pattern is repeatable.

---

## Threat model and design choices

The investigation above forces some practical choices.

1. **Assume ISP controlled IPv4 is untrusted and unpredictable**  
   Incoming IPv4 might work today and fail tomorrow, or be silently filtered.  
   Mitigation: treat IPv4 as best effort for outbound, and avoid depending on it for inbound administrative access.

2. **Prefer IPv6 for authenticated remote access**  
   IPv6 gives a true end to end path where the ISP cannot easily hide additional NAT layers.  
   Mitigation: expose SSH over IPv6 behind a strict `pf` policy, keeping strong keys and limited user accounts, in line with the OpenSSH documentation.

3. **Add a VPN overlay for control traffic**  
   WireGuard provides a stable administration plane independent of ISP routing changes.  
   Mitigation: restrict key based WireGuard access to known peers, and use `pf` to limit what those peers can reach on the host, following both WireGuard and OpenBSD pf best practices.

4. **Do not over trust DMZ and port forwarding checkboxes**  
   The router can honestly report a DMZ configuration, but if its WAN is behind a private 10.x network managed by the ISP, many packets will never reach it.  
   Mitigation: always confirm with independent tests, such as external SSH attempts and `tcpdump` on the host.

---

## A repeatable checklist for similar situations

Here is a condensed checklist you can adapt without exposing sensitive system information:

1. **Confirm listeners and firewall on the server**
   - Use `netstat` or equivalent to verify SSH and other services are listening on both IPv4 and IPv6.
   - Inspect your firewall rules with the appropriate tools (`pfctl -sr` on OpenBSD).

2. **Determine your real public addresses**
   - Use DNS based echo methods and simple HTTP echo services from the server itself.
   - Compare with what your router claims for its WAN IP.
   - If the router WAN is a private address, suspect carrier grade NAT.

3. **Capture traffic during a failing connection**
   - Run `tcpdump` on the server interface targeting the relevant ports before testing from outside.
   - If you see no inbound packets at all, the problem is probably upstream of the server and its firewall.

4. **Enable and verify IPv6 (if available from your ISP)**
   - Confirm that the router receives a global prefix and advertises it internally.
   - Check that the server receives a global IPv6 address and has a default IPv6 route.

5. **Update firewall rules for IPv6 explicitly**
   - Allow essential ICMPv6 and stateful outbound IPv6 as described in your OS firewall documentation.
   - Add explicit inbound IPv6 rules for services you intend to expose.

6. **Test IPv6 from multiple external networks**
   - From IPv4 only networks to see where it fails.
   - From networks or VPNs that provide IPv6 end to end.

7. **Layer a VPN for administrative access**
   - Use WireGuard or another modern VPN to establish a predictable control channel.
   - Restrict what that VPN can do using host firewall rules.

8. **Document and periodically recheck**
   - ISPs change routing and policies. Keep a simple test script or notebook of commands that validate both IPv4 and IPv6 paths, and run them after major changes or outages.

---

## Closing thoughts

The interesting part of this outage was not a misconfigured firewall on the OpenBSD host. The host ruleset and services were fine, as far as `pf` and `sshd` were concerned, following their vendor documentation. The real constraint was an ISP path that quietly turned inbound IPv4 into a best effort service at best, and a non existent service at worst.

By introducing IPv6 carefully, updating `pf` to treat it as a first class participant, and using a WireGuard overlay, it is possible to build a remote access story that stays under your control, even when the ISP behaves like an unpredictable middlebox.

If you run your own infrastructure at home or in a small office, it is worth planning for this reality up front: do not assume that a public IPv4 will always behave like a truly public address, and give IPv6 and VPNs explicit roles in your design rather than treating them as afterthoughts.