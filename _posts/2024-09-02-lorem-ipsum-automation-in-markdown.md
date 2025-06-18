---
layout: 
title: "Automating Markdown with Lorem Ipsum"
date: 2024-09-02
author: unattributed
categories: [automation, markdown]
tags: [scripting, jekyll, lorem, ipsum]
---

# Automating Markdown Creation

Writing sample content for testing themes or layouts can be automated using scripting tools.

---

## Using Python to Automate `_posts` Entries

Below is a simple example of how to create Markdown files dynamically:

```python
from datetime import date

def create_markdown(title: str, filename: str):
    content = f"""---
layout: post
title: "{title}"
date: {date.today()}
author: "automation"
categories: [examples, testing]
tags: [markdown, scripts]
---

# {title}

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
"""
    with open(filename, "w") as f:
        f.write(content)

create_markdown("Automated Post", "_posts/2024-09-10-automated-post.md")
````

---

## Terminal One-Liner

Need to insert placeholder Markdown via terminal?

```bash
printf "---\nlayout: post\ntitle: Terminal Example\n---\n\n# Hello from bash!" > _posts/2024-09-03-terminal-example.md
```

---

## Multiple Section Levels

### H3 Title Level

Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.

#### H4 Title Level

Totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto.

##### H5 Title Level

Beatae vitae dicta sunt explicabo.

---

## Blockquote with Markdown Tip

> 💡 *Tip*: When writing markdown posts, preview them in your browser using `bundle exec jekyll serve`.

---

## Final Thoughts

Automating markdown generation is helpful for:

* Static site testing
* Demo content
* Theming development

---