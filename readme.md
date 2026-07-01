# 🛡️ Local WPCTF (V1.1.3)

## 🎯 Overview

Local WPCTF is a modular **Web Application Security Assessment Framework** designed for structured security assessment, attack surface modeling, validation, security analytics, and AI-assisted security reasoning.

This version introduces the first **hybrid integration layer between rule-based scanning, external pentesting engine execution, and LLM-based security analysis**, marking the transition toward AI-assisted security intelligence.

---

# 🧠 Design Philosophy

The framework evolves while preserving its core principles:

- Clean Architecture
- Single Responsibility Principle
- Modular Design
- Framework Agnostic
- Security Reasoning over Signature Detection
- AI-assisted analysis

---

# 🧠 Major Enhancement (V1.1.3)

## 🤖 AI Security Layer Integration

Local WPCTF now integrates a **local LLM reasoning layer** via LM Studio-compatible OpenAI API interface.

Capabilities:

- Vulnerability interpretation using LLM reasoning
- Bilingual security analysis (English + Chinese)
- Attack vector explanation generation
- Mitigation suggestion synthesis
- Structured scan result understanding

---

## ⚙️ PentestAgent Integration

External PentestAgent engine is now integrated into the pipeline.

Functionality:

- Executes automated penetration testing workflows
- Supports full-mode scanning execution
- Acts as external security execution engine

---

## 🔗 Hybrid Security Pipeline

```text
Scanners + PentestAgent
        ↓
Attack Surface Construction
        ↓
Attack Graph Generation
        ↓
LLM Security Analysis
        ↓
Risk Analytics Engine
        ↓
Report Generation
```

---

# 🧱 Updated Architecture Layer

```text
                    Local WPCTF

        ┌─────────────────────────────┐
        │            Core             │
        │ Context • Classification    │
        │ Schema                      │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │          Scanner            │
        │ Discovery • Enumeration     │
        │ Technology Detection        │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │      PentestAgent Layer     │
        │ External Execution Engine   │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │         Workflow            │
        │ Attack Surface              │
        │ Attack Graph                │
        │ Test Plan                   │
        │ Validation Planning         │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │     AI Analysis Layer       │
        │ LLM Reasoning Engine        │
        │ Security Interpretation     │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │         Analysis            │
        │ Risk • Coverage • Posture   │
        │ Validation                  │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │          Reports            │
        │ JSON • Dashboard • OWASP    │
        └─────────────────────────────┘
```

---

# 🚀 Enhanced Pipeline Flow

```text
Configuration
      │
      ▼
Scanner Pipeline
      │
      ▼
PentestAgent Execution Layer
      │
      ▼
Application Context
      │
      ▼
Application Classification
      │
      ▼
Attack Surface Construction
      │
      ▼
Attack Graph Generation
      │
      ▼
LLM Security Analysis
      │
      ▼
Test Plan Generation
      │
      ▼
Validation Execution
      │
      ▼
Security Analytics
      │
      ▼
Report Generation
```

---

# 🧠 AI Security Capabilities

## 🤖 LLM-Based Analysis

- Scan result interpretation
- Vulnerability classification
- Risk scoring (0–10)
- Attack vector reasoning
- Mitigation suggestions
- Bilingual output (EN + CN)

---

## ⚙️ PentestAgent Execution

- External security testing engine integration
- Automated attack workflow execution
- Full-mode penetration testing support

---

# 📊 Analysis Enhancements

- LLM-assisted scan interpretation
- Semantic vulnerability enrichment
- AI reasoning overlay on scan data
- Structured security understanding layer

---

# 📄 Reporting Enhancements

Added:

- `llm_analysis` field
- AI-enhanced vulnerability reasoning layer

Reports now include:

- Scan results
- Attack surface graph
- AI reasoning output
- Risk analytics

---

# 🧱 Architecture Evolution

## Before v1.1.3

```text
Scanners → Analysis → Report
```

## After v1.1.3

```text
Scanners + PentestAgent
        ↓
Attack Surface Graph
        ↓
LLM Reasoning Layer
        ↓
Risk Engine
        ↓
Report
```

---

# ⚠️ Current Limitations

- LLM does not yet control scanning decisions
- PentestAgent operates independently (non-agentic mode)
- Attack graph is not yet AI-generated
- No autonomous exploit reasoning yet

---

# 🔮 Roadmap

## V1.1.4

- LLM-driven attack prioritization
- Structured JSON LLM output
- Graph-aware reasoning integration

## V1.1.5

- AI-controlled PentestAgent orchestration
- Adaptive scanning workflows
- Enhanced exploit simulation

## V1.2

- Full AI Security Agent architecture
- Autonomous attack path generation
- Self-directed security testing loops

---

# 🎯 Project Vision

Local WPCTF is evolving from a structured security framework into an **AI-augmented security intelligence system**.

> From security scanning → to AI-driven security reasoning systems