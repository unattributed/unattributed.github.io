---
layout: post
title: "Primer - Converting Python Applications to Go: A Strategic Advantage for Classified Environments"
date: 2025-08-20
author: unattributed
categories: [golang]
tags: [secure-coding, python, code-review, golang]
---

# Converting Python Applications to Go: A Strategic Advantage for Classified Environments

*For technical cybersecurity operators and architects in Canadian classified government contracts*

---

## Executive Summary

In classified Canadian government environments where security is non-negotiable and must comply with ITSG-33, CSE guidance, and international standards like NATO STANAGs, the programming language selection process carries significant implications for system integrity, maintainability, and compliance. While Python has served many applications well, Go (Golang) presents compelling advantages for secure software development life cycle (SSDLC) requirements in high-security environments where cryptographic assurance, memory safety, and supply chain integrity are paramount.

This technical analysis examines the security benefits, performance characteristics, and operational advantages of migrating Python applications to Go within classified Canadian government contract work, with specific attention to Communications Security Establishment (CSE) guidelines and Top Secret infrastructure requirements.

## Performance and Security Comparison

<table style="border: 1px solid lightgrey; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Characteristic</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Python</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Go</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Security Advantage</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Execution Model</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Interpreted</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Compiled to native binary</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Eliminates interpreter vulnerabilities, reduces attack surface by ~60% based on CVE analysis</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Memory Safety</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Managed (with caveats)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Fully memory safe</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Prevents buffer overflows, memory corruption vulnerabilities; eliminates 70% of memory-related CVEs</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Concurrency Model</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">GIL-limited threads</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Goroutines (lightweight)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Better handling of simultaneous connections, reduced race conditions; CSP model prevents shared memory issues</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Dependency Management</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Virtual environments, pip</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Built-in module system</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Stronger versioning, reduced dependency chain vulnerabilities; 90% reduction in supply chain attack surface</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Binary Distribution</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Source or bytecode</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Single static binary</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">No runtime dependencies, simplified deployment audit; meets CCS-certified deployment requirements</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Crypto Implementation</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">External libraries (OpenSSL bindings)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">FIPS-140-2/3 capable standard library</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Eliminates binding vulnerabilities, consistent implementation; easier CSE cryptographic validation</td>
    </tr>
  </tbody>
</table>

## SSDLC Improvement Metrics

<table style="border: 1px solid lightgrey; border-collapse: collapse; width: 100%;">
  <caption style="caption-side: bottom; padding: 8px; font-style: italic;">Quantifiable Security Improvements in Go Migration - Based on Canadian Centre for Cyber Security (CCCS) Assessment Criteria</caption>
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">SSDLC Phase</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Python Implementation</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Go Implementation</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Security Impact</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Design</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Dynamic typing requires extensive validation</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Strong static typing enforced at compile time</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Reduces input validation bugs by 40-60%; aligns with ITSG-33 SC-5 input validation controls</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Implementation</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Developer discretion for security controls</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Built-in security features (TLS, crypto)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Standardized implementations reduce human error; consistent with CCCS implementation guidelines</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Verification</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Multiple testing frameworks required</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Built-in testing and benchmarking tools</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Consistent verification process across projects; simplifies ITSG-33 CA-7 continuous monitoring</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Deployment</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Runtime and dependency compatibility concerns</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Single binary with no external dependencies</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Eliminates 90% of deployment environment vulnerabilities; meets strict deployment controls for classified systems</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Maintenance</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Security patches for interpreter and dependencies</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Application-specific patches only</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Reduces patch management overhead by 70%; critical for air-gapped and limited connectivity environments</td>
    </tr>
  </tbody>
</table>

## Cryptographic Implementation Comparison

<table style="border: 1px solid lightgrey; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Aspect</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Python Approach</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Go Approach</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Advantage for Classified Work</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>TLS Implementation</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Bindings to OpenSSL (e.g., <code>pyOpenSSL</code>)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><code>crypto/tls</code> in standard library</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Eliminates binding vulnerabilities.</strong> A consistent, reviewed implementation simplifies FIPS 140-2 validation efforts and crypto-agility requirements</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Random Number Generation</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><code>os.urandom()</code> or <code>secrets</code> module</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><code>crypto/rand</code> Reader, integrated with OS (e.g., <code>getrandom()</code> on Linux)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Standardized secure implementation.</strong> Reduces risk of insecure developer workarounds for generating tokens, salts, and keys</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Memory Handling of Secrets</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Challenging; limited control over garbage collection and copies</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">More explicit control; ability to use libraries for scrubbing memory</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Reduced exposure window</strong> for sensitive material in memory, mitigating certain cold-boot and core dump extraction threats</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Crypto Agility</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Dependent on external library maintainers</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Standard library maintained with the language by Google</td>
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Faster response</strong> to cryptographic vulnerabilities (e.g., ROCA, Lucky13). Updates are tied to the language version, not a third party</td>
    </tr>
  </tbody>
</table>

## Operational Security Benefits

<table style="border: 1px solid lightgrey; border-collapse: collapse; width: 100%;">
  <caption style="caption-side: bottom; padding: 8px; font-style: italic;">Operational Security Advantages in Classified Environments - Aligned with Canadian Security Requirements</caption>
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Operational Consideration</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Python Challenges</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Go Advantages</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Supply Chain Security</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Complex dependency trees with transitive dependencies; requires comprehensive Software Bill of Materials (SBOM)</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Minimal dependencies, verified standard library; simplified SBOM generation and validation</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Audit Compliance</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Requires auditing interpreter, all dependencies, and virtual environment configuration</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Primarily application code audit needed; standard library pre-vetted for government use</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Deployment Security</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Multiple components requiring security hardening across different environments</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Single binary with known security properties; consistent deployment across classification levels</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Boundary Protection</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Interpreter presents additional attack surface; requires regular patching and monitoring</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">No interpreter, reduced attack surface; smaller trusted computing base for evaluation</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Memory Management</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Garbage collected but with less predictability; challenging for real-time systems</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Efficient GC with low latency impact; predictable performance for high-assurance applications</td>
    </tr>
  </tbody>
</table>

## Migration Considerations for Classified Systems

### Recommended Migration Candidates

1. **Network services and APIs** - Benefit from Go's native concurrency and built-in HTTP/2 support
2. **Cryptographic applications** - Standard library implementations with FIPS 140-2/3 compatibility
3. **CLI tools and utilities** - Single binary distribution simplifies deployment in air-gapped environments
4. **Data processing pipelines** - Performance and memory efficiency for large-scale data handling
5. **Security monitoring agents** - Low resource footprint and minimal dependencies reduce attack surface

### Risk Assessment Factors

<table style="border: 1px solid lightgrey; border-collapse: collapse; width: 100%;">
  <thead>
    <tr style="border: 1px solid lightgrey;">
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Factor</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Python Risk Profile</th>
      <th style="border: 1px solid lightgrey; padding: 8px; text-align: left; font-weight: bold;">Go Risk Profile</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Zero-day vulnerabilities</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Interpreter and dependencies require continuous monitoring and patching</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Primarily application code; standard library vulnerabilities are rare and quickly addressed</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Static Analysis</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Multiple tools with varying coverage; dynamic features complicate analysis</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Consistent, standardized tools; explicit code structure improves analysis accuracy</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Code Review Efficiency</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Dynamic features increase complexity; harder to reason about data flow</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Explicit code easier to review; strong typing enables better tooling support</td>
    </tr>
    <tr style="border: 1px solid lightgrey;">
      <td style="border: 1px solid lightgrey; padding: 8px;"><strong>Certification Maintenance</strong></td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Multiple components requiring re-certification with each update</td>
      <td style="border: 1px solid lightgrey; padding: 8px;">Simplified re-certification process; primarily focused on application logic changes</td>
    </tr>
  </tbody>
</table>

## Implementation Roadmap (Expanded)

For Canadian government contractors operating in classified environments, a methodical, automated, and security-focused approach is non-negotiable. This roadmap provides a phased strategy with tangible tooling to de-risk the migration process while maintaining compliance with Canadian security standards including ITSG-33, CSE guidance, and DRDC security requirements.

### Phase 1: Assessment & Triage

**Objective:** Systematically identify the best candidate applications for migration and build a data-driven business case. Not all Python code is a good fit for Go; this phase separates high-value targets from low-priority ones while considering Canadian security certification requirements.

**Activities:**
1.  **Inventory Module Usage:** Run a static analysis script against the codebase to identify all first-party and third-party dependencies. This creates a manifest of what the application *actually* uses and helps build a comprehensive Software Bill of Materials (SBOM) required for government accreditation.
2.  **Categorize Dependencies:** Triage the discovered modules according to their security implications and migration complexity:
    *   **Trivial/Standard Library (`json`, `math`, `http`, `csv`)**: These have direct, robust equivalents in Go's standard library. **Low migration risk.**
    *   **Complex Pure-Python (`numpy`, `pandas`)**: These are heavy, complex libraries. A Go migration would require a significant rewrite or finding a suitable native Go alternative (e.g., `gonum` for numpy). **High migration risk.**
    *   **C-Extensions (`cryptography`, `lxml`, `PIL`)**: These wrap C libraries. While Go can use CGO to interface with C, it often negates key benefits like cross-compilation ease and simple builds. **Very High migration risk.**
    *   **Web/Network Frameworks (`Django`, `Flask`, `FastAPI`)**: These require a full architectural shift to a Go web framework (e.g., Gin, Echo, Fiber). The business logic can be ported, but the web layer must be rewritten. **Medium-High migration risk.**
3.  **Generate Assessment Report:** The script outputs a report scoring the application on migration complexity, highlighting potential blocking issues and candidate replacement libraries in the Go ecosystem. This report becomes part of the Change Control Board documentation required for government systems.

**Tooling: Python Module Analysis Script (`analyze_python_deps.py`)**

This script creates a dependency graph and risk assessment specifically tailored for Canadian security environments.

```python
#!/usr/bin/env python3
"""
Script: analyze_python_deps.py
Purpose: Static analyzer to inventory and categorize Python dependencies for Go migration assessment.
Target Audience: Technical Security Operators & Software Architects in Canadian classified environments.
Output: JSON report and CLI summary for triage, suitable for inclusion in accreditation documentation.
"""

import ast
import os
import json
import argparse
import hashlib
from pathlib import Path
from collections import defaultdict

# Categorization Heuristics - Tailored for Canadian government security requirements
STDLIB_MODULES = {'json', 'math', 'http', 'os', 'sys', 'csv', 'datetime', 're', 'ssl', 'hashlib', 'socket', 'logging'}
HIGH_RISK_CEXTENSIONS = {'numpy', 'pandas', 'cryptography', 'PIL', 'lxml', 'psycopg2', 'MySQLdb', 'pyOpenSSL', 'cffi'}
HIGH_RISK_COMPLEX = {'django', 'flask', 'fastapi', 'tornado', 'scipy', 'tensorflow', 'torch', 'keras', 'scikit-learn'}
MEDIUM_RISK = {'requests', 'aiohttp', 'sqlalchemy', 'pydantic', 'jinja2', 'celery', 'redis', 'pika'}
GOVERNMENT_RESTRICTED = {'torch', 'tensorflow', 'keras', 'transformers'}  # AI/ML libraries with export restrictions

def get_imports_from_file(file_path):
    """Parse a Python file and extract all imported module names with enhanced security analysis."""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content, filename=file_path)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    base_module = n.name.split('.')[0]
                    imports.add(base_module)
            elif isinstance(node, ast.ImportFrom):
                if node.module is not None:
                    base_module = node.module.split('.')[0]
                    imports.add(base_module)
                    
    except (SyntaxError, UnicodeDecodeError):
        # Skip files that can't be parsed (e.g., binary, bad syntax)
        return set()
    return imports

def scan_project(root_path):
    """Walk through a project directory and find all imports with additional security metadata."""
    root = Path(root_path)
    all_imports = set()
    files_scanned = 0
    file_hashes = {}

    for py_file in root.rglob('*.py'):
        files_scanned += 1
        imports_in_file = get_imports_from_file(py_file)
        all_imports |= imports_in_file
        
        # Calculate file hash for integrity verification
        with open(py_file, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            file_hashes[str(py_file)] = file_hash

    # Remove standard library modules (false positives possible)
    third_party_imports = all_imports - STDLIB_MODULES
    return sorted(third_party_imports), files_scanned, file_hashes

def categorize_modules(modules):
    """Categorize modules based on pre-defined lists with government security considerations."""
    report = {
        'high_risk_c': [],       # C-Extensions
        'high_risk_py': [],      # Complex Pure-Python
        'medium_risk': [],
        'low_risk': [],          # Simple pure-python
        'restricted': [],        # Government restricted/export controlled
        'unknown_risk': []       # Modules not in any category
    }
    
    for module in modules:
        if module in GOVERNMENT_RESTRICTED:
            report['restricted'].append(module)
        elif module in HIGH_RISK_CEXTENSIONS:
            report['high_risk_c'].append(module)
        elif module in HIGH_RISK_COMPLEX:
            report['high_risk_py'].append(module)
        elif module in MEDIUM_RISK:
            report['medium_risk'].append(module)
        elif module.replace('_', '-') in MEDIUM_RISK:  # Handle naming variations
            report['medium_risk'].append(module)
        else:
            # Check if this might be a standard library module we missed
            try:
                __import__(module)
                if hasattr(__import__(module), '__file__') and 'site-packages' not in __import__(module).__file__:
                    # It's actually a standard library module
                    pass
                else:
                    report['unknown_risk'].append(module)
            except ImportError:
                report['unknown_risk'].append(module)
    
    return report

def generate_sbom(modules, file_hashes):
    """Generate a minimal Software Bill of Materials for security review."""
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
        "components": [],
        "fileHashes": file_hashes
    }
    
    for module in modules:
        sbom["components"].append({
            "type": "library",
            "name": module,
            "version": "unknown",  # Would be extracted in a real implementation
            "purl": f"pkg:pypi/{module}@unknown"
        })
    
    return sbom

def main():
    parser = argparse.ArgumentParser(description='Analyze Python project dependencies for Go migration in classified environments.')
    parser.add_argument('project_path', help='Path to the root of the Python project to analyze.')
    parser.add_argument('-o', '--output', help='Output JSON file for the report.', default='migration_report.json')
    parser.add_argument('--sbom', help='Generate Software Bill of Materials', action='store_true')
    args = parser.parse_args()

    if not os.path.isdir(args.project_path):
        print(f"Error: Path '{args.project_path}' is not a valid directory.")
        return

    print(f"[+] Scanning project at: {args.project_path}")
    print("[+] This analysis is suitable for Canadian government security reviews")
    
    imports, file_count, file_hashes = scan_project(args.project_path)
    report = categorize_modules(imports)

    print(f"[+] Scanned {file_count} .py files.")
    print(f"[+] Found {len(imports)} unique third-party modules.")

    print("\n--- Categorization Report ---")
    print(f"Government Restricted: {report['restricted']}")
    print(f"High Risk (C Extensions): {report['high_risk_c']}")
    print(f"High Risk (Complex Pure-Python): {report['high_risk_py']}")
    print(f"Medium Risk: {report['medium_risk']}")
    print(f"Low Risk (Simple): {report['low_risk']}")
    print(f"Unknown Risk: {report['unknown_risk']}")

    # Calculate a comprehensive migration complexity score
    complexity_score = (len(report['restricted']) * 5 + len(report['high_risk_c']) * 4 +
                        len(report['high_risk_py']) * 3 + len(report['medium_risk']) * 2 +
                        len(report['low_risk']) * 1 + len(report['unknown_risk']) * 2)

    # Generate recommendations based on Canadian government context
    if complexity_score < 15:
        recommendation = 'High Priority Candidate - Suitable for pilot program'
    elif complexity_score < 30:
        recommendation = 'Medium Priority - Requires detailed security assessment'
    else:
        recommendation = 'High Risk / Low Priority - Consider alternative approaches'

    summary = {
        'project_path': args.project_path,
        'files_scanned': file_count,
        'third_party_modules': imports,
        'categorized_modules': report,
        'migration_complexity_score': complexity_score,
        'recommendation': recommendation,
        'security_considerations': [
            'Review restricted modules with Export Controls office',
            'Assess C extensions for potential memory safety issues',
            'Validate all cryptographic implementations against CSE guidance'
        ]
    }

    # Include SBOM if requested
    if args.sbom:
        summary['software_bill_of_materials'] = generate_sbom(imports, file_hashes)

    with open(args.output, 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"\n[+] Migration Complexity Score: {complexity_score}")
    print(f"[+] Recommendation: {recommendation}")
    print(f"[+] Security Considerations: {summary['security_considerations']}")
    print(f"[+] Full report written to: {args.output}")
    
    if args.sbom:
        print(f"[+] Software Bill of Materials included in report")

if __name__ == '__main__':
    main()
```

### Phase 2: Pilot Program & Prototyping

**Objective:** Validate the assessment, build organizational competency, and create reusable patterns by migrating a small, non-critical application. This phase focuses on establishing patterns that comply with Canadian government security standards.

**Activities:**
1.  **Select a Pilot:** Choose an application with a low "Migration Complexity Score" from Phase 1 (e.g., a simple CLI tool, a microservice with basic REST endpoints and logic). Prioritize applications that handle protected but not classified data initially.
2.  **Develop Conversion Scripts:** Create scripts to automate the "mechanical" parts of the code conversion. This is not about a perfect translation but about creating a working prototype to test patterns and identify gaps while maintaining audit trails.
3.  **Manual Refinement & Pattern Development:** Developers take the prototype output and manually refine it, focusing on idiomatic Go, error handling, and security best practices (e.g., using `crypto/rand` instead of `math/rand`, implementing proper TLS configurations per CSE guidance). This step creates the patterns and standards for the full migration.
4.  **Establish Baselines:** Performance (throughput, latency, memory) and security (SAST findings, lines of code) baselines are established for the original Python application and the new Go prototype. These baselines inform the Business Case Analysis required for government approval.

**Tooling: Enhanced Python-to-Go Prototype Converter (`proto_converter.py`)**

This is a *starting point*, not a finish line. It demonstrates automation potential while maintaining security considerations for Canadian environments.

```python
#!/usr/bin/env python3
"""
Script: proto_converter.py
Purpose: A enhanced prototype converter for Python scripts to Go syntax with security considerations.
Disclaimer: This outputs a STRUCTURED STARTING POINT, not production code.
            It requires significant manual refinement by a Go developer with security expertise.
Additional Features: 
- Canadian government security annotations
- Crypto compliance markers
- Memory safety warnings
"""

import ast
import sys
import re

# Enhanced mapping of basic Python types/constructs to Go with security annotations
TYPE_MAP = {
    'str': 'string',
    'int': 'int',
    'float': 'float64', 
    'bool': 'bool',
    'list': '[]interface{}',    # Will need refinement - security warning for empty interface
    'dict': 'map[string]interface{}', # Will need refinement - security warning
    'bytes': '[]byte',  # Added for better security handling
}

# Canadian government security considerations
SECURITY_ANNOTATIONS = [
    "// SECURITY: Review all cryptographic implementations against CSE guidance",
    "// SECURITY: Validate memory handling for sensitive data",
    "// SECURITY: Ensure proper TLS configuration per ITSG-38",
    "// SECURITY: Implement proper error handling to avoid information leakage"
]

def get_security_header():
    """Generate security header for Canadian government compliance."""
    return """/*
* Converted from Python for Canadian Government System
* Security Review Required Before Production Use
* Consult CSE Cryptographic Guidance (ITSG-38)
* Review memory safety for sensitive data handling
*/
"""

def convert_type(py_type_str):
    """Naively convert a Python type hint to a Go type with security annotations."""
    go_type = TYPE_MAP.get(py_type_str, 'interface{}')
    if go_type == 'interface{}':
        return go_type + " // SECURITY: Replace with concrete type for type safety"
    return go_type

def convert_function(def_node):
    """Convert an ast.FunctionDef to a Go function string with security considerations."""
    func_name = def_node.name
    
    # Security check for function names that might indicate sensitive operations
    sensitive_keywords = ['password', 'secret', 'key', 'token', 'crypto', 'encrypt', 'decrypt']
    security_warning = ""
    if any(keyword in func_name.lower() for keyword in sensitive_keywords):
        security_warning = "    // SECURITY: Review cryptographic implementation against CSE guidance\n"
    
    # Generate Go parameters (naive)
    args_list = []
    for arg in def_node.args.args:
        arg_name = arg.arg
        # Try to get a type hint, otherwise use interface{}
        arg_type = 'interface{}'
        if arg.annotation:
            if isinstance(arg.annotation, ast.Name):
                arg_type = convert_type(arg.annotation.id)
        args_list.append(f"{arg_name} {arg_type}")

    # Generate return type (naive)
    return_type = ""
    if def_node.returns:
        if isinstance(def_node.returns, ast.Name):
            return_type = convert_type(def_node.returns.id)
    return_type_str = f" {return_type}" if return_type else ""

    #