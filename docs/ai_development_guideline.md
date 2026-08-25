# Ariba AI — AI Development Guideline

These are the core AI commands and the fundamental development rules that guide the design and architecture of Ariba AI. During development, every command should maintain clear responsibility, specify allowed tools, enforce output formats, and adhere strictly to safety rules.

## Core AI Commands

### 1. `/scan` — System Investigation

**Purpose:** Full Linux system health and problem investigation.

```text
/scan
/scan nginx
/scan docker
/scan --deep
```

**AI Workflow:**
```text
User Request → Identify target → Create investigation plan → Collect evidence → Analyze → Find root cause → Severity → Recommendation
```

**Can collect:**
* CPU
* RAM
* Disk
* Processes
* Services
* Network
* Docker
* System logs
* Failed services

**Default:** Read-only.

---

### 2. `/status` — System Health

Quick health overview focusing on fast data collectors rather than deep AI reasoning.

```text
/status
```

**Output Example:**
```text
System Health

CPU       ✓ 23%
Memory    ✓ 61%
Disk      ⚠ 82%
Load      ✓ 1.42
Docker    ✓ Running
Nginx     ✓ Running
SSH       ✓ Running

Overall: GOOD
```

---

### 3. `/logs` — Log Analysis

```text
/logs
/logs nginx
/logs ssh
/logs docker
/logs --last 1h
```

**AI Workflow:**
```text
Collect → Parse → Filter noise → Detect errors → Correlate events → Explain root cause
```

**Special focus areas:**
* Errors and warnings
* Authentication failures
* Service failures
* Repeated events
* Timestamp correlation

---

### 4. `/docker` — Docker Assistant

```text
/docker
/docker status
/docker logs nginx
/docker health
/docker cleanup
```

**Inspections using:**
`docker ps`, `docker ps -a`, `docker stats`, `docker images`, `docker system df`, `docker logs`

**AI Output Example:**
```text
Docker Health: WARNING

Container: postgres
Status: unhealthy

Likely cause:
Database connection failure.

Recommendation:
Check PostgreSQL logs.
```

*Note: Destructive Docker commands require explicit confirmation.*

---

### 5. `/network` — Network Diagnostics

```text
/network
/network ports
/network dns
/network route
/network connectivity
```

**Tools used:**
`ip`, `ss`, `ping`, `dig`, `resolvectl`, `traceroute`

**Potential analysis:**
DNS, Routing, Listening ports, Connectivity, Interface status, Packet loss.
*Security-sensitive scans require explicit scope/authorization.*

---

### 6. `/security` — Security Assistant

This is one of the most powerful modules in Ariba.

```text
/security
/security audit
/security ports
/security users
/security ssh
/security permissions
```

**Possible checks:**
SSH configuration, Failed logins, Listening services, Suspicious processes, File permissions, Firewall status, Users, Sudo configuration, Package updates.

**Output Example:**
```text
Security Score: 78/100

HIGH
└── SSH permits password authentication

MEDIUM
└── 3 unnecessary listening services

LOW
└── 14 packages have available updates
```

*Important: Default is defensive/local assessment. Network/VAPT functionalities must enforce explicit scope and authorization.*

---

### 7. `/tools` — Tool Registry

```text
/tools
```

**Output Example:**
```text
Available Tools

System
  ✓ cpu
  ✓ memory
  ✓ disk
  ✓ processes

Services
  ✓ systemd
  ✓ nginx
  ✓ ssh

Containers
  ✓ docker

Network
  ✓ ip
  ✓ ss
  ✓ dig

Security
  ✓ firewall
  ✓ users
  ✓ permissions
```

(e.g., `/tools nginx` shows only Nginx-related tools.)

---

### 8. `/model` — AI Model

```text
/model
```

**Output Example:**
```text
Ariba AI Model

Provider: OpenAI
Model: GPT
Status: ● Connected

Context: 128K
Temperature: 0.2
```

**Switch providers:**
`/model ollama`, `/model openai`, `/model gemini`

**Architecture Principle:**
The "Ariba Brain" must remain provider-agnostic and avoid coupling to any specific LLM provider.

---

### 9. `/history` — Previous Sessions

```text
/history
```

**Example:**
```text
Today
10:32  nginx investigation
09:45  disk analysis

Yesterday
18:22  SSH configuration
```

Using `/history 10:32` retrieves the full investigation context.

---

### 10. `/config` — Ariba Configuration

```text
/config
```

**Sections:**
AI Provider, API Key, Model, Default Mode, Allowed Tools, Safety Policy, Log Limits, Context Limits, Telemetry.

**Example:**
```text
Provider: OpenAI
Mode: SAFE
Auto Execute: OFF
Telemetry: OFF
Max Log Size: 2 MB
```

*API keys must never be output in plaintext.*

---

### 11. `/help` — Help

```text
/help
```

Displays available commands (System, Diagnostics, Security, AI, Configuration).
Contextual help (e.g., `/help /docker`) shows specific module details.

---

## 🧠 The 10 AI Development Rules

These 10 core principles govern Ariba AI's architecture and operational safety, ensuring the tool remains highly professional and secure.

### Rule 1 — Evidence First
The AI must gather system evidence before making any assumptions or answering.
✅ **Collect → verify → analyze → answer**
❌ *AI guess → answer*

### Rule 2 — Tool Permission
Every tool operates under specific permissions:
`READ`, `WRITE`, `DESTRUCTIVE`, `NETWORK`, `PRIVILEGED`

### Rule 3 — Safe by Default
**Default Mode:** `SAFE`
**Auto execution:** `OFF`

### Rule 4 — Explain Before Action
Before executing any state-changing action, the AI must provide:
1. Problem
2. Cause
3. Proposed action
4. Risk
5. Expected result

### Rule 5 — Verify After Action
If an action is executed, it must be verified. Simply stating "command successful" is not enough.
**Execute → Verify → Report**

### Rule 6 — Least Privilege
Ariba will request and use only the permissions minimally required to perform a task.

### Rule 7 — Sensitive Data Protection
Before sending data to the AI API, all sensitive information must be masked:
* Passwords, API keys, Private keys, Tokens, Cookies, Secrets, Personal data

### Rule 8 — Context Limit
Do not blindly send entire `/var/log` or `/etc` directories to the AI.
**Request → Relevant files → Relevant lines → Filtered context → AI**

### Rule 9 — Provider Independent
The Ariba Brain must never depend directly on provider-specific (e.g., OpenAI-specific) logic.
**Ariba Brain → AI Provider Interface → OpenAI / Gemini / Claude / Ollama**

### Rule 10 — Human Control
The ultimate guiding principle of Ariba's architecture:
> **AI suggests; policy decides; user controls.**
