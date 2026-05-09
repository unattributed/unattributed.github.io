---
layout: post
title: "Primer: Cleaning Up a Fresh Parrot OS 7.x Install Without Breaking the Desktop"
date: 2026-05-08
author: unattributed
categories: [linux, parrot-os, sysadmin, infrastructure]
tags: [parrot-os, debian, kde, plasma, nvidia, systemd, lightdm, ntpsec, diagnostics]
---

A fresh Linux install should not be treated as healthy just because it reaches the desktop.

That is especially true on security-focused distributions such as Parrot OS, Kali, or other Debian-derived workstations where the default package set includes penetration testing tools, legacy daemons, wireless tooling, tunneling utilities, display manager integrations, and proprietary GPU drivers.

This post walks through a real Parrot OS 7.x cleanup on a hybrid Intel and NVIDIA laptop running KDE Plasma on X11. The system would usually boot and log in, but one reboot produced a blank black screen after login. That is the kind of failure that should not be fixed by guessing.

The useful method was simple:

1. Create a working directory.
2. Collect one diagnostic file at a time.
3. Change only one thing at a time.
4. Reboot when the change affects boot or login.
5. Verify the warning is gone before moving to the next one.
6. Stop when the system is clean enough, not when every cosmetic warning has disappeared.

The goal was not to make the logs silent. The goal was to remove actionable problems without damaging a working desktop.

* * *

## Starting Point

The system was a freshly installed Parrot OS 7.x workstation with KDE Plasma.

The main symptoms were:

- Intermittent blank screen after graphical login.
- KDE Plasma running under LightDM.
- NVIDIA proprietary driver present on a hybrid Intel plus NVIDIA laptop.
- Repeated boot warnings in `dmesg` and `journalctl`.
- No clear single root cause.

The first rule was to avoid large corrective scripts.

Instead, every step wrote evidence to:

```text
/home/foo/parrot-7x-dmesg-fix/stepNN.txt
````

This made the process auditable. Every change had before and after evidence.

That matters. On a workstation used for security work, a “fix” that cannot be explained is just another configuration drift.

---

## The Diagnostic Pattern

The working pattern looked like this:

```sh
OUT="/home/foo/parrot-7x-dmesg-fix/stepNN.txt" && \
{
  echo "== step NN: description =="
  date -Is
  echo

  echo "== evidence section =="
  command_here 2>&1 || true
  echo

  echo "== failed units =="
  systemctl --failed --no-pager 2>&1 || true
  echo
  systemctl --user --failed --no-pager 2>&1 || true
} | tee "$OUT"

echo "Saved diagnostic output to: $OUT"
```

This pattern has several advantages:

* It captures the exact state at the time of diagnosis.
* It avoids terminal scrollback loss.
* It allows someone else to review the system without guessing.
* It separates evidence from remediation.
* It makes rollback decisions easier.

This is not only useful for Parrot OS. It applies to Debian, Ubuntu, Kali, Mint, and most systemd-based Linux systems.

---

## Finding 1: KDE Plasma Login Needed X11 Stability

The machine was running KDE Plasma with LightDM. Because the original symptom was a blank screen after login, the display stack had to be treated carefully.

The system was kept on Plasma X11 rather than chasing Wayland behavior. After the cleanup, the session remained:

```text
XDG_SESSION_TYPE=x11
XDG_CURRENT_DESKTOP=KDE
DESKTOP_SESSION=plasmax11
```

This matters because NVIDIA hybrid graphics remains more predictable under X11 on many laptops, especially when the internal panel is driven by Intel graphics and NVIDIA is used for PRIME render offload.

The key lesson is not “always use X11.” The lesson is: when stabilizing a new install, reduce variables first. Do not debug KDE, LightDM, NVIDIA, Wayland, PAM, and systemd all at once.

---

## Finding 2: KDE Root Helpers Were Launching With Locale C

One of the recurring warnings came from KDE helper processes launched through system D-Bus and KAuth. The normal user locale was correct, but short-lived privileged KDE helpers were still logging UTF-8 warnings.

The system locale was valid:

```text
LANG=en_CA.UTF-8
System Locale: LANG=en_CA.UTF-8
```

The problem was not that the locale was missing. The issue was that several KDE root helpers were started outside the normal user login environment.

The affected service files were under:

```text
/usr/share/dbus-1/system-services/
```

Examples included:

```text
org.kde.powerdevil.discretegpuhelper
org.kde.powerdevil.chargethresholdhelper
org.kde.powerdevil.backlighthelper
org.kde.kded.smart
```

The safe fix was to avoid modifying the package binaries. Instead, root-owned wrapper scripts were placed under:

```text
/usr/local/libexec/kde-kauth-locale/
```

Those wrappers exported the UTF-8 locale and then executed the original helper.

After reboot, the KDE locale warnings were gone.

The lesson: when a warning comes from a privileged helper, do not assume `/etc/environment` or the user shell environment will reach it. Trace the launch path first.

---

## Finding 3: ntpsec Was Healthy, But Missing Its Statistics Directory

`ntpsec` was running and synchronizing time, but it logged:

```text
statistics directory /var/log/ntpsec/ does not exist or is unwriteable
```

The fix was simple:

```sh
sudo install -d -o ntpsec -g ntpsec -m 0755 /var/log/ntpsec
sudo systemctl restart ntpsec.service
```

After reboot, the warning was gone and `ntpsec.service` remained active.

This is a good example of a warning that should be fixed. Time synchronization is infrastructure. On a security workstation, clean time matters for logs, package validation, TLS, Kerberos, VPNs, and incident timelines.

---

## Finding 4: DrKonqi Was Noisy In the LightDM Greeter Context

The logs showed repeated DrKonqi socket warnings.

The important discovery was that this was not an actual application crash. There were no coredumps. The warning was caused by the LightDM greeter user context trying to uphold a user socket that was not supposed to run for a system user.

The problematic behavior came from a global `sockets.target.upholds` symlink for:

```text
drkonqi-coredump-launcher.socket
```

The normal `sockets.target.wants` link was left intact so the real user session could still use DrKonqi.

The cleanup removed only the noisy `upholds` link. After reboot, the repeated warning disappeared, while the real user session still had the DrKonqi socket available.

The lesson: do not disable a crash handler globally just because its logs are noisy. First determine whether it is failing in the real user session or only in a greeter/system context.

---

## Finding 5: GNOME Keyring PAM Warning Was Benign

LightDM logged:

```text
gkr-pam: unable to locate daemon control file
```

At first glance this looks broken. It was not.

The follow-up evidence showed that GNOME Keyring started later in the real user session and the login keyring unlocked correctly.

This was a timing issue during authentication, before the daemon control socket existed.

No change was made.

This is an important point: not every warning deserves a fix. Some warnings are just a record of system startup ordering.

---

## Finding 6: NVIDIA PRIME Worked, But acpid Was Missing

The system had hybrid graphics:

* Intel iGPU was the active desktop renderer.
* NVIDIA RTX 4070 Laptop GPU was available as PRIME offload.
* `nvidia-drm.modeset=1` was active.
* `nvidia-smi` worked.
* NVIDIA offload rendering worked.

The Xorg log, however, showed that the NVIDIA X driver could not connect to `acpid`.

NVIDIA documents that its X driver attempts to connect to the ACPI daemon by default for ACPI events such as AC or battery state and docking events. It uses the default socket path `/var/run/acpid.socket`. ([NVIDIA Download Center][2])

The fix was:

```sh
sudo apt update
sudo apt install -y acpid
sudo systemctl enable --now acpid.service
```

A reboot was required, because Xorg had already started before `acpid` was installed.

After reboot:

```text
/run/acpid.socket
/var/run/acpid.socket
```

both existed, and the NVIDIA Xorg ACPI warning was gone.

The larger NVIDIA DRM warning remained:

```text
WARNING: nvidia-drm/nvidia-drm-drv.c:1226 at nv_drm_revoke_modeset_permission
```

That warning was left alone because the system was logging in successfully, PRIME worked, and the warning appeared during normal Xorg and offload activity. Changing kernel driver parameters at that point would have increased risk.

The lesson: fix missing support services first. Do not change GPU boot parameters until you have evidence that the remaining warning is causing a real failure.

---

## Finding 7: acpid Had a Trivial systemd Environment Warning

After installing `acpid`, systemd logged:

```text
acpid.service: Referenced but unset environment variable evaluates to an empty string: OPTIONS
```

The unit used:

```text
ExecStart=/usr/sbin/acpid $OPTIONS
```

but `/etc/default/acpid` had only:

```text
#OPTIONS=""
```

The fix was simply to define it:

```text
OPTIONS=""
```

After restart and reboot, the warning was gone.

This was not a functional problem. It was configuration hygiene.

---

## Finding 8: Legacy SysV Init Scripts Were Creating Boot Noise

The final class of warnings came from `systemd-sysv-generator`.

The affected packages were:

```text
dns2tcp
ptunnel
stunnel4
isc-dhcp-server
```

The systemd SysV generator creates wrapper `.service` units for legacy scripts in `/etc/init.d/` at boot and daemon reload time. The systemd manual notes that this component is deprecated and recommends replacing remaining SysV init scripts with native unit files. ([man7.org][3])

On this Parrot OS system, these packages were useful security tools, but their daemons were not intended to run by default.

The wrong fix would have been to purge useful tools.

The right fix was to create native systemd units that preserved the current behavior:

* installed
* available
* disabled
* inactive
* not listening
* not started during boot

Native compatibility units were created for:

```text
dns2tcp.service
ptunnel.service
stunnel4.service
isc-dhcp-server.service
```

After reboot, the SysV generator warnings were gone, and all four units remained disabled and inactive.

The final evidence showed:

```text
dns2tcp.service: disabled, inactive
ptunnel.service: disabled, inactive
stunnel4.service: disabled, inactive
isc-dhcp-server.service: disabled, inactive
```

No matching server processes or listeners were started.

This is a practical pattern for security distributions. Many tools are installed for operator use, not because their daemons should run at boot.

---

## Final State

The final health check showed:

```text
0 failed system units
0 failed user units
```

Resolved warning groups:

* KDE UTF-8 locale helper warnings.
* `ntpsec` statistics directory warning.
* `acpid OPTIONS` warning.
* SysV generator warnings.
* DrKonqi repeated `upholds` warning.
* NVIDIA Xorg ACPI warning.

The system retained:

* KDE Plasma on X11.
* LightDM.
* NVIDIA proprietary driver.
* NVIDIA PRIME offload.
* Intel as the default renderer.
* Parrot security tooling packages.
* Disabled and inactive tunnel/DHCP server units.

The remaining warnings were accepted as non-actionable or low priority:

* NVIDIA proprietary module taint.
* NVIDIA DRM permission warning during Xorg/offload.
* LightDM greeter cleanup messages.
* GNOME Keyring timing warning.
* NTP time step during boot.
* firmware-level ACPI timing warning.
* optional desktop integration warnings from WirePlumber, OBEX, or camera discovery.

The system did not need to be made silent. It needed to be made explainable.

---

## Practical Checklist For Other Debian-Based Systems

For a fresh Parrot OS, Kali, Debian, or Ubuntu workstation, I would use this order.

### 1. Capture the current boot

```sh
mkdir -p "$HOME/parrot-7x-dmesg-fix"

journalctl -b -p warning..alert --no-pager > "$HOME/parrot-7x-dmesg-fix/current-boot-warnings.txt"
dmesg --ctime --level=err,warn > "$HOME/parrot-7x-dmesg-fix/current-dmesg-warnings.txt"
systemctl --failed --no-pager > "$HOME/parrot-7x-dmesg-fix/system-failed-units.txt"
systemctl --user --failed --no-pager > "$HOME/parrot-7x-dmesg-fix/user-failed-units.txt"
```

### 2. Confirm the desktop session

```sh
echo "$XDG_SESSION_TYPE"
echo "$XDG_CURRENT_DESKTOP"
echo "$DESKTOP_SESSION"
```

Do this before changing display managers, Wayland/X11 settings, or GPU driver options.

### 3. Check time services

```sh
systemctl status ntpsec.service systemd-timesyncd.service chrony.service --no-pager
timedatectl status
```

Only one time stack should be intentionally active.

### 4. Check GPU state

```sh
lspci -nnk | egrep -A4 -i 'vga|3d|display'
lsmod | egrep 'nvidia|nouveau|i915|xe|drm'
nvidia-smi
xrandr --listproviders
glxinfo -B
```

For NVIDIA PRIME offload:

```sh
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia glxinfo -B
```

### 5. Inspect service warnings before changing them

```sh
journalctl -b -p warning..alert --no-pager
systemctl --failed --no-pager
systemctl --user --failed --no-pager
```

Do not fix everything at once.

### 6. Treat systemd generator warnings as packaging hygiene

If a package has only an `/etc/init.d/` script and no native systemd unit, decide whether the daemon should run.

If it should not run, create a native unit that remains disabled and inactive.

If it should run, create a native unit that explicitly models the intended daemon behavior.

Do not let a legacy init script accidentally decide boot behavior.

---

## Operator Takeaways

The most useful outcome was not any single fix. It was the process.

A noisy fresh install can be cleaned safely if each warning is classified:

1. Functional problem.
2. Security problem.
3. Packaging hygiene.
4. Desktop timing noise.
5. Firmware noise.
6. Expected proprietary driver behavior.

Only the first three usually deserve immediate changes.

For this Parrot OS 7.x workstation, the practical wins were:

* Stable KDE Plasma X11 login.
* Clean failed-unit state.
* Time service cleaned up.
* NVIDIA ACPI support corrected.
* Legacy SysV boot noise removed without uninstalling tools.
* Security tools preserved but kept inactive unless explicitly started.

That is the balance I want on a security workstation: tools available, daemons quiet, boot behavior explicit, and every change backed by evidence.

Published 2026-05-08 on unattributed.blog

```

The operational claims in the post are based on your final step evidence, which showed clean failed units, resolved warning checks, active `acpid` and `ntpsec`, disabled inactive compatibility units, and working Intel plus NVIDIA PRIME state. :contentReference[oaicite:3]{index=3}
::contentReference[oaicite:4]{index=4}
```

[1]: https://unattributed.blog/?utm_source=chatgpt.com "unattributed"
[2]: https://download.nvidia.com/XFree86/Linux-x86_64/580.126.09/README/xconfigoptions.html?utm_source=chatgpt.com "Appendix B. X Config Options - Index of / - NVIDIA"
[3]: https://www.man7.org/linux/man-pages/man8/systemd-sysv-generator.8.html?utm_source=chatgpt.com "systemd-sysv-generator(8) - Linux manual page"

