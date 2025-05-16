---
title: "Code Block Test"
date: 2025-05-16
categories: [Testing]
tags: 
  - codeblocks
  - security
  - test
---

### 1. File Creation/Updates Needed

#### A. Create new JavaScript file:
```javascript
// assets/js/code-actions.js
[Previous complete content from last message]
```
**Commit:**  
`git add assets/js/code-actions.js`  
`git commit -m "add cloud security code actions with KQL and multi-cloud support"`

#### B. Update CSS (append to existing main.scss):
```scss
// assets/css/main.scss
[Add the new code block styles from previous messages]
```
**Commit:**  
`git add assets/css/main.scss`  
`git commit -m "style code blocks for security content with provider colors"`

#### C. Update footer inclusion:
```html
// _includes/footer.html
[Add the script tag as shown earlier]
```
**Commit:**  
`git add _includes/footer.html`  
`git commit -m "load code actions script in footer"`

### 2. Implementation Verification

To test the implementation:

1. Create a test post with code blocks like:
````markdown
```kql
SecurityAlert
| where TimeGenerated > ago(7d)
| where AlertName == "Suspicious PowerShell Execution"
```

```sigma
title: Suspicious Service Installation
logsource:
    product: windows
detection:
    selection:
        EventID: 7045
    condition: selection
```
````

2. Verify:
- Language labels appear with correct colors
- Download generates properly named files
- Copy functionality works
- Hover states appear correctly

### 3. Optional Enhancements

Things I might do later?  
- [ ] Custom icons for different languages  
- [ ] Keyboard shortcuts for copy  
- [ ] Download all code blocks in a post  
- [ ] Line number toggling  

