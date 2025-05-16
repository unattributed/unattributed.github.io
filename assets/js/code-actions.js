// assets/js/code-actions.js
document.addEventListener('DOMContentLoaded', function() {
    // ========================
    // SECURITY LANGUAGE CONFIG
    // ========================
    const languageExtensions = {
        // Cloud Security & SIEM
        'kql': 'kql', 'kusto': 'kql', 'sentinel': 'kql',
        'splunk': 'spl', 'sumologic': 'json', 'elasticsearch': 'json',
        'sigma': 'yml', 'yara': 'yar', 'snort': 'rules', 'suricata': 'rules',
        'zeek': 'zeek', 'osquery': 'sql', 'falco': 'yaml',
        
        // Threat Intel
        'stix': 'json', 'openioc': 'xml', 'maec': 'xml', 'cybox': 'xml',
        
        // Cloud Providers
        'aws-cloudwatch': 'json', 'gcp-logging': 'yaml', 'azure-log-analytics': 'kql',
        'aws-guardduty': 'json', 'gcp-scc': 'yaml', 'azure-security-center': 'json',
        
        // Infrastructure-as-Code
        'terraform': 'tf', 'pulumi': 'yaml', 'cloudformation': 'yaml',
        'arm-template': 'json', 'bicep': 'bicep', 'ansible': 'yml',
        
        // Secure Coding Languages
        'c': 'c', 'cpp': 'cpp', 'csharp': 'cs', 'java': 'java',
        'python': 'py', 'go': 'go', 'rust': 'rs', 'ruby': 'rb',
        'php': 'php', 'nodejs': 'js', 'solidity': 'sol',
        
        // Scripting & Shell
        'bash': 'sh', 'powershell': 'ps1', 'zsh': 'sh',
        
        // Web Security
        'sql': 'sql', 'xss': 'txt', 'xslt': 'xsl', 'html': 'html'
    };

    // =====================
    // SECURITY AUTO-NAMING
    // =====================
    const securityFilePrefixes = {
        // Detection Rules
        'sigma': 'sigma_rule_', 'yara': 'yara_', 'snort': 'snort_rule_',
        'suricata': 'suricata_rule_', 'zeek': 'zeek_script_',
        
        // Cloud Queries
        'kql': 'kql_query_', 'splunk': 'splunk_search_',
        
        // Secure Code
        'solidity': 'contract_', 'cpp': 'secure_'
    };

    // =================
    // CORE FUNCTIONALITY
    // =================
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
        
        // Cloud-specific defaults
        if (lang.includes('azure')) return 'json';
        if (lang.includes('aws')) return 'json';
        if (lang.includes('gcp')) return 'yaml';
        
        // Direct matches
        if (languageExtensions[lang]) return languageExtensions[lang];
        
        // Fallback to language detection
        if (lang.includes('python')) return 'py';
        if (lang.includes('javascript')) return 'js';
        
        return 'txt';
    }

    // ==============
    // UI COMPONENTS
    // ==============
    function createSecurityLabel(preElement, language) {
        const label = document.createElement('div');
        label.className = 'security-language-label';
        
        // Threat detection rules (red)
        if (/sigma|yara|snort|suricata/i.test(language)) {
            label.style.backgroundColor = '#ff4444';
            label.style.color = 'white';
        }
        // Cloud providers
        else if (/azure/i.test(language)) {
            label.style.backgroundColor = '#0078D4';
        } 
        else if (/aws/i.test(language)) {
            label.style.backgroundColor = '#FF9900';
        }
        else if (/gcp/i.test(language)) {
            label.style.backgroundColor = '#4285F4';
        }
        // Secure coding (green)
        else if (/solidity|rust|go|cpp|csharp/i.test(language)) {
            label.style.backgroundColor = '#4CAF50';
        }
        
        label.textContent = language.replace(/-/g, ' ').toUpperCase();
        preElement.appendChild(label);
    }

    // =============
    // INITIALIZATION
    // =============
    document.querySelectorAll('pre').forEach(pre => {
        const code = pre.querySelector('code');
        if (!code) return;

        const language = Array.from(code.classList)
            .find(cls => cls.startsWith('language-')) 
            ?.replace('language-', '') || 'text';

        // Create action buttons
        const btnGroup = document.createElement('div');
        btnGroup.className = 'security-code-actions';
        
        // Download Button
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'security-code-btn download';
        downloadBtn.innerHTML = '<svg width="14" height="14"><use xlink:href="#download-icon"/></svg>';
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

        // Copy Button
        const copyBtn = document.createElement('button');
        copyBtn.className = 'security-code-btn copy';
        copyBtn.innerHTML = '<svg width="14" height="14"><use xlink:href="#copy-icon"/></svg>';
        copyBtn.onclick = () => {
            navigator.clipboard.writeText(code.textContent)
                .then(() => {
                    copyBtn.innerHTML = '<svg width="14" height="14"><use xlink:href="#check-icon"/></svg>';
                    setTimeout(() => {
                        copyBtn.innerHTML = '<svg width="14" height="14"><use xlink:href="#copy-icon"/></svg>';
                    }, 2000);
                });
        };

        btnGroup.appendChild(downloadBtn);
        btnGroup.appendChild(copyBtn);
        pre.appendChild(btnGroup);
        
        // Add language label if not plaintext
        if (language !== 'text') {
            createSecurityLabel(pre, language);
        }
    });
});