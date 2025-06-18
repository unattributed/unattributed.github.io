---
layout: post
title: "Exploring Liquid, HTML Tables, and Multilingual Code Blocks"
date: 2024-09-03
author: unattributed
categories: [jekyll, testing, layout]
tags: [jekyll, theme, code, table, markdown]
---

# Rich Markdown Structures for Jekyll Themes

This post demonstrates how to include various content types in a markdown file compatible with GitHub Pages and Jekyll, such as HTML tables, multiple code blocks, and safely escaped Liquid syntax.

## 🔢 HTML Table

<table>
  <thead>
    <tr>
      <th>Language</th>
      <th>Purpose</th>
      <th>Extension</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Markdown</td>
      <td>Blog posts</td>
      <td>.md</td>
    </tr>
    <tr>
      <td>SCSS</td>
      <td>Styling</td>
      <td>.scss</td>
    </tr>
    <tr>
      <td>Liquid</td>
      <td>Templating</td>
      <td>.liquid</td>
    </tr>
  </tbody>
</table>

## 💡 Multilingual Code Examples

```bash
# Bash script to serve Jekyll locally
bundle exec jekyll serve --livereload
```

```python
# Python snippet to automate post creation
from datetime import datetime

def slugify(title):
    return title.lower().replace(" ", "-")

print(slugify("New Blog Post"))
```

```html
<!-- Basic HTML block -->
<div class="post">
  <h2>Hello, Jekyll!</h2>
</div>
```

## 📘 Liquid Snippet Example (Escaped)

The following code shows how to loop through posts tagged with `jekyll`:

```html
<pre><code>
&#123;% assign posts = site.posts | where_exp: "post", "post.tags contains 'jekyll'" %&#125;
&lt;ul&gt;
  &#123;% for post in posts %&#125;
    &lt;li&gt;&lt;a href=&#123;&#123; post.url &#125;&#125;&gt;&#123;&#123; post.title &#125;&#125;&lt;/a&gt;&lt;/li&gt;
  &#123;% endfor %&#125;
&lt;/ul&gt;
</code></pre>
```

This prevents Jekyll from interpreting the Liquid tags during build.

## ✅ Conclusion

This example combines Markdown, HTML, and safely escaped Liquid to create versatile sample content for Jekyll-based themes.