document.addEventListener('DOMContentLoaded', function() {
    const languageExtensions = {
        // Cloud Security
        'kql': 'kql', 'kusto': 'kql', 'azure-log-analytics': 'kql', 'sentinel': 'kql',
        'aws-cloudwatch': 'json', 'gcp-logging': 'json', 'splunk': 'spl', 'sumologic': 'json',
        'sigma': 'yml', 'yara': 'yar', 'stix': 'json', 'openioc': 'xml',
        'osquery': 'sql', 'falco': 'yaml', 'zeek': 'zeek', 'suricata': 'rules',

        // Cloud IaC
        'bicep': 'bicep', 'arm-template': 'json', 'cloudformation': 'yaml', 
        'gcp-deployment': 'yaml', 'terraform': 'tf', 'pulumi': 'yaml',

        // Standard Languages
        'bash': 'sh', 'python': 'py', 'powershell': 'ps1', 'rust': 'rs', 'go': 'go',
        'sql': 'sql', 'c': 'c', 'cpp': 'cpp', 'java': 'java', 'csharp': 'cs'
    };

    const specialFileNames = {
        'sigma': 'sigma_rule_', 'yara': 'yara_rule_', 
        'azure-policy': 'azure_policy_', 'aws-cloudwatch': 'aws_query_',
        'gcp-logging': 'gcp_query_', 'kql': 'kql_query_'
    };

    function getFileName(language) {
        const prefix = specialFileNames[language.toLowerCase()] || '';
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
        return `${prefix}${timestamp}`;
    }

    function getExtension(language) {
        const langKey = language.toLowerCase();
        if (langKey.includes('azure')) return 'json';
        if (langKey.includes('aws')) return 'json';
        if (langKey.includes('gcp')) return 'yaml';
        return languageExtensions[langKey] || 'txt';
    }

    function createDownloadButton(codeContent, language) {
        const button = document.createElement('button');
        button.className = 'code-btn download';
        button.innerHTML = '↓';
        button.title = 'Download';
        
        button.addEventListener('click', () => {
            const extension = getExtension(language);
            const blob = new Blob([codeContent], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${getFileName(language)}.${extension}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
        
        return button;
    }

    function createCopyButton(codeContent) {
        const button = document.createElement('button');
        button.className = 'code-btn copy';
        button.innerHTML = '⎘';
        button.title = 'Copy';
        
        button.addEventListener('click', () => {
            navigator.clipboard.writeText(codeContent).then(() => {
                button.innerHTML = '✓';
                setTimeout(() => button.innerHTML = '⎘', 2000);
            });
        });
        
        return button;
    }

    function addLanguageLabel(preElement, language) {
        const label = document.createElement('div');
        label.className = 'language-label';
        
        if (language.match(/azure/i)) {
            label.style.backgroundColor = '#0078D4'; // Azure blue
        } else if (language.match(/aws/i)) {
            label.style.backgroundColor = '#FF9900'; // AWS orange
        } else if (language.match(/gcp/i)) {
            label.style.backgroundColor = '#4285F4'; // GCP blue
        } else if (language.match(/sigma|yara/i)) {
            label.style.backgroundColor = '#FF5722'; // Alert orange
        }
        
        label.textContent = language.replace(/-/g, ' ');
        preElement.appendChild(label);
    }

    document.querySelectorAll('pre').forEach(preElement => {
        const codeElement = preElement.querySelector('code');
        if (!codeElement) return;

        const languageClasses = Array.from(codeElement.classList)
            .filter(className => className.startsWith('language-'));
        
        const language = languageClasses.length > 0 
            ? languageClasses[0].replace('language-', '')
            : 'text';

        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'code-actions';
        
        actionsContainer.appendChild(
            createDownloadButton(codeElement.textContent, language)
        );
        
        actionsContainer.appendChild(
            createCopyButton(codeElement.textContent)
        );
        
        preElement.appendChild(actionsContainer);
        
        if (language !== 'text') {
            addLanguageLabel(preElement, language);
        }
    });
});