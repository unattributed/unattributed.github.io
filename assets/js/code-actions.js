document.addEventListener('DOMContentLoaded', function() {
    // Security language configuration
    const languageExtensions = {
        'kql': 'kql', 'kusto': 'kql', 'sentinel': 'kql',
        'splunk': 'spl', 'sumologic': 'json', 'elasticsearch': 'json',
        'sigma': 'yml', 'yara': 'yar', 'snort': 'rules', 'suricata': 'rules',
        'zeek': 'zeek', 'osquery': 'sql', 'falco': 'yaml',
        'stix': 'json', 'openioc': 'xml', 'maec': 'xml', 'cybox': 'xml',
        'aws-cloudwatch': 'json', 'gcp-logging': 'yaml', 'azure-log-analytics': 'kql',
        'aws-guardduty': 'json', 'gcp-scc': 'yaml', 'azure-security-center': 'json',
        'terraform': 'tf', 'pulumi': 'yaml', 'cloudformation': 'yaml',
        'arm-template': 'json', 'bicep': 'bicep', 'ansible': 'yml',
        'c': 'c', 'cpp': 'cpp', 'csharp': 'cs', 'java': 'java',
        'python': 'py', 'go': 'go', 'rust': 'rs', 'ruby': 'rb',
        'php': 'php', 'nodejs': 'js', 'solidity': 'sol',
        'bash': 'sh', 'powershell': 'ps1', 'zsh': 'sh',
        'sql': 'sql', 'xss': 'txt', 'xslt': 'xsl', 'html': 'html'
    };

    const securityFilePrefixes = {
        'sigma': 'sigma_rule_', 'yara': 'yara_', 'snort': 'snort_rule_',
        'suricata': 'suricata_rule_', 'zeek': 'zeek_script_',
        'kql': 'kql_query_', 'splunk': 'splunk_search_',
        'solidity': 'contract_', 'cpp': 'secure_'
    };

    const languageColors = {
        'sigma': '#ff4444', 'yara': '#ff4444', 'snort': '#ff4444', 'suricata': '#ff4444',
        'azure': '#0078D4', 'aws': '#FF9900', 'gcp': '#4285F4',
        'solidity': '#4CAF50', 'rust': '#4CAF50', 'go': '#4CAF50',
        'cpp': '#4CAF50', 'csharp': '#4CAF50', 'python': '#4CAF50',
        'bash': '#859900', 'powershell': '#859900',
        '_default': '#9cdcfe'
    };

    function getLanguageColor(lang) {
        lang = lang.toLowerCase();
        for (const [key, color] of Object.entries(languageColors)) {
            if (lang.includes(key)) return color;
        }
        return languageColors._default;
    }

    function getSecurityPrefix(lang) {
        lang = lang.toLowerCase();
        for (const [key, prefix] of Object.entries(securityFilePrefixes)) {
            if (lang.includes(key)) return prefix;
        }
        return '';
    }

    function getDownloadFilename(language) {
        const prefix = getSecurityPrefix(language) || '';
        const timestamp = new Date().toISOString()
            .replace(/[:.]/g, '-')
            .replace('T', '_')
            .slice(0, 19);
        return `${prefix}${timestamp}`;
    }

    function getFileExtension(language) {
        const lang = language.toLowerCase();
        if (lang.includes('azure')) return 'json';
        if (lang.includes('aws')) return 'json';
        if (lang.includes('gcp')) return 'yaml';
        if (languageExtensions[lang]) return languageExtensions[lang];
        if (lang.includes('python')) return 'py';
        if (lang.includes('javascript')) return 'js';
        return 'txt';
    }

    function createSecurityLabel(preElement, language) {
        const label = document.createElement('div');
        label.className = 'security-language-label';
        label.style.backgroundColor = getLanguageColor(language);
        label.style.color = '#ffffff';
        label.textContent = language.replace(/-/g, ' ').toUpperCase();
        preElement.appendChild(label);
    }

    document.querySelectorAll('pre').forEach(pre => {
        const code = pre.querySelector('code');
        if (!code) return;

        const language = Array.from(code.classList)
            .find(cls => cls.startsWith('language-')) 
            ?.replace('language-', '') || 'text';

        const btnGroup = document.createElement('div');
        btnGroup.className = 'security-code-actions';
        
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'security-code-btn download';
        downloadBtn.title = 'Download';
        downloadBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
        `;
        downloadBtn.onclick = () => {
            const ext = getFileExtension(language);
            const filename = `${getDownloadFilename(language)}.${ext}`;
            const blob = new Blob([code.textContent], {type: 'text/plain'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        };

        const copyBtn = document.createElement('button');
        copyBtn.className = 'security-code-btn copy';
        copyBtn.title = 'Copy';
        copyBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
        `;
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(code.textContent)
                .then(() => {
                    copyBtn.innerHTML = `
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                            <path d="M20 6L9 17l-5-5"></path>
                        </svg>
                    `;
                    setTimeout(() => {
                        copyBtn.innerHTML = `
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                        `;
                    }, 2000);
                });
        };

        btnGroup.appendChild(downloadBtn);
        btnGroup.appendChild(copyBtn);
        pre.appendChild(btnGroup);
        
        if (language !== 'text') {
            createSecurityLabel(pre, language);
        }
    });
});