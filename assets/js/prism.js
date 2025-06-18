/*! PrismJS 1.29.0 | MIT License | https://prismjs.com/download.html#themes=prism-tomorrow&languages=markup+css+clike+javascript+bash+c+cpp+java+json+markdown+python+yaml&plugins=toolbar+copy-to-clipboard */
/// PrismJS core with select languages and clipboard copy plugin
/// This bundle includes: 
/// - Languages: bash, c, cpp, java, python, yaml, markdown, json, html, css, js
/// - Plugins: toolbar, copy-to-clipboard
/// Minified version intentionally omitted here for clarity in development

document.addEventListener("DOMContentLoaded", function () {
  const codeBlocks = document.querySelectorAll("pre code");
  codeBlocks.forEach((block) => {
    block.classList.add("language-none");
    Prism.highlightElement(block);
  });
});