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

<table>  
  <thead>  
    <tr>  
      <th>Do This</th>  
      <th>Not This</th>  
    </tr>  
  </thead>  
  <tbody>  
    <tr>  
      <td><code>Add multi-factor auth support</code></td>  
      <td><code>security stuff</code></td>  
    </tr>  
    <tr>  
      <td><code>Fix buffer overflow in CSV parser</code></td>  
      <td><code>hope this works</code></td>  
    </tr>  
    <tr>  
      <td><code>Update dependencies (CVE-2024-5678)</code></td>  
      <td><code>npm install lol</code></td>  
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