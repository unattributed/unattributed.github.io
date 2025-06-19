# 📘 Release Notes

**Version 1.0.0** — *Initial Public Release*
**2025-06-18**

This is the first stable release of the `unattributed-theme` Jekyll template, designed for minimal, privacy-conscious publishing and technical blogging. It includes GitHub Pages compatibility, search support, archive generation, and AI-aware SEO features.

---

## 🧱 Initial Setup

* **Initial commit** — Basic project scaffolding established. \[`3305c0f`]
* **Docs:** Added setup instructions and system requirements to `README.md`. \[`6920418`]

## 💂 Theme and Content Initialization

* **Theme Config:** Set `remote_theme` to `unattributed/unattributed-theme` for GitHub Pages. \[`55ed1a4`]
* **Content Setup:**

  * Added example blog posts. \[`75132ed`]
  * Created `_category_pages/` for automatic archive generation. \[`33df70c`]
  * Removed placeholder/sample content. \[`0f3651b`]

## 🔧 Build & Deployment

* **GitHub Actions Integration:**

  * Added deployment workflow for Jekyll with GitHub Pages. \[`543c60f`]
  * Corrected workflow path and artifact names. \[`c52ed76`, `d0983b0`]
  * Removed invalid `custom-domain` key and fixed Ruby version. \[`8f63e4b`]

* **Dependencies & Environment:**

  * Installed required theme and plugin dependencies via `Gemfile`. \[`e27ff11`]
  * Updated `_config.yml` to include theme and plugins. \[`449642f`]

* **Site Structure:**

  * Renamed `index.html` to `index.md` for proper layout processing. \[`247d42f`]
  * Removed unnecessary `CNAME` (DNS records already valid). \[`b825254`]

## 🌐 Visual Preview

* Added `preview.jpg` assets for theme repository presentation. \[`6344058`]

## ✨ Content Additions

* Added guide: **Cobalt Strike Beacon Techniques for Red Teamers**. \[`dac3795`]
* Added writeup on **Cloudflare bypass techniques**. \[`9cd629b`]
* Styled and optimized **threat mitigation table** for better readability. \[`d17908b`]

## 🧱 Navigation & Layout Improvements

* Added navigation controls to post pages. \[`b93baad`]
* Fixed broken `/search` links across layouts and menus.
  \[`884fd7d`, `d1591e3`, `37af705`, `0901866`, `0e61403`]

## 🪪 Maintenance & Testing

* Temporarily disabled plugins to test GitHub Pages compatibility. \[`9fd25eb`, `7da864c`]
* Triggered deploys and reconfigured workflows for correctness.
  \[`96f6bee`, `6140c0a`, `23ed776`, `e089138`]

---
