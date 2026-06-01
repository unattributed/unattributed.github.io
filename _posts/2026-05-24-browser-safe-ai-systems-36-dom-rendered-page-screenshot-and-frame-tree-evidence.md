---
layout: post
title: "Browser-Safe AI Systems, Part 36: DOM, Rendered Page, Screenshot, and Frame-Tree Evidence"
date: 2026-05-24
author: unattributed
categories: [ai-security, browser-security, security-operations, red-team]
tags: [browser-safe-ai, ai-security, browser-security, red-team, adversary-emulation, detection-engineering, llm-security, browser-evidence, playwright]
---

# Browser-Safe AI Systems, Part 36: DOM, Rendered Page, Screenshot, and Frame-Tree Evidence

Part 35 defined how to build safe synthetic browser-AI attack cases.

Once those cases exist, the next question is whether the lab captures the right browser evidence.

A browser-based AI security test cannot rely on a single view of the page. DOM evidence, rendered page evidence, screenshot evidence, and frame-tree evidence are different views of browser state. They can agree. They can also disagree.

Those disagreements are often where the security-relevant behavior appears.

A page can contain source that changes after script execution. A DOM tree can contain content the user never sees. Rendered text can omit layout, visual hierarchy, and QR codes. A screenshot can show visual deception but hide frame origin. A top-level page summary can miss nested frame content. Model context can contain extracted content that differs from both the screenshot and the DOM.

For browser-based AI security testing, this is not trivia.

It is the evidence problem.

Serious browser evidence must be captured, correlated, challenged, and preserved before model interpretation or policy decisions are allowed to claim confidence.

The current test suite implements this as a multi-view evidence discipline. Lab 03 captures hidden DOM and low-visibility evidence with browser source, DOM, visible text, computed style, screenshots, direct HTTP replay, proxied HTTP replay, marker provenance, and model-bound context review. Lab 04 captures DOM/render mismatch evidence. Lab 05 focuses on screenshot and visual-deception evidence. Lab 06 captures iframe and frame-tree evidence, including frame URLs and child-frame DOM snapshots. Lab 07 adds timing and state-transition evidence.

Those labs are still training evidence, not production security validation. Their strength is that they force each claim to point back to artifacts.

## Why Single-View Evidence Fails

Single-view evidence fails because the browser is not a single artifact.

Raw HTML can show what was initially served, but it does not necessarily show what the browser became after script execution, client-side rendering, asynchronous fetches, user interaction, or delayed state changes.

DOM evidence can show script-mutated document state, hidden nodes, attributes, and structural relationships. It does not automatically prove what the user visually perceived.

Rendered text can show user-facing text more directly than raw source. It does not preserve layout, visual hierarchy, brand-like presentation, QR codes, icons, canvas content, or fake dialog styling.

Screenshot evidence can preserve visual state, layout, QR codes, and analyst-reviewable presentation. It does not expose hidden DOM, frame origin, model context, redirect history, or extraction logic.

Frame evidence can show nested browsing contexts. It is often lost when the harness captures only the top-level page. Losing frame evidence can hide where content came from and how it related to the visible page.

Model context may contain extracted content that differs from both visual evidence and DOM evidence. It may omit visible content, include hidden content, collapse frame boundaries, or merge browser-derived text with trusted instructions.

A weak test stores one artifact and writes a conclusion.

A serious test compares evidence views.

A disagreement between evidence views is not noise.

It may be the finding.

## DOM Evidence

DOM evidence captures the browser’s document model.

The [DOM Standard](https://dom.spec.whatwg.org/) defines a platform-neutral model for events and node trees, while [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) describes the DOM as a programming interface for web documents that represents the page so programs can change document structure, style, and content.

For browser-based AI security testing, DOM evidence matters because it can show state that does not exist in raw source and may not appear in a screenshot.

It can show:

* script-mutated nodes
* hidden elements
* attributes
* metadata
* form structure
* injected or rewritten content
* client-rendered content
* node relationships
* content that extraction logic may see even when a user does not

DOM evidence is especially important when testing hidden content influence, model-context contamination, DOM versus rendered mismatch, delayed content, and client-side state changes.

But DOM evidence has limits.

The DOM is not automatically equivalent to what the user saw. A node can exist but be invisible. A value can be present but not displayed. A script can mutate the document after initial capture. A browser extension, automation harness, or accessibility-oriented extraction method may see content differently from the user.

A DOM snapshot should therefore be treated as one evidence view.

Not the whole truth.

## Rendered Page Evidence

Rendered page evidence captures what the page presents as user-facing content.

This may include visible text extraction, computed visibility, accessible text, layout-adjacent text, and other browser-derived representations of what a user could plausibly read.

Rendered text is useful because raw HTML and DOM snapshots can overstate what matters visually. A page may contain many nodes that are hidden, offscreen, collapsed, or irrelevant. Rendered text helps focus on what the browser exposed to the user.

Rendered page evidence helps answer:

* What text was visible?
* What content was likely user-facing?
* Did the visible text match the DOM?
* Did the model context omit visible content?
* Did the model context include content that was not visible?
* Did the user-facing state change after initial load?

Rendered text also has limits.

It does not preserve visual hierarchy. It may flatten the page. It may lose proximity between labels and fields. It may miss QR codes, images, icons, fake dialogs, brand-like styling, and spatial deception. It may not represent canvas-rendered text. It may differ based on viewport, fonts, language support, browser engine, or extraction method.

Rendered text should therefore be captured alongside screenshot evidence, DOM evidence, timing evidence, and frame-tree evidence.

It is useful because it is comparable.

It is weak when treated as complete.

## Screenshot Evidence

Screenshot evidence captures the visible browser state.

Screenshots matter because browser risk is often visual. A screenshot can preserve visual hierarchy, page layout, QR codes, fake dialogs, brand-like presentation, visual spoofing, warning banners, button placement, and page composition.

A screenshot can show what text extraction misses.

It can show whether a QR code was visible. It can show whether a lab-branded page looked like a login, warning, file share, policy notice, or approval workflow. It can show whether visible emphasis changed the security interpretation.

Tools such as [Playwright](https://playwright.dev/docs/screenshots) support page screenshots, including full-page screenshots. [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer) can also support review of recorded browser behavior after a run.

Screenshot evidence is critical for analyst review.

But screenshots are not sufficient.

A screenshot does not show hidden DOM. It does not show frame URLs. It does not show redirect chains. It does not show model context. It may not show offscreen content. It may fail to capture dynamic state if taken at the wrong time. It may show a visual state without explaining where the content came from.

A screenshot is strong when correlated with DOM, rendered text, frame tree, URL metadata, timing records, and model context.

A screenshot alone is a picture.

A correlated screenshot is evidence.

## Frame-Tree Evidence

Frame-tree evidence captures nested browsing context.

Frames matter because modern pages often assemble content from multiple sources, contexts, and nested structures. A top-level page may contain child frames. A child frame may contain the relevant content. A frame may be sandboxed. A frame may have a different URL. A frame may load, change, or fail independently from the parent page.

The [HTML Standard](https://html.spec.whatwg.org/) defines browser document and browsing context behavior, and [Playwright frame documentation](https://playwright.dev/docs/frames) describes how a page can have one or more frame objects, including additional frames attached with the `iframe` HTML tag. The [Playwright Frame API](https://playwright.dev/docs/api/class-frame) also exposes the current frame tree through main frame and child frame relationships.

For browser-based AI security testing, frame-tree evidence helps answer:

* What was the top-level page?
* What child frames existed?
* What URL did each frame load?
* Which frame contained the relevant content?
* Did rendered text come from the parent page or a child frame?
* Did the screenshot show content whose frame origin was not preserved?
* Did the model context collapse frame boundaries?
* Did the report incorrectly treat nested content as top-level content?

Frame-tree evidence should preserve parent and child relationships, per-frame URL, per-frame text when practical, sandbox indicators where available, timing, and whether each frame contributed to model context.

Without frame-tree evidence, a report may know what appeared but not where it came from.

That is not enough.

## Evidence Comparison Matrix

| Evidence View | Shows Well | Misses or Weakens | Required Capture Output | Reviewer Question |
|---|---|---|---|---|
| Raw HTML | Initial source where applicable | Script-mutated DOM, delayed content, rendered state | `raw_html.html` or equivalent source artifact | What did the target initially provide? |
| DOM snapshot | Live document structure, nodes, attributes, hidden content, client-rendered state | Visual hierarchy, user perception, screenshots, frame origin unless captured per frame | `dom_snapshot.html` or structured DOM artifact | What did the browser document become? |
| Rendered text | User-facing text and visible page content | Layout, QR codes, images, icons, spatial deception, canvas content | `rendered_text.txt` or structured visible-text artifact | What text was visible or extractable from rendered state? |
| Screenshot | Visual state, layout, QR codes, visual deception, analyst-reviewable presentation | Hidden DOM, frame origin, redirect chain, model context | `screenshot.png` or equivalent image artifact | What would an analyst see visually? |
| Frame tree | Parent and child frame hierarchy, per-frame URLs, nested context | Visual layout unless paired with screenshots, hidden DOM unless captured per frame | `frame_tree.json` or equivalent frame artifact | Where did each piece of content come from? |
| Redirect and URL metadata | Navigation path, final URL, redirect chain, URL-level context | DOM, screenshot, rendered content | `redirects.json` or navigation metadata artifact | How did the browser reach this state? |
| Model context artifact | What the model received | Raw browser truth, omitted content, visual state unless explicitly included | `model_context.json` or equivalent context artifact | What evidence was transformed into model input? |

## Capture Timing

Capture timing is evidence.

A browser page is not always stable at first load. Client-side rendering, delayed content, asynchronous requests, redirects, timers, animations, and user-triggered state changes can alter the security interpretation.

A serious browser-based AI security test should define when evidence is captured.

Baseline capture records target state before the synthetic artifact is loaded. It helps distinguish the lab target’s normal state from the test case.

After page load capture records the page after initial navigation completes. It is useful, but it should not be treated as final when delayed behavior is part of the case.

After network idle or stable state capture can help identify post-load browser state, though the lab should not assume network idle means semantic safety.

Delayed content capture is required when the case models state changes after a controlled interval or event.

Pre-model capture is mandatory. Browser evidence should exist before model interpretation.

Post-model capture may matter when the model interaction changes the application state, report state, or enforcement simulation view.

Before and after screenshot comparison is useful when testing delayed content, user-facing state changes, visual mismatch, or enforcement simulation.

The timing record should be included in the artifact manifest. It should state when each artifact was captured and why that capture point mattered.

Without timing evidence, delayed behavior becomes guesswork.

## Correlation Logic

A report should not simply store artifacts.

It should compare them.

Correlation is where browser evidence becomes useful. The goal is not to collect every possible artifact for its own sake. The goal is to identify whether the evidence views support, contradict, or qualify the conclusion.

Useful correlation questions include:

* Does rendered text appear in the DOM?
* Does DOM content fail to appear visually?
* Does the screenshot show visual cues absent from rendered text?
* Does the frame tree show nested content that the top-level DOM summary missed?
* Does the model context include content not visible in the screenshot?
* Does the model context omit visible content that appeared in the screenshot?
* Does the redirect chain explain the final rendered state?
* Does delayed content change the security interpretation?
* Does a child frame contain content that the report attributes to the parent page?
* Does the model receive flattened text that loses visual hierarchy?
* Does the screenshot show a QR code that text extraction did not represent?
* Does the policy decision reference evidence that was not preserved?

These questions are safe.

They do not require exploit payloads.

They require disciplined comparison.

A high-quality report should identify material disagreements between evidence views. It should not hide them.

## Evidence Capture Workflow

A controlled browser evidence workflow should be explicit.

1. Select the test case.

2. Start the run directory.

3. Record the test case identifier and version.

4. Record browser, harness, target, and model versions.

5. Capture baseline target state.

6. Load the controlled synthetic artifact.

7. Capture raw HTML where applicable.

8. Capture the DOM snapshot.

9. Capture rendered text.

10. Capture the screenshot.

11. Capture the frame tree.

12. Capture redirect and URL metadata.

13. Capture timing and state-change metadata.

14. Build model context from labeled evidence.

15. Save the model context artifact.

16. Query the model only after evidence capture.

17. Save raw model output.

18. Validate model output.

19. Apply deterministic policy.

20. Generate the report.

21. Record artifact hashes.

22. Review evidence differences.

The ordering is intentional.

Evidence comes before model interpretation. Model output comes before validation. Validation comes before policy. Policy comes before enforcement simulation. The report comes from artifacts, not from memory.

## Artifact Naming and Manifest Requirements

Artifacts need stable names and hashes.

Stable names make review easier. Hashes help preserve integrity. A manifest turns a directory of files into a defensible evidence package.

A conceptual manifest can look like this:

```yaml
run_id: "BSAI-RUN-20260524-EXAMPLE"
test_case_id: "BSAI-SYN-036-EXAMPLE"
test_case_version: "1.0"
target_version: "LOCAL_TARGET_VERSION_EXAMPLE"
browser_name: "BROWSER_NAME_EXAMPLE"
browser_version: "BROWSER_VERSION_EXAMPLE"
harness_version: "HARNESS_VERSION_EXAMPLE"
model_name: "MODEL_NAME_EXAMPLE"
model_version: "MODEL_VERSION_EXAMPLE"

capture_timestamps:
  baseline_capture_utc: "2026-05-24T00:00:00Z"
  page_load_capture_utc: "2026-05-24T00:00:05Z"
  delayed_capture_utc: "2026-05-24T00:00:15Z"
  pre_model_capture_utc: "2026-05-24T00:00:20Z"
  post_model_capture_utc: "2026-05-24T00:00:30Z"

artifacts:
  - filename: "raw_html.html"
    artifact_type: "raw_html"
    sha256: "SHA256_PLACEHOLDER_RAW_HTML"
    purpose: "Preserve initial source where applicable"
    required: true
    present: true
    notes: "LAB_DOMAIN_EXAMPLE only"

  - filename: "dom_snapshot.html"
    artifact_type: "dom_snapshot"
    sha256: "SHA256_PLACEHOLDER_DOM"
    purpose: "Preserve live document state after browser processing"
    required: true
    present: true
    notes: "Captured before model context build"

  - filename: "rendered_text.txt"
    artifact_type: "rendered_text"
    sha256: "SHA256_PLACEHOLDER_RENDERED_TEXT"
    purpose: "Preserve user-facing extractable text"
    required: true
    present: true
    notes: "Visible text extraction from controlled browser session"

  - filename: "screenshot.png"
    artifact_type: "screenshot"
    sha256: "SHA256_PLACEHOLDER_SCREENSHOT"
    purpose: "Preserve visual browser state"
    required: true
    present: true
    notes: "Viewport and full-page setting recorded separately"

  - filename: "frame_tree.json"
    artifact_type: "frame_tree"
    sha256: "SHA256_PLACEHOLDER_FRAME_TREE"
    purpose: "Preserve parent and child frame relationships"
    required: true
    present: true
    notes: "No third-party targets used"

  - filename: "redirects.json"
    artifact_type: "redirect_metadata"
    sha256: "SHA256_PLACEHOLDER_REDIRECTS"
    purpose: "Preserve navigation and final URL metadata"
    required: true
    present: true
    notes: "Local or lab-owned destinations only"

  - filename: "timing.json"
    artifact_type: "timing_record"
    sha256: "SHA256_PLACEHOLDER_TIMING"
    purpose: "Preserve capture sequence and timing assumptions"
    required: true
    present: true
    notes: "Includes delayed capture checkpoint"

  - filename: "model_context.json"
    artifact_type: "model_context"
    sha256: "SHA256_PLACEHOLDER_CONTEXT"
    purpose: "Preserve exactly what entered model context"
    required: true
    present: true
    notes: "Browser-derived content labeled untrusted"

  - filename: "raw_model_output.json"
    artifact_type: "raw_model_output"
    sha256: "SHA256_PLACEHOLDER_MODEL_OUTPUT"
    purpose: "Preserve untrusted model response before validation"
    required: true
    present: true
    notes: "Not treated as policy authority"

  - filename: "policy_decision.json"
    artifact_type: "policy_decision"
    sha256: "SHA256_PLACEHOLDER_POLICY"
    purpose: "Preserve deterministic policy result"
    required: true
    present: true
    notes: "Policy engine owns final decision"

  - filename: "report.md"
    artifact_type: "report_markdown"
    sha256: "SHA256_PLACEHOLDER_REPORT"
    purpose: "Provide analyst-readable summary with evidence references"
    required: true
    present: true
    notes: "Generated from artifacts"
```

The exact schema can change.

The requirements should not.

A reviewer must be able to determine what artifacts exist, what purpose they serve, whether they were required, whether they were present, and whether their hashes match.

## Evidence Quality Table

| Artifact | Minimum Quality Bar | Common Defect | Impact of Defect |
|---|---|---|---|
| DOM snapshot | Captured from the controlled browser after relevant page state exists | Captured too early or only from raw source | Script-mutated or delayed content cannot be reviewed |
| Rendered text | Captures user-facing text with capture timing recorded | Flattened text without timing, viewport, or extraction method | Reviewer cannot compare visible content with DOM and model context |
| Screenshot | Captures relevant visual state with viewport or full-page mode documented | Screenshot taken before state change or without relevant frame visible | Visual risk signal may be missed or misrepresented |
| Frame tree | Preserves parent and child frame relationships and per-frame URLs where available | Only top-level page captured | Nested content loses origin and context |
| Redirect metadata | Captures navigation path, final URL, and relevant redirect events | Final URL only | Reviewer cannot explain how the browser reached the final state |
| Timing record | Records capture order and relevant timestamps | Missing or informal timing notes | Delayed behavior cannot be reconstructed |
| Model context | Saves exactly what entered the model and labels browser-derived content | Context not saved or hidden content merged into trusted instruction | Trust boundary cannot be reviewed |
| Raw model output | Preserves untrusted model response before validation | Only final report summary retained | Validator and policy behavior cannot be audited |
| Policy decision | Records deterministic decision, inputs, rule, and reason | Decision described only in prose | Reviewer cannot separate model advice from policy action |
| Report markdown | References artifacts and explains evidence differences | Narrative conclusion without artifact links | Analyst cannot challenge or reproduce the finding |

## How Evidence Feeds Model Context

Evidence capture and model context are related.

They are not the same thing.

Evidence should be captured before model interpretation. The model context should be derived from evidence, but it should never replace the original evidence.

This distinction is critical.

A DOM snapshot can contain many nodes. Rendered text can flatten visible content. A screenshot can show visual state. A frame tree can explain nested origin. The context builder may select, summarize, label, omit, or transform parts of those artifacts before sending anything to a model.

That transformation must be reviewable.

Untrusted browser content must be labeled as untrusted. System instructions must remain separate from browser-derived content. Test instructions must not be mixed with page text. Hidden content must not silently merge with trusted instructions. Frame boundaries should not disappear without explanation. Omissions should be reviewable. Additions should be explainable.

The model context should be saved as its own artifact.

A reviewer should be able to compare:

* DOM evidence against model context
* rendered text against model context
* screenshot evidence against model context
* frame-tree evidence against model context
* redirect metadata against the report conclusion
* model output against validator result
* validator result against policy decision

If the model context cannot be inspected, the test cannot support a strong conclusion.

The model may produce useful analysis.

The evidence must remain independent.

## Analyst Review

Analyst review is part of the evidence pipeline.

It is not an afterthought.

A human reviewer should be able to inspect each evidence view. The reviewer should be able to identify disagreements between views, verify what entered model context, challenge the model’s interpretation, confirm whether policy relied on validated fields, reproduce the test case, identify missing artifacts, and write a defensible conclusion.

A useful review should answer:

* What loaded?
* What rendered?
* What changed?
* What frame contained the relevant content?
* What did the screenshot show?
* What did the DOM contain?
* What did rendered text capture?
* What entered model context?
* What did the model return?
* What did validation accept or reject?
* What did deterministic policy decide?
* What evidence supports the conclusion?
* What evidence is missing?
* What should be retested?

Analyst review is especially important when evidence views disagree.

The model may interpret a case one way. The analyst may determine that the model saw incomplete context. The policy may have reached the right decision for the wrong reason. The screenshot may show a risk signal that text extraction omitted. The frame tree may reveal that the relevant content came from a child frame that the report did not mention.

Those review outcomes improve the control.

They should be captured, not treated as inconvenience.

## Safe Failure Examples Without Payloads

The following failure classes do not require exploit payloads or reusable attack strings.

A screenshot shows a risk signal, but rendered text does not. The lab should flag the gap between visual evidence and text extraction.

A DOM snapshot contains an untrusted marker that is not visible to the user. The lab should show whether the context builder labeled it correctly or omitted it according to policy.

Rendered text includes content that is missing from model context. The lab should make the omission visible.

A frame tree reveals a child frame that is not represented in the top-level summary. The lab should flag incomplete frame evidence.

Redirect metadata contradicts a final-page-only conclusion. The lab should require the report to account for navigation history.

Model context includes hidden content without labeling. The lab should flag a trust-boundary failure.

A report claims success but omits screenshot or frame evidence. The lab should mark the run incomplete.

A timing record shows the page changed after first capture. The lab should compare before and after state rather than trusting the first capture.

These failures are useful because they test the evidence process itself.

They are not payload examples.

They are validation failures.

## Relationship to Authoritative References

Browser evidence work should be grounded in browser platform behavior, web testing discipline, LLM application risk, and repeatable automation.

The [DOM Standard](https://dom.spec.whatwg.org/) and [MDN DOM documentation](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model) are relevant because DOM evidence is a browser platform issue, not an AI invention.

The [HTML Standard](https://html.spec.whatwg.org/) and browser documentation for frames and iframes matter because frame-tree evidence depends on nested browsing contexts and document relationships.

[Playwright documentation](https://playwright.dev/docs/intro) is relevant because Playwright and similar tools can automate browser sessions and capture repeatable evidence. Its documentation covers [screenshots](https://playwright.dev/docs/screenshots), [trace viewing](https://playwright.dev/docs/trace-viewer), and [frames](https://playwright.dev/docs/frames), all of which map directly to browser evidence collection.

The [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/) remains relevant because browser-based AI security testing still depends on disciplined web testing structure.

The [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) helps frame model-context and output-handling risk, including prompt injection and insecure output handling concerns in LLM-enabled applications.

The [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) is relevant because evidence capture supports measurement, review, and risk management. A control that cannot preserve evidence cannot be measured with confidence.

The point is not to turn browser evidence into a literature review.

The point is to keep the lab aligned with the browser platform, structured security testing, AI application risk, and repeatable evidence capture.

## What This Evidence Process Is Not

This evidence process is not a substitute for authorization.

It is not an instruction to test third-party systems.

It is not a phishing analysis pipeline for live victim data.

It is not a claim that screenshots alone prove risk.

It is not a claim that DOM alone proves risk.

It is not a model benchmark.

It is not a replacement for broader web application security testing.

It is an evidence process for controlled browser-based AI security testing.

## Practitioner Quality Bar

A high-quality browser evidence capture should be strong enough that another tester can inspect what was loaded.

Another tester should be able to inspect what rendered.

Another tester should be able to inspect what changed.

Another tester should be able to inspect frame context.

Another tester should be able to inspect what entered model context.

Another tester should be able to challenge the model interpretation.

Another tester should be able to reproduce the case locally.

A defender should be able to use the result to improve a control.

That is the quality bar.

If the evidence cannot be compared, the conclusion is weak.

If the model context cannot be inspected, the trust boundary is unreviewable.

If frame evidence is missing, nested content may be misattributed.

If screenshots are missing, visual risk may be lost.

If timing is missing, delayed behavior may be invisible.

If the report cannot be challenged, it is not serious evidence.

## Closing Thesis

Part 36 defines browser evidence as a multi-view problem.

DOM evidence, rendered page evidence, screenshot evidence, and frame-tree evidence each reveal different parts of browser state.

Serious browser-based AI security testing must capture, compare, and preserve these views before trusting model interpretation or policy conclusions.

A browser-AI control should not be evaluated only by what the model says.

It should be evaluated by what the evidence proves.

That means preserving the DOM.

Preserving the rendered page.

Preserving the screenshot.

Preserving the frame tree.

Preserving the model context.

Then comparing them.

That is how browser evidence becomes defensible.