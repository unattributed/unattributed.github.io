---
---

````markdown
                   _   _   _        _ _           _           _       _   _                         
 _   _ _ __   __ _| |_| |_| |_ _ __(_) |__  _   _| |_ ___  __| |     | |_| |__   ___ _ __ ___   ___ 
| | | | '_ \ / _` | __| __| __| '__| | '_ \| | | | __/ _ \/ _` |_____| __| '_ \ / _ \ '_ ` _ \ / _ \
| |_| | | | | (_| | |_| |_| |_| |  | | |_) | |_| | ||  __/ (_| |_____| |_| | | |  __/ | | | | |  __/
 \__,_|_| |_|\__,_|\__|\__|\__|_|  |_|_.__/ \__,_|\__\___|\__,_|      \__|_| |_|\___|_| |_| |_|\___|

A privacy-first, minimalist Jekyll theme built for cybersecurity professionals, automation writers, and those blogging in the age of AI surveillance. Designed to be fast, clean, monospaced, and resilient.

---

## 🔍 Live Demo

**Site**: [https://unattributed.blog](https://unattributed.blog)  
**Preview**:  
![preview](https://unattributed.blog/preview.jpg)

---

## ✨ Features

- ⚫️ Terminal-style dark theme (monospace font, yellow links)
- ✅ Clean: no bios, no sidebars, no JS bloat
- 🔍 Dual-mode in-browser search (metadata + full-text)
- 🗂 Auto-generated category archive pages in `_category_pages/`
- 📦 Offline-first, CDN-free design for full control and permanence
- 🔐 No third-party analytics, fonts, or dependencies
- 🛠 Python automation tools for post QA and formatting
- ✅ GitHub Actions CI with full test suite
- ⬇️ One-click copy/download buttons for code blocks

---

## 🚀 Quick Start

1. **Use this repo as a template**  
   Click [Generate new repo](https://github.com/unattributed/unattributed-theme/generate) to instantly create your own fork of this site.

2. **Install Ruby and Jekyll**  
   ```bash
   sudo apt install ruby-full build-essential zlib1g-dev
   gem install bundler jekyll
   bundle install
````

3. **Run locally**

   ```bash
   bundle exec jekyll serve
   ```

4. **Edit `_posts/*.md`**, commit, and push to GitHub Pages.

---

## 🔎 Hybrid Search (No Index Files)

`assets/js/search-hybrid.js` implements a **hybrid client-side search system**:

* **Predictive** search checks user input against post metadata including titles, categories, and tags.
* **Ad hoc full-text** search scans the complete in-browser contents of all blog posts (embedded in `window.posts`).

Search results appear in real-time in a single UI without external APIs or index files. This eliminates reliance on `_data/search_suggestions.json` or Lunr.js and supports fully offline functionality.

---

## 🎨 Styling Overview

This theme uses Dart Sass with modular SCSS structure:

* `main.scss`: Central entry point, imports all other partials with `@use`
* `_sass/variables.scss`: Core theme settings (colors, layout, spacing)
* `_sass/theme.scss`: Primary styles for layout, typography, dark mode
* `assets/css/style.scss`: Final compiled output for site styling

All assets are bundled locally, no external CSS/CDN required.

---

## ⚙️ Configuration

Edit `_config.yml` to update:

* Site title, description, author
* Base URL, permalink structure
* Highlighter and syntax theme
* Category archive paths and behaviors

---

## 🧪 Automation & Testing

Automation scripts are located in `_scripts/` and tested with Pytest under `_tests/`.

Install Python requirements:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Key flags:

* `--dry-run`: simulate changes
* `--quiet`: suppress output
* `--verbose`: detailed logs

Run the test suite:

```bash
PYTHONPATH=. pytest -v _tests/
```

CI integration ensures every commit is validated automatically on GitHub Actions.

---

## 🧾 Markdown & Front Matter Rules

Each `_posts/*.md` must contain:

```yaml
layout: post
title: "your-title"
date: YYYY-MM-DD
author: your-name
categories: [example, tag]
tags: [another, keyword]
```

* Categories and tags must be lowercase, alphanumeric
* Filenames and permalinks should use kebab-case

---

## ❓ Why This Theme?

Most modern content is written by AI and served through opaque platforms. This theme is for humans who still publish with intent: clean, offline, respectful of reader attention, and easy to maintain without JavaScript frameworks or marketing overlays.

---

## 📄 License

MIT License. Use freely. Fork anonymously. No attribution required.

> Built for those who still write with intent of being unattributed but not without voice.
> — [unattributed](https://github.com/unattributed)
