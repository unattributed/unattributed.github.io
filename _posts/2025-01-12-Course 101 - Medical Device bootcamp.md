---
layout: post
title: "Course --- 5-Day Healthcare Cybersecurity Boot Camp, Medical Device Security"
author: unattributed
date: 2025-01-12
categories: [eLearning]
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

| Control Area      | ISO 81001 Requirements                          | NHS CyberEssentials               | FDA Guidance                          | Radiotherapy Implementation                     |
|-------------------|------------------------------------------------|-----------------------------------|---------------------------------------|-------------------------------------------------|
| Access Control    | 5.3.1: Role-based access for clinical functions | Control 4: User privilege management | Section IV.B: Authentication for treatment changes | DICOM AE Title whitelisting + Active Directory integration |
| Cryptography      | 5.3.2: TLS 1.2+ for network communications     | Control 2: Secure configuration    | Section VI.C: Encryption of PHI in transit | DICOM TLS with AES-256 and certificate-based authentication |
| Audit Logging     | 5.3.4: Log all treatment plan modifications    | Control 3: Malware protection      | Section V.D: Detect unauthorized changes | Syslog integration with SIEM for treatment plan changes |

**Implementation Examples for Radiotherapy Systems:**
1. **DICOM Security:** Configure Orthanc server with TLS 1.3 using DICOM Supplement 142 Basic TLS Profile.
2. **User Access:** Implement CyberEssentials Control 4 by integrating Mosaiq with Okta for MFA.
3. **Patch Management:** Automated Windows updates for treatment planning workstations per FDA Section VII.

### Healthcare Standards & Architecture

**DICOM Security (Supplement 142)**

| Profile       | Security Requirements                          | TLS Configuration                          |
|---------------|-----------------------------------------------|--------------------------------------------|
| Basic TLS     | Mandatory: Server authentication<br>Optional: Client authentication | TLS 1.2+ with AES-128<br>Certificate chain validation |
| Enhanced TLS  | Mandatory: Mutual authentication<br>Secure cipher suites | TLS 1.3 preferred<br>ECDHE key exchange<br>OCSP stapling |

**SMART on FHIR Security Framework**

| Component | Requirement                          | Implementation               |
|-----------|--------------------------------------|-------------------------------|
| OAuth 2.0 | Authorization Code Flow with PKCE    | Azure AD or Okta integration  |
| Scopes    | Least privilege access               | `patient/*.read` for viewing only |

**2020 Elekta Vulnerabilities Case Study**

| CVE          | Vulnerability                     | Impact                          | Mitigation                          |
|--------------|-----------------------------------|---------------------------------|-------------------------------------|
| CVE-2020-6975| Hard-coded credentials in MOSAIQ  | Unauthorized access to patient data | Credential rotation + HSM integration |
| CVE-2020-6977| DICOM service DOS                 | Treatment delays                | Rate limiting + AE title validation |

### Threat Modeling Practice

**STRIDE Analysis for Radiotherapy System**

| Component     | Spoofing          | Tampering               | Repudiation       | Information Disclosure | DOS           | Elevation of Privilege |
|---------------|-------------------|-------------------------|-------------------|------------------------|---------------|------------------------|
| DICOM Node    | Fake AE titles    | Modified treatment plans | No logs of changes | Unencrypted PHI        | Flood C-STORE | Admin via DIMSE        |
| Web Interface | Session hijacking | SQL injection           | -                 | IDOR                   | Brute force login | XSS to admin           |

**Mini Security Risk Management Report**

| Risk                                   | Severity        | Mitigation                          | Standard Reference   |
|----------------------------------------|-----------------|-------------------------------------|----------------------|
| Unauthorized treatment plan modification | Critical (CVSS 9.1) | Digital signatures with HSM      | ISO 81001 5.3.3      |
| DICOM DOS attack                       | High (CVSS 7.5) | Rate limiting + AE title validation | NHS CE Control 1     |
| PHI leakage via FHIR                   | Medium (CVSS 5.3) | OAuth scopes + audit logging     | FDA Section IV       |

---

## Day 2: Secure SDLC & Technical Documentation

### Security Documentation Practice

**Medical Device Documentation Requirements**

| Document                | Standard          | Template Structure                          | Example Content                          |
|-------------------------|-------------------|---------------------------------------------|------------------------------------------|
| Vulnerability Management SOP | FDA Postmarket | 1. Scope<br>2. Roles<br>3. Process<br>4. Timelines<br>5. Reporting | "Critical CVEs patched within 7 days per NHS CE" |
| SBOM                    | OWASP CycloneDX   | 1. Metadata<br>2. Components<br>3. Dependencies<br>4. Vulnerabilities | "pydicom 2.3.0 (CVE-2022-2534)"          |
| SOUP Management         | IEC 62304         | 1. Identification<br>2. Risk Assessment<br>3. Monitoring<br>4. Updates | "OpenSSL: Critical, used for DICOM TLS"  |

**Security Risk Management Report Template**
```markdown
1. Executive Summary
   - System: Cloud-connected radiotherapy planning
   - Scope: DICOM, FHIR, and treatment plan storage

2. Risk Assessment Methodology
   - Standards: ISO 14971, ISO 81001
   - Tools: Threat Dragon, Microsoft TMT

3. Identified Risks
   | Risk ID | Description               | Severity | Mitigation          |
   |---------|---------------------------|----------|---------------------|
   | R-001   | Unauthorized plan modify  | Critical | HSM signatures      |

4. Residual Risk Evaluation
   - Justification for acceptable risks

5. Appendices
   - STRIDE diagrams
   - Testing results
```

### Security Testing Tools

**SAST/DAST/SCA Command Reference**

| Tool          | Command                                      | Output Analysis                          | Medical Device Example                  |
|---------------|----------------------------------------------|------------------------------------------|-----------------------------------------|
| SonarQube     | `sonar-scanner -Dsonar.projectKey=RTPlan`    | Check for hardcoded credentials in DICOM config | Verify AE titles aren't hardcoded       |
| OWASP ZAP     | `zap-cli quick-scan -s xss,sqli https://rtp-web` | Review FHIR API injection flaws         | Test patientId parameter for IDOR       |
| Dependency-Check | `dependency-check.sh --project RTPlan --scan /src` | Flag vulnerable DICOM libraries        | Check pydicom for known CVEs            |

**Medical Device Code Review Findings**

| Vulnerability    | Code Example                          | Fix                          | Standard Reference   |
|------------------|---------------------------------------|------------------------------|----------------------|
| DICOM injection  | `dcmsnd +P +sd "*.dcm"`              | Validate AE titles           | DICOM PS3.15         |
| FHIR IDOR        | `/Patient/{id}/TreatmentPlan`         | Add scope checks             | SMART on FHIR        |

---

## Day 3: Penetration Testing & Vulnerability Management

### Medical Device Testing Frameworks

**Medical Device Penetration Testing (MD-PT)**

| Phase       | Activities                          | Radiotherapy Focus           | Tools               |
|-------------|-------------------------------------|------------------------------|---------------------|
| Planning    | Define clinical impact scenarios    | Treatment plan integrity     | Threat Dragon       |
| Discovery   | DICOM service enumeration          | AE title brute force         | dcmtk, nmap         |
| Exploitation| DICOM file injection               | Malformed RT Plan objects    | dcmodify, pydicom   |

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

| Test                | Command                                      | Expected Result                          | Security Control          |
|---------------------|----------------------------------------------|------------------------------------------|---------------------------|
| TLS Verification    | `openssl s_client -connect ip:port -showcerts` | TLS 1.2+ with strong cipher             | DICOM Suppl. 142          |
| AE Title Validation | `findscu -aet HACKER -aec TARGET -P -k 0008,0052="PATIENT"` | Reject unauthorized AE           | NHS CE Control 4          |
| DICOM File Validation | `dcmftest malicious.dcm`                  | Reject malformed files                  | FDA Section VI            |

**Penetration Test Report Excerpt**

| Finding            | Risk           | Evidence               | Recommendation                          |
|--------------------|----------------|------------------------|-----------------------------------------|
| Unencrypted DICOM  | High (CVSS 7.4)| Wireshark capture      | Implement DICOM TLS per Suppl. 142      |

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

| Stage    | Action                          | Medical Device Example                  |
|----------|---------------------------------|-----------------------------------------|
| PR Check | `- uses: shiftleft/scan-action@v1` | Block PR if SAST finds DICOM hardcoding |
| Build    | `- run: dependency-check --failOnCVSS 8` | Fail build if critical CVE in SBOM      |

### Communication & Interview Prep

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

| Area        | Key Points                          | Radformation Alignment                  |
|-------------|-------------------------------------|-----------------------------------------|
| Standards   | ISO 81001 5.3, NHS CE Controls 1/4, FDA Postmarket | Global compliance for cancer care products |
| Technical   | DICOM TLS, FHIR scopes, Treatment plan integrity | Directly relevant to their products    |
| Behavioral  | STAR method with metrics            | Show impact on patient safety           |
```
