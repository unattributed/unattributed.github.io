---
layout: post
title: "When Cloudflare Sneezes: Lessons From The November 18 Outage For Security Architects"
date: 2025-11-19
author: unattributed
categories: [internet-resilience, incident-response, third-party-risk, cloudflare]
tags: [cloudflare, outage-analysis, bot-management, clickhouse, third-party-risk, sres, zero-trust, cdn, supply-chain, resilience]
---

# When Cloudflare Sneezes: Lessons From The November 18 Outage For Security Architects

*A security practitioner’s view on what the November 18 Cloudflare outage really tells us about our dependencies, resilience patterns, and threat models.*

On 18 November 2025, a configuration and software failure inside Cloudflare took large parts of the internet offline for several hours. Cloudflare’s own postmortem attributes the incident to a bug in the generation of a Bot Management feature file, triggered by a change in ClickHouse permissions, that pushed a feature list past a hard coded limit and caused the core proxy software to panic across their global network. :contentReference[oaicite:0]{index=0}  

Independent telemetry from Cisco ThousandEyes observed that network paths to Cloudflare’s edge remained healthy while HTTP 5xx errors and timeouts spiked, which strongly supports Cloudflare’s narrative that this was an application and configuration issue rather than a routing, BGP, or volumetric DDoS problem. :contentReference[oaicite:1]{index=1}  

The blast radius was not theoretical. Wire services and global media report that platforms such as X, ChatGPT, Claude, Spotify, League of Legends, Shopify, Canva, Discord, Coinbase, and even public transit systems like New Jersey Transit and France’s SNCF were degraded or unavailable, along with financial and regulatory organisations including the UK FCA and MI5. Estimates vary, but multiple outlets place Cloudflare in front of roughly one fifth of all websites on the public internet. :contentReference[oaicite:2]{index=2}  

This article:

- Summarises what actually failed inside Cloudflare using their own postmortem as the primary source  
- Integrates independent outage telemetry and reporting to understand global impact  
- Extracts concrete engineering and governance lessons that Cloudflare, and the rest of us, should internalise  
- Translates those lessons into questions and checklists you can turn on your own organisation and your vendors  

Structurally, this piece follows the same long form, practitioner focused format used in my earlier AI security guides on this site. :contentReference[oaicite:3]{index=3}  

---

## 1. What Actually Happened Inside Cloudflare

Cloudflare’s official postmortem describes a failure chain that is simple on paper and brutal in practice. :contentReference[oaicite:4]{index=4}  

1. A permissions change in ClickHouse, used as an analytics back end, allowed a query against `system.columns` to see more schema data than before, including columns from multiple databases instead of just the intended one.  
2. The job that generates a Bot Management feature file did not filter by database, so it suddenly saw duplicated columns and produced a much larger feature file than expected.  
3. The Rust based FL2 proxy had a hard coded limit on the number of supported bot features (200). The newly generated file exceeded that limit.  
4. The code that parsed the file used `unwrap` style error handling on the result and panicked when the limit was exceeded.  
5. Because this feature file was distributed at regular intervals across the network, more and more proxies began to ingest the bad file and crash when processing bot features, producing HTTP 5xx responses for customer traffic.  
6. Older FL engines handled similar conditions more defensively by degrading bot scores rather than crashing the proxy. The new path did not.  
7. Observability and error reporting code amplified the pain by consuming CPU while trying to capture diagnostic context for the flood of panics.  

From the outside, ThousandEyes saw a clean network path to Cloudflare with elevated 5xx and timeouts at the application layer, exactly what you would expect when the proxy tier is repeatedly ingesting invalid configuration and panicking. :contentReference[oaicite:5]{index=5}  

The net result was a failure of Cloudflare’s own control and data plane that manifested as HTTP 5xx responses and timeouts for a very large fraction of internet services that transit their edge.

---

## 2. Global Blast Radius And Systemic Risk

The useful part of the media coverage is not the headline “half the internet went down”, it is the concrete sectors and systems that were affected.  

- **Core platforms and communication**  
  - X, Facebook properties in some regions, Discord, and other social platforms saw significant disruption. :contentReference[oaicite:6]{index=6}  
- **AI and developer ecosystems**  
  - ChatGPT and other OpenAI services, Anthropic, and associated tooling were intermittently inaccessible, which cascaded into development workflows and incident response itself because many teams now rely on these tools for operations. :contentReference[oaicite:7]{index=7}  
- **Commerce and finance**  
  - Shopify, Home Depot’s earnings webcast, Moody’s, payment and retail sites in Europe, and multiple national transit operators experienced visible impact. :contentReference[oaicite:8]{index=8}  
- **Public sector and critical institutions**  
  - UK FCA, MI5, and other organisations fronted by Cloudflare reported disruption, alongside city and national emergency management agencies that rely on Cloudflare based properties. :contentReference[oaicite:9]{index=9}  

Two themes matter for security architects:

1. **Cloudflare is effectively critical infrastructure**  
   Regardless of your view of the exact percentage, the combination of Cloudflare’s own numbers and independent estimates makes it clear that a small number of providers can materially affect the operational integrity of large chunks of the public internet. :contentReference[oaicite:10]{index=10}  

2. **The failure mode was not exotic**  
   This was not a BGP hijack, a massive volumetric DDoS, or some obscure kernel bug. It was a config generation bug, a schema assumption, and an unsafe error handling pattern in a feature module. Exactly the sort of thing every large platform has lurking somewhere in its estate. :contentReference[oaicite:11]{index=11}  

This is what makes the incident so relevant. If a feature file in a single module can create a systemic internet event, you cannot treat such modules as “just another config consumer”.

---

## 3. Lessons Cloudflare Should Learn (And The Rest Of Us Too)

This section embeds, in full, the core lessons we extracted earlier, with light editing for narrative flow.

### 3.1 Treat Internal Configuration Like Untrusted Input

The root cause was a ClickHouse permission change that caused a query to return duplicated columns. That bloated a Bot Management feature file, which then broke the proxy when it exceeded a hard coded feature limit. :contentReference[oaicite:12]{index=12}  

Cloudflare’s own write up explicitly states that they will harden ingestion of Cloudflare generated configuration files “in the same way we would for user generated input”. :contentReference[oaicite:13]{index=13}  

**Lesson:** internal data products are not inherently safe.

For Cloudflare and any large platform, that means:

- Strict schema validation and bounds checks (feature count, file size, value ranges) for generated configs  
- Automatic rejection and rollback when a new config fails validation  
- Staged propagation with health checks before global rollout  

If you auto generate and globally distribute anything that can affect the data plane, you must treat it as hostile until proven valid at each hop.

---

### 3.2 Make Optional Features Fail Open, Not Fail Hard

The failure came from the Bot Management module. A bigger than expected feature file hit a limit and triggered a panic in the FL2 Rust code, which in turn produced HTTP 5xx errors on the core proxy. :contentReference[oaicite:14]{index=14}  

The previous generation FL proxy apparently degraded more gracefully, defaulting to neutral bot scores and continuing to serve traffic.

**Lesson:** optional controls should not have catastrophic failure modes.

Specifically:

- If Bot Management, WAF custom features, or similar modules fail, the fallback should be a safe default (for example treat as “unknown, probably human” with conservative rate limits) while the HTTP path continues to function  
- Proxies should ignore or trim invalid or excessive feature definitions and continue using the last good configuration instead of panicking  
- Errors must be visible in telemetry and alerting, but must not be allowed to tear down the process that serves traffic  

The security community often obsesses over “fail closed”. At internet scale, you need a more nuanced discussion about which features can fail closed and which must degrade.

---

### 3.3 Remove Panics And Unsafe Assumptions From Critical Path Code

In the core data path, Cloudflare’s FL2 proxy used an `unwrap` style assumption on the feature file parsing result. When the feature list blew past the hard limit, that assumption failed and the proxy panicked.

**Lesson:** in a global edge proxy, nothing that depends on external configuration or dynamic data should be treated as infallible.

The engineering discipline here is boring and essential:

- Systematically hunt down `unwrap` and equivalent patterns in critical path modules and replace them with explicit error handling  
- For every failure case, explicitly design: “What does the proxy do now, and does HTTP still work”  
- Cap lists and ignore extras instead of panicking  
- Quarantine bad nodes as a last resort, but never crash the only process that can answer requests  

Rust is not magic. You can write brittle systems in any language if you assert instead of handling error conditions.

---

### 3.4 Design Configuration Distribution To Limit Blast Radius

The bad configuration file was generated every few minutes and distributed widely. During partial rollout, some nodes used a good file and some a bad one, which created a confusing pattern of intermittent failures. As more nodes received the bad file, the system converged to a stable but broken state. :contentReference[oaicite:15]{index=15}  

**Lesson:** configuration distribution is a safety critical system.

For Cloudflare and similar providers, that implies:

- Strict canarying per region or per POP, with automatic rollback when error rates cross pre defined thresholds  
- Positive health signals from canaries (for example error budgets, latency, resource usage) before rollout continues  
- A global “freeze” capability that can pin all nodes to the last known good configuration with a single control action  
- Transparent visibility into which version of which config is deployed where, so SRE and security teams can correlate behaviour in real time  

Many organisations already do this for code, but treat config as a second class citizen. This outage shows that configuration changes can be more dangerous than software deploys.

---

### 3.5 Strengthen Change Management Around Shared Infrastructure

The initial change was made to improve ClickHouse permissions so users could see metadata for underlying tables. That change was reasonable on its own, but it broke an unwritten contract in a downstream query that generated the Bot Management feature file. :contentReference[oaicite:16]{index=16}  

**Lesson:** queries used in critical paths should be treated as APIs, not ad hoc SQL.

Events like this usually mean:

- Central data platform teams must maintain a catalogue of “contract queries” that serve other systems, with tests that guard their shape and semantics  
- Any change to system tables, permission models, or query semantics must trigger dependent test suites  
- There must be a formal sign off process for changes to shared infra where impact on consuming systems is examined with engineers from both sides of the dependency  

If you own a central database, you own part of the availability story of every downstream system that depends on it.

---

### 3.6 Build Better Kill Switches And Bypasses

Cloudflare notes that one of their follow up actions is enabling more global kill switches for features. During the incident they created bypasses for internal services such as Workers KV and Access to minimise impact. :contentReference[oaicite:17]{index=17}  

**Lesson:** kill switches and bypass paths are first class resilience features, not nice to haves.

In practice:

- Every major module (Bot Management, WAF, Workers KV fronting, Access, etc) should have a well defined kill switch that can be flipped quickly from a stable control plane  
- Those switches should not depend on the failing subsystem they are trying to disable  
- There should be alternate paths for internal traffic, so SREs and security engineers can still reach dashboards, status pages, and emergency tooling when the main proxy is degraded  

If you have never rehearsed using a kill switch, it probably will not work when you need it.

---

### 3.7 Isolate Observability From The Data Plane And Cap Its Resource Use

During the outage, error reporting and diagnostic systems consumed significant CPU as they tried to enhance uncaught errors with additional context. That extra load made the situation worse on already stressed proxies. :contentReference[oaicite:18]{index=18}  

**Lesson:** observability systems must be good citizens under failure conditions.

That requires:

- Hard budgets on how much CPU, memory, and I/O error reporting and tracing are allowed to consume on hot paths  
- Automatic downshifting to sampling or reduced verbosity when error volume spikes  
- Off loading expensive capture and processing to sidecars or out of band workers that cannot take down the data plane  

Telemetry that becomes a denial of service is a very expensive way to learn that you over instrumented your core services.

---

### 3.8 Improve Incident Triage And Hypothesis Discipline

Cloudflare’s own narrative and public commentary indicate that the first instinct of many observers was to suspect a large scale DDoS or coordinated attack, especially because Cloudflare’s externally hosted status page also experienced issues around the same time. :contentReference[oaicite:19]{index=19}  

**Lesson:** incident triage must explicitly guard against narrative lock in.

For Cloudflare and for your own incident response runbooks:

- Always run at least two investigation tracks in parallel: one focused on internal change and regression, one on external attack hypotheses  
- Ensure your incident tooling surfaces “what changed” on shared infra (databases, config generation jobs, permission models) in the time window leading into the incident  
- Teach incident commanders to treat “probably a DDoS” as a working hypothesis, not a conclusion  

Most large outages come from inside the house.

---

### 3.9 Reconsider Dependency Graphs Between Internal Services

Multiple Cloudflare internal and customer facing services were affected because they all depended on the same failing proxy path: core CDN and security, Workers KV, Access, Turnstile, parts of the dashboard, and email security. :contentReference[oaicite:20]{index=20}  

**Lesson:** you cannot put everything on one critical path and then be surprised when its failure is devastating.

Concrete actions:

- Map which internal services truly need to go through the same data plane and which can have independent ingress  
- Ensure that the control plane you need for emergency changes (status pages, internal dashboards, break glass tooling) does not share the exact same failure domain as the main proxy  
- Consider offering “degraded mode” bypass options for customers, where some features are disabled but core HTTP delivery stays up even when the full feature stack is in trouble  

If your incident tooling relies on the component that is on fire, you need a different incident tooling design.

---

### 3.10 Institutionalise Failure Mode Reviews Across All Modules

Cloudflare explicitly commits to reviewing failure modes for all core proxy modules. That is the right instinct and it should become an ongoing engineering ritual, not a one off. :contentReference[oaicite:21]{index=21}  

**Lesson:** treat failure mode and effects analysis as part of the development lifecycle.

For each module:

- Ask “what happens to HTTP traffic if this module returns garbage”  
- Decide whether the correct behaviour is to degrade, bypass, or fail closed, and then test those paths  
- Include malformed, missing, oversized, and adversarial configurations in automated test suites  

The boring work you do here is what prevents the interesting headlines later.

---

## 4. What This Outage Tells Security Teams About Their Own Risk

It is tempting to file this incident under “Cloudflare’s problem”. For security architects and adversarial minded defenders, it is more useful to treat it as a free tabletop exercise in third party dependency risk.

A few practical observations, anchored in the public reporting and Cloudflare’s own account: :contentReference[oaicite:22]{index=22}  

1. **Single vendor dependency is now a systemic threat vector**  
   If your primary external facing surfaces are fronted by a single CDN or security provider, an internal config error at that provider can be as impactful as a successful attack on your own infrastructure.  

2. **Resilience and security are entangled**  
   For a few hours, incident response for many organisations was constrained because their primary communication and coordination platforms (chat, email, issue tracking, AI assistants) were impacted by the same event. That is a security problem, not just an availability problem.  

3. **Supply chain risk is not only software and hardware**  
   Most supply chain conversations in security focus on libraries, firmware, and vendors that ship code. The November 18 outage is a reminder that service level dependencies (CDNs, DDoS protection, AI providers, status page vendors) belong on the same risk register.  

4. **Threat modelling needs to include “latent bug in provider” as a scenario**  
   You cannot patch Cloudflare’s code, but you can design for its failure. That means explicitly modelling “provider outage” and “provider misconfiguration that breaks but does not fully erase traffic” as scenarios when you design critical paths.

---

## 5. Turning This Into Actionable Questions

Here are concrete questions you can ask of your own stack and of Cloudflare or any similar provider.

### 5.1 Questions For Your Own Architecture

- How many critical external services (customer portals, APIs, SSO, email, incident tooling) share the same CDN or edge provider?  
- For each of those services, what actually happens if that provider:
  - Returns only 5xx for 2 to 4 hours  
  - Intermittently fails (for example 30 percent error rate)  
  - Serves stale or partial content  
- Which of your internal systems (dashboards, VPN, IdP, status pages, remote access) depend on the same edge provider?  
- Do you have an architectural pattern for “feature can fail, HTTP must not”, and is it enforced by code review and testing?  
- Do your own config generation systems have:
  - Strong validation  
  - Canary rollout  
  - A global freeze button  
- Have you ever tested failure modes where observability is partially or fully disabled to preserve the data plane?

### 5.2 Questions For Cloudflare And Other Providers

Cloudflare’s postmortem already lists remediation items, but as a customer or assessor you should be asking:

- How are you hardening configuration ingestion for internally generated files, especially for security features such as Bot Management and WAF custom rules? :contentReference[oaicite:23]{index=23}  
- What is your policy on panics and fatal errors in core proxy code paths, and how are you enforcing it?  
- Which global kill switches and bypasses exist, how are they controlled, and how often are they exercised in drills? :contentReference[oaicite:24]{index=24}  
- What guarantees do you provide about staged rollout of configuration changes and associated blast radius control?  
- How do you ensure that changes to shared infra components (for example ClickHouse permissions, system tables) are tested against downstream consumers?  
- How is your observability stack isolated from the data plane, and what automatic downshifts exist under error storms? :contentReference[oaicite:25]{index=25}  

Well run providers will either have good answers to these questions or will welcome them as pressure that justifies internal investment.

---

## 6. A Practical Checklist For Security And Resilience Teams

You can use the following checklist as a starting point for internal reviews and vendor assessments.

### Architecture And Dependency Mapping

- [ ] Maintain an up to date map of which external services depend on which CDN and security providers  
- [ ] Identify truly critical user journeys and APIs and note which depend on Cloudflare or equivalent providers  
- [ ] Ensure critical internal tooling for incident response and access control has a different failure domain from primary customer traffic  

### Config And Change Management

- [ ] Treat all auto generated configuration as untrusted until validated  
- [ ] Require schema, size, and semantic validation for all config that can affect the data plane  
- [ ] Enforce canary rollout with health based gating for both code and config  
- [ ] Implement a global freeze mechanism for configuration distribution  

### Failure Mode Engineering

- [ ] Classify modules as “must fail closed” or “must degrade” and implement behaviour accordingly  
- [ ] Eliminate panics and unchecked assumptions from core request handling paths  
- [ ] Test behaviour under oversized, malformed, and missing configuration inputs  
- [ ] Constrain observability resource usage and implement sampling under extreme error conditions  

### Third Party And Vendor Risk

- [ ] Include CDN and security providers explicitly in third party risk registers  
- [ ] Integrate Cloudflare (or equivalent) outage scenarios into business continuity and DR plans  
- [ ] Regularly review provider postmortems and compare their remediation items to your own expectations and contracts  

---

You are right, that section was too thin for your audience. Here is a rewritten **Section 7. Further Reading** you can drop in to replace the old one. It keeps your blog’s style and focuses on authoritative, citable sources.

```markdown
## 7. Further Reading

For security architects and SRE teams, it is worth going beyond headlines and reading the primary technical accounts and high quality secondary analyses. The references below are grouped by type so you can decide how deep you want to go.

### 7.1 Primary technical sources

- **Cloudflare incident write up**  
  Cloudflare’s own postmortem is the authoritative source on root cause, internal timeline, and planned remediation. It details the ClickHouse permission change, the Bot Management feature file bloat, the FL2 panic behaviour, and the configuration rollout model that amplified the impact. :contentReference[oaicite:0]{index=0}  

- **Cloudflare status history**  
  The incident entries on `cloudflarestatus.com` provide the operational timeline, customer facing impact descriptions, and recovery milestones. Useful for correlating with your own logs and for SLA/contract discussions. :contentReference[oaicite:1]{index=1}  

### 7.2 Independent network-measurement and outage analysis

- **Cisco ThousandEyes: “Cloudflare Outage Analysis: November 18, 2025”**  
  A measurement driven view of the outage, showing that network paths to Cloudflare’s edge remained healthy while timeouts and HTTP 5xx errors spiked, which supports the conclusion that this was a backend and configuration issue rather than a routing or volumetric DDoS event. :contentReference[oaicite:2]{index=2}  

- **ThousandEyes Internet Outage Map**  
  A useful companion to the Cloudflare specific post, providing cross provider context and comparisons to other recent cloud and CDN incidents (Azure Front Door, AWS, Starlink, and others). :contentReference[oaicite:3]{index=3}  

### 7.3 High quality news and context

- **Reuters business coverage**  
  Concise framing of scale and impact, including Downdetector statistics, the list of high profile affected platforms (X, ChatGPT, Canva, Grindr), and the estimate that Cloudflare fronts roughly 20 percent of the web. Useful for executive briefings and third party risk registers. :contentReference[oaicite:4]{index=4}  

- **Financial Times analysis**  
  Emphasises the role of an oversized bot management configuration file and lists specific institutional impact (IKEA, FCA, MI5, Home Depot’s earnings webcast). Highlights market reaction and positions Cloudflare clearly as critical internet infrastructure. :contentReference[oaicite:5]{index=5}  

- **The Guardian and ABC News explainers**  
  Provide readable summaries of what Cloudflare is, why the outage cascaded across sectors, and how quickly Cloudflare implemented a fix. These are useful to share with non technical stakeholders while keeping the narrative reasonably accurate. :contentReference[oaicite:6]{index=6}  

- **Associated Press / WCVB and other wire reports**  
  Short, edited reports that emphasise that the incident was not a cyberattack but an internal “latent bug” triggered by a routine configuration change. Good for reinforcing the “most large outages come from inside” lesson in governance and board discussions. :contentReference[oaicite:7]{index=7}  

### 7.4 Sector-specific impact and second order effects

- **Forbes, Computing, and other specialist outlets**  
  These pieces focus on the fragility of global internet infrastructure and catalogue the breadth of affected platforms (X, Zoom, ChatGPT, Shopify, payment providers, transit operators). They are useful when you want to illustrate systemic dependency in risk assessments and BCP/DR workshops. :contentReference[oaicite:8]{index=8}  

- **Customer postmortems (for example, Resend)**  
  Some downstream providers have already published their own incident reports describing how the Cloudflare outage affected their services and what they are changing in response. These are excellent case studies in how a single provider failure propagates through the service supply chain. :contentReference[oaicite:9]{index=9}  

Taken together, these sources give you three complementary views of the event:

1. Cloudflare’s internal reality (root cause, timeline, remediation)  
2. Independent network telemetry (what the internet actually saw)  
3. Sector and customer impact (what broke for users and how it is being framed)

If you are responsible for third party risk, incident response, or internet facing architecture, reading at least one item from each category is time well spent.