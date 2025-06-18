---
layout: post
title: "Primer - Privacy focused Messaging"
date: 2025-05-13
author: unattributed
categories: [secure-coms]
tags: [signal, whatsapp, element, session, threema, wire, detla-chat, secure-messaging, privacy]
---

# **Secure Messengers: A Privacy-Focused Guide for Researchers, Journalists, and any joe**  

In an era of mass surveillance, selecting a secure messaging application is crucial for cybersecurity professionals, journalists, and free speech advocates. While mainstream apps like **WhatsApp** and **Signal** are widely used, alternatives such as **Element (Matrix), Session, Threema, Wire, and Delta Chat** offer varying degrees of privacy and security. This article evaluates these platforms based on **encryption standards, metadata protection, perfect forward secrecy (PFS), post-compromise security (PCS), and plausible deniability**. We also examine **data leakage risks**—both from platform vulnerabilities and device seizures—and discuss **Android Private Spaces** as a method to enhance security.  

---  

## **Key Security & Privacy Features**  

### **1. End-to-End Encryption (E2EE)**  
All listed apps support E2EE, but implementations differ:  
- **Signal, WhatsApp, Wire**: Use the **Signal Protocol**, the gold standard for E2EE.  
- **Session**: Uses a modified **Oxen Protocol** (based on Signal) and operates without phone numbers.  
- **Threema**: Uses **NaCl (libsodium) encryption** and allows fully anonymous registration.  
- **Element (Matrix)**: Supports E2EE via **Olm/Megolm**, an implementation of the Double Ratchet algorithm.  
- **Delta Chat**: Relies on **Autocrypt (PGP-based)**, which lacks forward secrecy but integrates with email.  

### **2. Metadata Protection**  
Metadata (who you communicate with, when, and for how long) is often more revealing than message content.  
- **Signal**: Minimal metadata retention but requires a phone number.  
- **Session**: No identifiers (uses random Session IDs); decentralized via the Oxen network.  
- **Threema**: No phone/email required; minimal metadata collection.  
- **Element**: Self-hostable, but metadata retention depends on server configuration.  
- **WhatsApp**: Collects extensive metadata (contacts, timestamps, IPs), shared with Meta and, under legal pressure, authorities.  

### **3. Perfect Forward Secrecy (PFS)**  
PFS ensures past messages remain secure even if long-term keys are compromised.  
- **Signal, WhatsApp, Wire, Session, Element**: All implement PFS via the Double Ratchet algorithm.  
- **Delta Chat (PGP)**: Lacks PFS—compromised keys can decrypt past messages.  

### **4. Post-Compromise Security (PCS)**  
PCS ensures that if a device is compromised, future messages regain security after key renegotiation.  
- **Signal, WhatsApp, Wire, Session, Element**: Provide strong PCS.  
- **Threema**: Supports PCS but relies on manual key updates.  

### **5. Plausible Deniability**  
Some apps allow users to deny sending a message.  
- **Signal/WhatsApp**: No deniability—messages are cryptographically signed.  
- **Session/Threema/Wire**: Offer some deniability features (e.g., no signing proofs).  
- **Element**: Editable/deletable messages across devices can aid deniability.  

---  

## **Android Private Spaces: Enhanced Isolation for Secure Messaging**  

Android’s **Private Space** (or **Work Profile** on some devices) allows users to create a separate, encrypted container for apps and data. Installing a secure messenger within this space provides additional security benefits:  

### **Key Features & Benefits**  
- **Isolated Storage**: Messaging apps and their data are sandboxed, preventing other apps from accessing them.  
- **Separate Identity**: You can create a new Google account (or none at all) for the Private Space, reducing cross-app tracking.  
- **Enhanced Encryption**: Private Space data is encrypted separately from the main device storage.  
- **Hidden from Main Profile**: Apps in Private Space do not appear in the main app drawer unless unlocked.  

### **Practical Use Cases**  
- **Journalists**: Maintain separate identities for sensitive sources.  
- **Activists**: Shield communications from device-wide malware or forensic extraction.  
- **Researchers**: Test apps in a controlled environment without contaminating primary data.  

**Note**: While Private Spaces improve security, they do not protect against **device seizure and hardware-level decryption** (discussed below).  

---  

## **Device Seizure Risks: Local Data & Hardware Vulnerabilities**  

Even with strong encryption, local data storage remains a risk. State and state-sponsored actors may employ:  

### **1. Forensic Extraction Tools**  
Tools like **Cellebrite** and **GrayKey** can extract data from locked devices by exploiting vulnerabilities in device encryption or bypassing passcode attempts.  

### **2. Cloud Backups (iCloud/Google Drive)**  
- **Signal/WhatsApp**: Encrypted, but if backups are enabled, they may be accessible via subpoena.  
- **Session/Threema**: No reliance on cloud backups by default.  

### **3. Cold Boot Attacks & Hardware Exploits**  
Advanced adversaries may use:  
- **Cold boot attacks**: Extracting encryption keys from RAM.  
- **JTAG/ISP extraction**: Directly reading flash memory.  

### **Mitigation Strategies**  
- **Disable Cloud Backups**: For Signal/WhatsApp, disable iCloud/Google Drive backups.  
- **Use Self-Destructing Messages**: Apps like Session allow auto-deletion.  
- **Full-Disk Encryption (FDE)**: Ensure FDE is enabled (Android: File-Based Encryption, iOS: Data Protection).  
- **Faraday Bags**: If at risk of seizure, store devices in Faraday bags to prevent remote wiping.  
- **Private Containers**: See next blog posting

---  

## **Anonymity: Why It Matters & How to Achieve It**  

**Session** stands out as the best option for anonymity due to:  
- **No phone number/email required** (unlike Signal/WhatsApp).  
- **Decentralized infrastructure** (Oxen network, no central servers).  
- **Onion routing** (messages are relayed through multiple nodes).  

### **Practical Anonymity Measures**  
1. **Burner Devices**: Use a secondary phone without personal data.  
2. **VPN/Tor**: Route traffic through Tor (Session does this by default).  
3. **Avoid Cross-Platform Linking**: Don’t use the same identity across services.  
4. **Metadata Minimization**: Use apps like Session or Threema that collect minimal metadata.  
5. **Isolation w/ Private Containers**: See next blog posting

---  

## **FBI & EFF Perspectives**  
- **FBI Concerns**: Leaked documents ([The Intercept](https://theintercept.com)) reveal frustration with Signal’s encryption, while WhatsApp’s metadata remains a valuable intelligence source.  
- **EFF Recommendations**: The EFF’s [Secure Messaging Scorecard](https://www.eff.org/secure-messaging-scorecard) favors **Signal, Session, and Threema** for strong encryption and metadata resistance.  

---  

## **Final Recommendations**  
- **Best for Activists/Journalists**: **Signal** (if phone number is acceptable), **Session** (for full anonymity).  
- **Enterprise/Team Use**: **Element** (self-hostable, interoperable).  
- **High-Risk Scenarios**: **Threema** (paid, no identifiers) or **Session** (fully anonymous).  
- **Avoid for Sensitive Comms**: **WhatsApp** (metadata risks), **Delta Chat** (no PFS).  

### **Bottom Line**  
No messenger is 100% secure, but combining **minimal metadata apps, Android Private Spaces, and strong operational security (OPSEC)** reduces exposure. Stay informed, as security features and threats evolve.  

**Further Reading:**  
- [EFF Surveillance Self-Defense](https://ssd.eff.org)  
- [Signal’s Technical Documentation](https://signal.org/docs/)  
- [The Intercept: FBI & Encrypted Messaging](https://theintercept.com)  

Stay secure, stay informed.

[Back to Top](#secure-messengers-a-privacy-focused-guide-for-researchers-journalists-and-any-joe)