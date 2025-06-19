---
layout: post
title: "How Not to Write Git Commit Comments"
date: 2025-05-11
author: unattributed
categories: [version-control]
tags: [vcs]
---

# How Not to ...
**Write Git Commit Comments**

Writing good Git commit messages is a skill that separates professional developers from… well, those who look like idiots. A well-crafted commit message improves collaboration, makes debugging easier, and helps with future code reviews. Here’s how to avoid common pitfalls and write Git commit comments that actually add value.  

## The Cardinal Sins of Git Commit Messages  

Before we discuss best practices, let’s highlight what **not** to do:  

- **"Fixed bug"** – Which bug? How?  
- **"Updated code"** – What changed? Why?  
- **"asdf"** – Seriously?  
- **"WIP"** (without context) – Work in progress on what?  
- **"Please work this time"** – We’ve all been there, but no.  

## How to Write a Good Git Commit Message  

### 1. **Use a Clear, Descriptive Subject Line**  
- Keep it under **50 characters** (if possible).  
- Start with an **imperative verb** (e.g., "Fix," "Add," "Refactor").  
- No trailing punctuation.  

**Bad:**  
```  
fixed the thing  
```  

**Good:**  
```  
Fix memory leak in user authentication module  
```  

### 2. **Provide a Detailed Body (When Needed)**  
- Explain **what changed** and **why** (not just *how*).  
- Wrap lines at **72 characters** for readability.  
- Use bullet points if necessary.  

**Example:**  
```  
Refactor password validation logic  

- Split into separate helper functions for readability  
- Add entropy check for weak passwords (CWE-521 compliance)  
- Remove deprecated SHA-1 hashing  
```  

### 3. **Reference Issues & Tickets**  
If your commit relates to a Jira ticket, GitHub issue, or CVE, **link it!**  

**Example:**  
```  
Patch SQL injection in login form (CVE-2023-1234)  

- Sanitize user input in `login.php`  
- Add parameterized queries (Fixes #123)  
```  

### 4. **Avoid Vague or Emotional Messages**  
🚫 **"OMG FINALLY"** → ✅ **"Fix race condition in file upload handler"**  

## A Quick Reference Table  

<table style="border-collapse: collapse; width: 100%; margin: 16px 0; font-family: Arial, sans-serif;">
  <thead>
    <tr>
      <th style="border: 1px solid lightgrey; padding: 12px; text-align: left; font-weight: 600;">Do This</th>
      <th style="border: 1px solid lightgrey; padding: 12px; text-align: left; font-weight: 600;">Not This</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">Add multi-factor auth support</code></td>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">security stuff</code></td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">Fix buffer overflow in CSV parser</code></td>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">hope this works</code></td>
    </tr>
    <tr>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">Update dependencies (CVE-2024-5678)</code></td>
      <td style="border: 1px solid lightgrey; padding: 12px;"><code style="padding: 2px 4px; border-radius: 3px;">npm install lol</code></td>
    </tr>
  </tbody>
</table>

## Final Tip: Follow a Convention  
If your team uses a standard (like [Conventional Commits](https://www.conventionalcommits.org/)), stick to it. Consistency matters.  

**Example:**  
```  
feat(auth): add rate limiting to login endpoint  

- Limits failed attempts to 5/min (prevents brute force)  
- Logs suspicious IPs (Ref: SEC-456)  
```  

### **TL;DR:**  
✔ **Be clear.**  
✔ **Be concise.**  
✔ **Explain why, not just what.**  
✔ **Reference relevant issues.**  
✔ **Don’t be the person who writes "lol" in a commit.**  

Shopkeepr 'at' unattributed understands this, but doesn't follow this 🚀

[Back to Top](#how-not-to-write-git-commit-comments)