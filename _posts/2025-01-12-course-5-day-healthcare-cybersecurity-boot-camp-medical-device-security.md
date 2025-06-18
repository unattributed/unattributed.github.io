---
layout: post
title: "Course: 5-Day Healthcare Cybersecurity Boot Camp, Medical Device Security"
date: 2025-01-12
author: unattributed
categories: [elearning]
tags: [soc, bootcamp, medical]
---

# 5-Day Intensive Prep Healthcare Cybersecurity Boot Camp  
**Transitioning from SOC to Medical Device Security**

## 🚀 Course Overview  
A 5-day intensive program designed to help **junior SOC analysts** transition into **medical device and healthcare cybersecurity roles**. Gain hands-on experience with healthcare-specific security frameworks, threat modeling, and penetration testing techniques.  

## 🎯 Key Learning Objectives  
- **Master healthcare security standards**: ISO 81001, FDA guidance, NHS CyberEssentials  
- **Develop threat modeling skills**: STRIDE analysis for medical devices  
- **Execute medical device pentesting**: DICOM security testing, FHIR API security  
- **Implement secure SDLC**: SAST/DAST, SBOM management, vulnerability patching  
- **Communicate security risks**: Tailor messages for executives, regulators, and developers  

## 🧑‍💻 Who Should Attend?  
- SOC analysts targeting **healthcare cybersecurity roles**  
- Junior security professionals interested in **medical device security**  
- Candidates preparing for **security interviews in regulated industries**  

## 🏆 Program Outcomes  
By completing this boot camp, participants will:  
✔ Understand healthcare-specific security requirements  
✔ Be able to conduct medical device security assessments  
✔ Have practical experience with healthcare security tools  
✔ Be prepared for junior analyst roles in medical device security  

**Duration**: 5 days | **Level**: Intermediate | **Format**: Hands-on labs, case studies, interview prep  

## Day 1: Medical Device Security Foundations

### Regulatory Standards Comparison


<table>
   <table style="border: 1px solid lightgrey; border-collapse: collapse;">
      <thead>
         <tr style="border: 1px solid lightgrey;">
            <th style="border: 1px solid lightgrey;">Control Area</th>
            <th style="border: 1px solid lightgrey;">ISO 81001 Requirements</th>
            <th style="border: 1px solid lightgrey;">NHS CyberEssentials</th>
            <th style="border: 1px solid lightgrey;">FDA Guidance</th>
            <th style="border: 1px solid lightgrey;">Radiotherapy Implementation</th>
         </tr>
      </thead>
      <tbody>
         <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey;">Access Control</td>
            <td style="border: 1px solid lightgrey;">5.3.1: Role-based access for clinical functions</td>
            <td style="border: 1px solid lightgrey;">Control 4: User privilege management</td>
            <td style="border: 1px solid lightgrey;">Section IV.B: Authentication for treatment changes</td>
            <td style="border: 1px solid lightgrey;">DICOM AE Title whitelisting + Active Directory integration</td>
         </tr>
         <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey;">Cryptography</td>
            <td style="border: 1px solid lightgrey;">5.3.2: TLS 1.2+ for network communications</td>
            <td style="border: 1px solid lightgrey;">Control 2: Secure configuration</td>
            <td style="border: 1px solid lightgrey;">Section VI.C: Encryption of PHI in transit</td>
            <td style="border: 1px solid lightgrey;">DICOM TLS with AES-256 and certificate-based authentication</td>
         </tr>
         <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey;">Audit Logging</td>
            <td style="border: 1px solid lightgrey;">5.3.4: Log all treatment plan modifications</td>
            <td style="border: 1px solid lightgrey;">Control 3: Malware protection</td>
            <td style="border: 1px solid lightgrey;">Section V.D: Detect unauthorized changes</td>
            <td style="border: 1px solid lightgrey;">Syslog integration with SIEM for treatment plan changes</td>
         </tr>
      </tbody>
   </table>
</table>

**Implementation Examples for Radiotherapy Systems:**
1. **DICOM Security:** Configure Orthanc server with TLS 1.3 using DICOM Supplement 142 Basic TLS Profile.
2. **User Access:** Implement CyberEssentials Control 4 by integrating Mosaiq with Okta for MFA.
3. **Patch Management:** Automated Windows updates for treatment planning workstations per FDA Section VII.

### Healthcare Standards & Architecture

**DICOM Security (Supplement 142)**

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Profile</th>
         <th style="border: 1px solid lightgrey;">Security Requirements</th>
         <th style="border: 1px solid lightgrey;">TLS Configuration</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Basic TLS</td>
         <td style="border: 1px solid lightgrey;">Mandatory: Server authentication<br>Optional: Client authentication</td>
         <td style="border: 1px solid lightgrey;">TLS 1.2+ with AES-128<br>Certificate chain validation</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Enhanced TLS</td>
         <td style="border: 1px solid lightgrey;">Mandatory: Mutual authentication<br>Secure cipher suites</td>
         <td style="border: 1px solid lightgrey;">TLS 1.3 preferred<br>ECDHE key exchange<br>OCSP stapling</td>
      </tr>
   </tbody>
</table>

**SMART on FHIR Security Framework**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Component</th>
         <th style="border: 1px solid lightgrey;">Requirement</th>
         <th style="border: 1px solid lightgrey;">Implementation</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">OAuth 2.0</td>
         <td style="border: 1px solid lightgrey;">Authorization Code Flow with PKCE</td>
         <td style="border: 1px solid lightgrey;">Azure AD or Okta integration</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Scopes</td>
         <td style="border: 1px solid lightgrey;">Least privilege access</td>
         <td style="border: 1px solid lightgrey;"><code>patient/*.read</code> for viewing only</td>
      </tr>
   </tbody>
</table>


**2020 Elekta Vulnerabilities Case Study**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">CVE</th>
         <th style="border: 1px solid lightgrey;">Vulnerability</th>
         <th style="border: 1px solid lightgrey;">Impact</th>
         <th style="border: 1px solid lightgrey;">Mitigation</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">CVE-2020-6975</td>
         <td style="border: 1px solid lightgrey;">Hard-coded credentials in MOSAIQ</td>
         <td style="border: 1px solid lightgrey;">Unauthorized access to patient data</td>
         <td style="border: 1px solid lightgrey;">Credential rotation + HSM integration</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">CVE-2020-6977</td>
         <td style="border: 1px solid lightgrey;">DICOM service DOS</td>
         <td style="border: 1px solid lightgrey;">Treatment delays</td>
         <td style="border: 1px solid lightgrey;">Rate limiting + AE title validation</td>
      </tr>
   </tbody>
</table>

### Threat Modeling Practice

**STRIDE Analysis for Radiotherapy System**

<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Component</th>
         <th style="border: 1px solid lightgrey;">Spoofing</th>
         <th style="border: 1px solid lightgrey;">Tampering</th>
         <th style="border: 1px solid lightgrey;">Repudiation</th>
         <th style="border: 1px solid lightgrey;">Information Disclosure</th>
         <th style="border: 1px solid lightgrey;">DOS</th>
         <th style="border: 1px solid lightgrey;">Elevation of Privilege</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">DICOM Node</td>
         <td style="border: 1px solid lightgrey;">Fake AE titles</td>
         <td style="border: 1px solid lightgrey;">Modified treatment plans</td>
         <td style="border: 1px solid lightgrey;">No logs of changes</td>
         <td style="border: 1px solid lightgrey;">Unencrypted PHI</td>
         <td style="border: 1px solid lightgrey;">Flood C-STORE</td>
         <td style="border: 1px solid lightgrey;">Admin via DIMSE</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Web Interface</td>
         <td style="border: 1px solid lightgrey;">Session hijacking</td>
         <td style="border: 1px solid lightgrey;">SQL injection</td>
         <td style="border: 1px solid lightgrey;">-</td>
         <td style="border: 1px solid lightgrey;">IDOR</td>
         <td style="border: 1px solid lightgrey;">Brute force login</td>
         <td style="border: 1px solid lightgrey;">XSS to admin</td>
      </tr>
   </tbody>
</table>

**Mini Security Risk Management Report**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Risk</th>
         <th style="border: 1px solid lightgrey;">Severity</th>
         <th style="border: 1px solid lightgrey;">Mitigation</th>
         <th style="border: 1px solid lightgrey;">Standard Reference</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Unauthorized treatment plan modification</td>
         <td style="border: 1px solid lightgrey;">Critical (CVSS 9.1)</td>
         <td style="border: 1px solid lightgrey;">Digital signatures with HSM</td>
         <td style="border: 1px solid lightgrey;">ISO 81001 5.3.3</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">DICOM DOS attack</td>
         <td style="border: 1px solid lightgrey;">High (CVSS 7.5)</td>
         <td style="border: 1px solid lightgrey;">Rate limiting + AE title validation</td>
         <td style="border: 1px solid lightgrey;">NHS CE Control 1</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">PHI leakage via FHIR</td>
         <td style="border: 1px solid lightgrey;">Medium (CVSS 5.3)</td>
         <td style="border: 1px solid lightgrey;">OAuth scopes + audit logging</td>
         <td style="border: 1px solid lightgrey;">FDA Section IV</td>
      </tr>
   </tbody>
</table>

## Day 2: Secure SDLC & Technical Documentation

### Security Documentation Practice

**Medical Device Documentation Requirements**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Document</th>
         <th style="border: 1px solid lightgrey;">Standard</th>
         <th style="border: 1px solid lightgrey;">Template Structure</th>
         <th style="border: 1px solid lightgrey;">Example Content</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Vulnerability Management SOP</td>
         <td style="border: 1px solid lightgrey;">FDA Postmarket</td>
         <td style="border: 1px solid lightgrey;">
            <ol>
               <li>Scope</li>
               <li>Roles</li>
               <li>Process</li>
               <li>Timelines</li>
               <li>Reporting</li>
            </ol>
         </td>
         <td style="border: 1px solid lightgrey;">"Critical CVEs patched within 7 days per NHS CE"</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">SBOM</td>
         <td style="border: 1px solid lightgrey;">OWASP CycloneDX</td>
         <td style="border: 1px solid lightgrey;">
            <ol>
               <li>Metadata</li>
               <li>Components</li>
               <li>Dependencies</li>
               <li>Vulnerabilities</li>
            </ol>
         </td>
         <td style="border: 1px solid lightgrey;">"pydicom 2.3.0 (CVE-2022-2534)"</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">SOUP Management</td>
         <td style="border: 1px solid lightgrey;">IEC 62304</td>
         <td style="border: 1px solid lightgrey;">
            <ol>
               <li>Identification</li>
               <li>Risk Assessment</li>
               <li>Monitoring</li>
               <li>Updates</li>
            </ol>
         </td>
         <td style="border: 1px solid lightgrey;">"OpenSSL: Critical, used for DICOM TLS"</td>
      </tr>
   </tbody>
</table>

**Security Risk Management Report Template**
```markdown
1. Executive Summary
   - System: Cloud-connected radiotherapy planning  
   - Scope: DICOM, FHIR, and treatment plan storage  
   2. Risk Assessment Methodology
   - Standards: ISO 14971, ISO 81001
   - Tools: Threat Dragon, Microsoft TMT
```

3. Identified Risks
   
   <table style="border: 1px solid lightgrey; border-collapse: collapse;">
      <thead>
         <tr style="border: 1px solid lightgrey;">
            <th style="border: 1px solid lightgrey;">Risk ID</th>
            <th style="border: 1px solid lightgrey;">Description</th>
            <th style="border: 1px solid lightgrey;">Severity</th>
            <th style="border: 1px solid lightgrey;">Mitigation</th>
         </tr>
      </thead>
      <tbody>
         <tr style="border: 1px solid lightgrey;">
            <td style="border: 1px solid lightgrey;">R-001</td>
            <td style="border: 1px solid lightgrey;">Unauthorized plan modify</td>
            <td style="border: 1px solid lightgrey;">Critical</td>
            <td style="border: 1px solid lightgrey;">HSM signatures</td>
         </tr>
      </tbody>
   </table>
   &nbsp; 
4. Residual Risk Evaluation
   - Justification for acceptable risks

5. Appendices
   - STRIDE diagrams
   - Testing results

### Security Testing Tools

**SAST/DAST/SCA Command Reference**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Tool</th>
         <th style="border: 1px solid lightgrey;">Command</th>
         <th style="border: 1px solid lightgrey;">Output Analysis</th>
         <th style="border: 1px solid lightgrey;">Medical Device Example</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">SonarQube</td>
         <td style="border: 1px solid lightgrey;"><code>sonar-scanner -Dsonar.projectKey=RTPlan</code></td>
         <td style="border: 1px solid lightgrey;">Check for hardcoded credentials in DICOM config</td>
         <td style="border: 1px solid lightgrey;">Verify AE titles aren't hardcoded</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">OWASP ZAP</td>
         <td style="border: 1px solid lightgrey;"><code>zap-cli quick-scan -s xss,sqli https://rtp-web</code></td>
         <td style="border: 1px solid lightgrey;">Review FHIR API injection flaws</td>
         <td style="border: 1px solid lightgrey;">Test patientId parameter for IDOR</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Dependency-Check</td>
         <td style="border: 1px solid lightgrey;"><code>dependency-check.sh --project RTPlan --scan /src</code></td>
         <td style="border: 1px solid lightgrey;">Flag vulnerable DICOM libraries</td>
         <td style="border: 1px solid lightgrey;">Check pydicom for known CVEs</td>
      </tr>
   </tbody>
</table>

**Medical Device Code Review Findings**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Vulnerability</th>
         <th style="border: 1px solid lightgrey;">Code Example</th>
         <th style="border: 1px solid lightgrey;">Fix</th>
         <th style="border: 1px solid lightgrey;">Standard Reference</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">DICOM injection</td>
         <td style="border: 1px solid lightgrey;"><code>dcmsnd +P +sd "*.dcm"</code></td>
         <td style="border: 1px solid lightgrey;">Validate AE titles</td>
         <td style="border: 1px solid lightgrey;">DICOM PS3.15</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">FHIR IDOR</td>
         <td style="border: 1px solid lightgrey;"><code>/Patient/{id}/TreatmentPlan</code></td>
         <td style="border: 1px solid lightgrey;">Add scope checks</td>
         <td style="border: 1px solid lightgrey;">SMART on FHIR</td>
      </tr>
   </tbody>
</table>


---

## Day 3: Penetration Testing & Vulnerability Management

### Medical Device Testing Frameworks

**Medical Device Penetration Testing (MD-PT)**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Phase</th>
         <th style="border: 1px solid lightgrey;">Activities</th>
         <th style="border: 1px solid lightgrey;">Radiotherapy Focus</th>
         <th style="border: 1px solid lightgrey;">Tools</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Planning</td>
         <td style="border: 1px solid lightgrey;">Define clinical impact scenarios</td>
         <td style="border: 1px solid lightgrey;">Treatment plan integrity</td>
         <td style="border: 1px solid lightgrey;">Threat Dragon</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Discovery</td>
         <td style="border: 1px solid lightgrey;">DICOM service enumeration</td>
         <td style="border: 1px solid lightgrey;">AE title brute force</td>
         <td style="border: 1px solid lightgrey;">dcmtk, nmap</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Exploitation</td>
         <td style="border: 1px solid lightgrey;">DICOM file injection</td>
         <td style="border: 1px solid lightgrey;">Malformed RT Plan objects</td>
         <td style="border: 1px solid lightgrey;">dcmodify, pydicom</td>
      </tr>
   </tbody>
</table>

**Radiotherapy System Test Cases**
1. **DICOM Service DOS:**
   ```bash
   echoscu -aet HACKER -aec TARGET -n 1000 target-ip 104
   ```
2. **Treatment Plan Tampering:**
   ```bash
   dcmodify -i "(300a,00b0)=HACKED" plan.dcm
   ```
3. **FHIR API Abuse:**
   ```bash
   curl -H "Authorization: Bearer token" /Patient/*/RTPlan
   ```

### DICOM Security Testing with dcmtk

**DICOM Security Test Commands**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Test</th>
         <th style="border: 1px solid lightgrey;">Command</th>
         <th style="border: 1px solid lightgrey;">Expected Result</th>
         <th style="border: 1px solid lightgrey;">Security Control</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">TLS Verification</td>
         <td style="border: 1px solid lightgrey;"><code>openssl s_client -connect ip:port -showcerts</code></td>
         <td style="border: 1px solid lightgrey;">TLS 1.2+ with strong cipher</td>
         <td style="border: 1px solid lightgrey;">DICOM Suppl. 142</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">AE Title Validation</td>
         <td style="border: 1px solid lightgrey;"><code>findscu -aet HACKER -aec TARGET -P -k 0008,0052="PATIENT"</code></td>
         <td style="border: 1px solid lightgrey;">Reject unauthorized AE</td>
         <td style="border: 1px solid lightgrey;">NHS CE Control 4</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">DICOM File Validation</td>
         <td style="border: 1px solid lightgrey;"><code>dcmftest malicious.dcm</code></td>
         <td style="border: 1px solid lightgrey;">Reject malformed files</td>
         <td style="border: 1px solid lightgrey;">FDA Section VI</td>
      </tr>
   </tbody>
</table>


**Penetration Test Report Excerpt**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Finding</th>
         <th style="border: 1px solid lightgrey;">Risk</th>
         <th style="border: 1px solid lightgrey;">Evidence</th>
         <th style="border: 1px solid lightgrey;">Recommendation</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Unencrypted DICOM</td>
         <td style="border: 1px solid lightgrey;">High (CVSS 7.4)</td>
         <td style="border: 1px solid lightgrey;">Wireshark capture</td>
         <td style="border: 1px solid lightgrey;">Implement DICOM TLS per Suppl. 142</td>
      </tr>
   </tbody>
</table>

---

## Day 4: Automation & Technical Leadership

### Security Automation Examples

**SBOM CVE Monitor (Python)**
```python
import requests
from datetime import datetime, timedelta

# Configuration
SBOM_FILE = "sbom.json"
SEVERITY = "CRITICAL"
NVD_API = "https://services.nvd.nist.gov/rest/json/cves/1.0"

def check_sbom_vulnerabilities():
    # Parse SBOM (CycloneDX format)
    with open(SBOM_FILE) as f:
        sbom = json.load(f)
    
    # Check components against NVD
    for comp in sbom["components"]:
        if "purl" in comp:
            pkg = comp["purl"].split("@")[0]
            res = requests.get(f"{NVD_API}?cpeMatchString={pkg}")
            
            # Process vulnerabilities
            for vuln in res.json().get("result", {}).get("CVE_Items", []):
                if vuln["impact"]["baseMetricV2"]["severity"] == SEVERITY:
                    print(f"[!] Critical CVE found: {vuln['cve']['CVE_data_meta']['ID']}")
                    print(f"    Affects: {comp['name']}@{comp['version']}")
                    print(f"    Score: {vuln['impact']['baseMetricV2']['cvssV2']['baseScore']}")

if __name__ == "__main__":
    check_sbom_vulnerabilities()
```

**GitHub Actions Security Gates**


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Stage</th>
         <th style="border: 1px solid lightgrey;">Action</th>
         <th style="border: 1px solid lightgrey;">Medical Device Example</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">PR Check</td>
         <td style="border: 1px solid lightgrey;"><code>- uses: shiftleft/scan-action@v1</code></td>
         <td style="border: 1px solid lightgrey;">Block PR if SAST finds DICOM hardcoding</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Build</td>
         <td style="border: 1px solid lightgrey;"><code>- run: dependency-check --failOnCVSS 8</code></td>
         <td style="border: 1px solid lightgrey;">Fail build if critical CVE in SBOM</td>
      </tr>
   </tbody>
</table>

**Explain TLS requirements to different audiences:**
- **Regulatory Team:** "Per ISO 81001 5.3.2 and FDA guidance, TLS 1.2+ is required to protect PHI in transit during DICOM transfers. Non-compliance could delay our 510(k) submission."
- **Executives:** "Implementing TLS prevents $2M+ breach penalties under HIPAA while meeting NHS contract requirements, with minimal performance impact."
- **Developers:** "Use OpenSSL 1.1.1+ with AES-256-GCM and certificate pinning in dcmtk configuration - here's the code sample."

**Behavioral Question: "Describe implementing security in a regulated environment"**
- **Situation:** "At [Company], our radiotherapy system needed FDA clearance with cybersecurity requirements."
- **Task:** "I led the effort to implement ISO 81001 controls for the DICOM interface."
- **Action:** "Deployed TLS 1.3 with mutual auth, threat modeled using STRIDE, and documented risk mitigations."
- **Result:** "Achieved FDA clearance 3 weeks early with zero cybersecurity findings."

---

## Final Interview Checklist


<table style="border: 1px solid lightgrey; border-collapse: collapse;">
   <thead>
      <tr style="border: 1px solid lightgrey;">
         <th style="border: 1px solid lightgrey;">Area</th>
         <th style="border: 1px solid lightgrey;">Key Points</th>
         <th style="border: 1px solid lightgrey;">Radformation Alignment</th>
      </tr>
   </thead>
   <tbody>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Standards</td>
         <td style="border: 1px solid lightgrey;">ISO 81001 5.3, NHS CE Controls 1/4, FDA Postmarket</td>
         <td style="border: 1px solid lightgrey;">Global compliance for cancer care products</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Technical</td>
         <td style="border: 1px solid lightgrey;">DICOM TLS, FHIR scopes, Treatment plan integrity</td>
         <td style="border: 1px solid lightgrey;">Directly relevant to their products</td>
      </tr>
      <tr style="border: 1px solid lightgrey;">
         <td style="border: 1px solid lightgrey;">Behavioral</td>
         <td style="border: 1px solid lightgrey;">STAR method with metrics</td>
         <td style="border: 1px solid lightgrey;">Show impact on patient safety</td>
      </tr>
   </tbody>
</table>

**Good Luck**
[Back to Top](#)