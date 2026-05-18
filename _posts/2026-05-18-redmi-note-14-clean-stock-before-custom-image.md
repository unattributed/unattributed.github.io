---
layout: post
title: "Why I Chose Clean Stock Before a Custom Android Image"
date: 2026-05-18
author: unattributed
categories: [android, mobile-security, rom-development, security-engineering]
tags: [android, redmi-note-14-5g, citrine, hyperos, aosp, custom-rom, mobile-security, clean-stock, bootloader, avb]
---

## Why I Chose Clean Stock Before a Custom Android Image

The original goal sounded simple: take a Redmi Note 14 5G and replace the vendor-heavy Android experience with something closer to vanilla Android.

That is still the long-term research direction.

I am continuing to investigate and test whether a proper custom image, AOSP-style build, Lineage-style build, GSI path, or device-specific ROM path can be made safe and repeatable for this device. At this stage, however, I chose not to flash a custom image. I chose the more conservative path: keep stock HyperOS, keep the bootloader locked, keep verified boot green, and remove or disable enough launcher-visible OEM software to make the phone as close to clean stock Android as I can without crossing the wrong safety boundary.

That decision was not a retreat from the project. It was the first mature result of the project.

This post explains the process, the decision making, and the challenges behind that choice.

* * *

## The Starting Point

The device is a Redmi Note 14 5G, codename `citrine`, with Xiaomi firmware naming observed as `beryl` and `beryl_dc`. The platform is MediaTek MT6855. The current stock operating system observed during the project is HyperOS 3.0 on Android 16.

The practical problem was familiar to anyone who has used modern OEM Android builds.

The phone worked, but the software experience was not clean. It included Xiaomi and MIUI applications, promotional surfaces, recommendation paths, analytics-oriented components, and OEM apps that did not fit the intended daily-driver model.

The first instinct was to remove the vendor image entirely and replace it with a clean Android build. That is an attractive idea, but on a single physical phone it carries real risk.

This was not a spare lab handset with unlimited recovery options. It was one device. If the bootloader unlock, flash, rollback, or relock path failed, the project could lose the only test platform. Worse, a partially working custom ROM would not meet the actual goal. A phone that boots but loses camera quality, modem behavior, emergency reliability, banking app compatibility, Play services behavior, or update trust is not a successful outcome.

The project therefore needed a security engineering process, not a flashing adventure.

* * *

## The Real Goal Was Not "Install AOSP"

The real goal was a usable, lower-noise, lower-bloat Android phone that preserved the properties that matter in daily life.

That meant the success criteria were broader than a boot animation.

A successful phone needed to preserve:

- normal boot behavior,
- working touchscreen and launcher,
- mobile data and Wi-Fi,
- telephony and SMS,
- camera behavior,
- Play Store access,
- Play services behavior,
- default browser, phone, messaging, and assistant roles,
- reasonable Play Protect and device trust posture,
- a clear rollback path,
- no unnecessary exposure of private device identifiers,
- and no irreversible change unless the evidence justified it.

For a cybersecurity audience, the important point is this: device integrity is a security property. A cleaner user interface is not worth much if the path to get there destroys trusted boot state, breaks rollback confidence, or replaces an understood vendor risk with an unverified supply-chain risk.

* * *

## The Repository Became an Evidence System

The project quickly became a documentation and evidence project before it became a modification project.

The repository was structured around device profile, firmware recovery, partition analysis, bootchain and AVB notes, GSI readiness, kernel-source research, decision records, runbooks, evidence indexes, risk registers, and clean-stock feasibility work.

That structure mattered because every major decision needed to answer the same question:

**What evidence would make this action safe enough to take on the only device available?**

The project rule was simple: do not unlock, flash, downgrade, erase userdata, install DSU, sideload Google applications, execute Xiaomi flash scripts, relock, or modify system images unless a later decision record explicitly approves it.

That rule sounds restrictive, but it kept the project honest.

* * *

## Track 1: Recovery Had to Come First

Before any custom ROM path could be considered, the project needed to know whether the phone could be returned to stock.

The recovery work documented stock fastboot ROM evidence, checksums, fastboot access, ADB access, the anti-rollback value, flash-script anatomy, image inventory, and dry-run rollback readiness.

That was useful progress, but it did not prove complete recovery.

The following remained unproven:

- actual full reflash,
- hard-brick recovery,
- recovery if fastboot is unavailable,
- MediaTek authenticated service-tool recovery,
- safe relock after modification.

That was enough to block destructive work.

A rollback plan that has been studied but never executed is not the same as a proven recovery path. In a lab with multiple devices, that risk might be acceptable. On one physical daily-driver candidate, it was not.

* * *

## Track 2: Custom ROM Research Was Useful, But Not Yet Sufficient

The custom ROM track investigated GSI, DSU, Halcyon, and AlphaDroid-style options.

The device had several encouraging technical signs. It supported Treble. It used dynamic partitions. It used virtual A/B. Fastboot and ADB access were available for read-only investigation. The system had the architectural shape of a modern Android device that might eventually support a clean custom path.

But architectural possibility is not the same thing as operational readiness.

DSU and GSI research did not produce a safely exposed, low-risk installation path that I was willing to use on the only device. Dynamic System Updates looked present at a component level, but the available path was not clean enough to justify a test that could compromise the daily-driver state.

The custom ROM candidates also did not clear the evidence bar.

Halcyon was investigated, but source retrieval and review hit practical blockers. AlphaDroid became the strongest reachable candidate lead, but its public release integrity and functional phone evidence were not strong enough to justify bootloader unlock.

The problem was not merely whether a build existed. The questions were stricter:

- Is there credible device-specific source evidence?
- Is there clear release integrity evidence?
- Is the artifact provenance understandable?
- Does the build support a functional phone, not just a booting device?
- Are modem, camera, audio, sensors, calls, SMS, and mobile data known to work?
- Does Google Play services behavior remain acceptable for the intended use?
- Is there a documented rollback route if the first boot fails?
- Is the maintainer or release process trustworthy enough for a phone used in real life?

The answer was not strong enough.

The correct decision was no-go for bootloader unlock and no-go for flashing.

* * *

## The Key Decision: A Functional Phone Beats a Booting Image

One of the most important decision records in the project reframed the success criterion.

The goal was not a booting image.

The goal was a functional phone.

That distinction matters because custom ROM communities often treat "boots" as a major milestone. It is a milestone, but it is not enough for this use case. A phone can boot and still fail as a daily driver. It can boot without reliable camera behavior. It can boot while losing trusted app compatibility. It can boot with broken modem behavior. It can boot with a poor rollback story.

For this project, a successful custom image would need to prove more than the operating system starting. It would need to prove that the device remains a phone.

That single distinction changed the direction of the work.

* * *

## Track 3: Clean Stock Became the Practical Path

The clean-stock path preserved the stock vendor image, modem stack, camera stack, Google Play Store, Google Play services, Google Services Framework, WebView, Play Protect behavior, and locked bootloader posture.

Instead of modifying partitions or replacing the system image, the clean-stock path used Android package state for user `0`.

That means unwanted packages could be removed or disabled for the primary Android user without deleting them from the read-only system image. The restore model stayed simple: document the restore command before running the removal command.

The core restore pattern was:

```text
adb shell cmd package install-existing --user 0 PACKAGE_NAME
```

For packages that resisted user-level uninstall but could be disabled for user `0`, the restore pattern was:

```text
adb shell pm enable --user 0 PACKAGE_NAME
```

This was not as pure as flashing a clean AOSP image, but it was safer, testable, and reversible.

* * *

## Package Cleanup Was Treated as a Risk-Control Exercise

The project did not start by removing everything with a Xiaomi or MIUI prefix.

That would have been reckless.

The package inventory classified 102 Xiaomi or MIUI packages. Of those, 46 were preserved by default, 14 were marked as review-only cleanup candidates, and 42 remained unknown and required manual review.

That classification was important because many OEM packages are ugly from a user-interface perspective but still connected to framework behavior, accounts, permissions, telephony, power management, camera behavior, media, system UI, package installation, security services, or trust behavior.

The clean-stock rule was therefore conservative:

- preserve core system behavior,
- remove only optional user-facing or promotional targets after review,
- never touch security center by default,
- avoid launcher, package installer, permission controller, WebView, Play Store, Play services, Google Services Framework, telephony, IMS, modem, camera, audio, sensors, location, thermal, and trust components,
- define the restore command before removal,
- test after each small change,
- stop when the desired visible result is achieved.

That last point matters. The goal was not to make the package list ideologically pure. The goal was to make the phone clean enough while keeping the risk low.

* * *

## Clean Stock Milestone 1

Clean Stock Milestone 1 reached the practical target.

The phone remained on stock HyperOS. The bootloader remained locked. Verified boot remained in the expected locked and green posture. No flashing, downgrade, userdata erase, DSU installation, Google app sideloading, Xiaomi flash script execution, relock, or system-image modification occurred.

Optional OEM launcher-visible applications were removed or disabled for Android user `0`. The main cleanup targets were no longer launcher-visible. Four resistant applications remained installed but were disabled for user `0`:

```text
com.miui.calculator
com.miui.compass
com.miui.notes
com.xiaomi.scanner
```

The remaining visible OEM-looking launcher package was the Themes application. That was treated separately because themes, wallpapers, icons, lock-screen appearance, and launcher behavior are tied to user-interface state in ways that should not be casually broken.

The project also intentionally retained `com.miui.securitycenter`. That was the right decision. Removing something because it has an OEM label is not security engineering. Security center and related Xiaomi framework packages may affect permission behavior, app scanning, device management, and other platform integrations. Without deeper proof, preserving it was safer.

After reboot, the phone remained functional in normal use.

* * *

## Moving Toward a Pixel-Like Default App Model

A clean phone is not just fewer icons. Default handlers matter.

After the cleanup, the phone was validated with a more Google-oriented default app model:

```text
android.app.role.DIALER: com.google.android.dialer
android.app.role.SMS: com.google.android.apps.messaging
android.app.role.BROWSER: com.android.chrome
android.app.role.ASSISTANT: com.google.android.googlequicksearchbox
android.app.role.HOME: com.miui.home
```

Direct intent checks confirmed that phone, SMS, and web intents resolved to Google Phone, Google Messages, and Chrome. The Google app was recorded as the assistant role holder, although direct ASSIST intent behavior remained device-specific and should not be overstated.

MIUI Home remained the launcher because replacing the launcher was not required to reach the milestone, and launcher instability is one of the easiest ways to turn a cosmetic cleanup into a usability problem.

The result is not a Pixel ROM. It should not be described that way.

It is better described as stock HyperOS with a cleaner user-facing profile and Google-oriented default roles where supported.

* * *

## Publication Safety Was Part of the Engineering Work

Because this work may be useful to other people, I also created a sanitized public repository path.

That required a separate safety boundary.

The public mirror can include project documentation, decision records, sanitized runbooks, helper scripts, restore scripts, small non-secret evidence summaries, and technical notes.

It must not include firmware archives, extracted firmware images, raw super images, private evidence directories, full `getprop` output, full `fastboot getvar all` output, IMEI values, serials, MAC addresses, SIM identifiers, account identifiers, or private user data.

That distinction matters. Publishing a mobile-device research project without a privacy boundary can leak more than people expect.

The public repository exists to make the process reviewable, not to publish private device evidence.

* * *

## Why I Did Not Unlock the Bootloader

The bootloader unlock decision is where enthusiasm usually collides with reality.

Unlocking would reduce device security, likely wipe data, change the trust posture, and create a recovery burden. It could also affect warranty or service expectations, and for HyperOS-era Xiaomi devices the unlock path is account-bound and process-bound.

None of that makes unlocking inherently wrong.

It does mean unlocking should have a reason strong enough to justify the risk.

At this stage, the custom image track did not clear that bar. Backup readiness was not fully complete. End-to-end stock reflash was not proven. The custom ROM candidates did not provide enough public functional evidence. Release-integrity confidence was incomplete. The first post-unlock target was not strong enough to justify a destructive state change.

So the answer was no.

Not no forever. No for now.

* * *

## The Hardest Challenge Was Restraint

The most difficult part of this project was not running ADB commands.

The hard part was resisting the temptation to do the exciting thing before the boring prerequisites were complete.

A custom ROM sounds more impressive than user-level package cleanup. It is also easier to explain in a headline. But security engineering is not measured by how dramatic the change looks. It is measured by whether the change improves the system while preserving the properties that matter.

In this case, the restrained path produced the better result.

The phone is cleaner. The bootloader is still locked. Stock firmware remains intact. The rollback posture is better than it would be after a speculative flash. The system remains daily-driver viable. The project has decision records, risk boundaries, restore tooling, and evidence manifests.

That is real progress.

* * *

## Lessons for Security Professionals

This project reinforced several lessons that apply beyond Android phones.

### 1. Rollback is a security control

A change without a tested rollback path is not just operationally risky. It is a security risk. If recovery depends on assumptions that have never been tested, the system is not under control.

### 2. Trusted boot state is an asset

A locked bootloader and green verified boot state are not cosmetic details. They are part of the device trust model. Giving them up should require a better reason than dissatisfaction with OEM applications.

### 3. "Boots" is not a sufficient acceptance test

A custom image that boots but fails as a phone is not successful. Mobile acceptance criteria must include communications, camera, sensors, app trust, update behavior, recovery, and daily use.

### 4. Supply-chain questions apply to ROMs too

A community ROM is software supply chain. Source availability, maintainer reputation, release integrity, artifact provenance, and reproducibility matter. Flashing an image from an unclear source is not a privacy win just because it looks cleaner.

### 5. Package names are not proof

A package with an OEM name is not automatically safe to remove. A package with a boring name is not automatically harmless. Classification must be tied to function, dependencies, restore behavior, and observed impact.

### 6. Good engineering sometimes means stopping early

The clean-stock track stopped after the practical target was met. Continuing broad cleanup after that would increase risk without a clear benefit.

* * *

## Current State

The current active path is clean-stock HyperOS daily-driver validation.

The operating rule is:

- do not flash,
- do not unlock the bootloader,
- do not downgrade,
- do not erase userdata,
- do not install DSU,
- do not sideload Google applications,
- do not run Xiaomi flash scripts,
- do not relock,
- do not continue broad package cleanup,
- only change packages when a specific observed issue is tied to a package.

The restore tooling is committed. The inventory tooling is committed. The public mirror is sanitized. The project has a safer baseline than it had at the start.

That is a useful place to be.

* * *

## Where the Custom Image Work Goes Next

I have not abandoned the custom image goal.

The custom image path can be reopened if the evidence changes. The evidence bar is clear:

- stronger device-specific source evidence,
- stronger release-integrity evidence,
- credible functional phone proof,
- clear maintainer and artifact provenance,
- documented modem, camera, audio, sensor, telephony, SMS, mobile data, and Play services behavior,
- a better rollback story,
- completed backup readiness,
- and a first post-unlock test target that is worth the risk.

Until then, the clean-stock path is the correct engineering decision.

It gives me most of the user-facing benefit I wanted from a clean image while preserving the device trust and recovery posture that a speculative flash would weaken.

* * *

## Final Thoughts

This project started as a search for a clean Android replacement.

It became a lesson in evidence-based restraint.

For now, the best result is not a custom AOSP image. The best result is a stock HyperOS device with the bootloader locked, verified boot preserved, OEM noise reduced, Google-oriented defaults validated, restore commands prepared, and future custom-image research kept on the evidence track.

That may not sound as exciting as flashing a new ROM.

It is better engineering.

Clean is valuable. Recoverable is valuable. Trustworthy is valuable.

On a single physical phone, the right answer is not the cleanest theoretical image. It is the cleanest state that can be reached without lying about risk.

Repository: https://github.com/unattributed/redmi-note-14-5g-citrine-clean-stock-public
