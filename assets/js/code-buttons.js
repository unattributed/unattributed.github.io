document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("pre > code").forEach((codeBlock, index) => {
    const pre = codeBlock.parentElement;

    // Copy button
    const copyBtn = document.createElement("button");
    copyBtn.textContent = "Copy";
    copyBtn.className = "copy-button";
    copyBtn.setAttribute("type", "button");
    copyBtn.addEventListener("click", () => {
      navigator.clipboard.writeText(codeBlock.textContent).then(() => {
        copyBtn.textContent = "Copied!";
        setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
      });
    });

    // Download button
    const downloadBtn = document.createElement("button");
    downloadBtn.textContent = "Download";
    downloadBtn.className = "download-button";
    downloadBtn.setAttribute("type", "button");
    downloadBtn.addEventListener("click", () => {
      const blob = new Blob([codeBlock.textContent], { type: "text/plain" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = `code-snippet-${index + 1}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });

    const btnGroup = document.createElement("div");
    btnGroup.className = "code-buttons";
    btnGroup.appendChild(copyBtn);
    btnGroup.appendChild(downloadBtn);

    pre.style.position = "relative";
    pre.insertBefore(btnGroup, codeBlock);
  });
});
