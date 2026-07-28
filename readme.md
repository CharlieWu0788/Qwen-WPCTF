# 🛡️ Local WPCTF (V1.2.1)

## 🎯 Overview

Local WPCTF v1.2.0 introduces a major architectural upgrade by adding a **Preflight System (Target Preparation Layer)**, which decouples target resolution, profile selection, scanner configuration, and environment validation from the core scanning pipeline.

The framework evolves toward a modular security reasoning system while maintaining deterministic execution and strict separation of concerns.

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

# 🧠 Major Enhancement (V1.2.1)

## 🤖 Preflight System

The Preflight System is the core preparation layer before pipeline execution. It ensures that all required execution context is properly resolved and validated prior to security scanning.

This layer is responsible for:

- Target resolution (supports both numeric IDs and string-based aliases)
- Profile mapping (associates targets with predefined security profiles)
- Scanner selection (derives scanner sets from profile configuration)
- Environment validation (verifies target reachability and accessibility)
- Context construction (builds unified `TargetContext` consumed by downstream pipeline)

The Preflight System guarantees that the scanning pipeline operates on a fully resolved and validated execution context, eliminating direct dependency on configuration sources.

---

# 🧱 Updated Architecture Layer

```text
 Local WPCTF

        ┌─────────────────────────────┐
        │            Core             │
        │ Context • Classification    │
        │ Schema • Utilities          │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │          Scanner            │
        │ Discovery • Enumeration     │
        │ Plugin-based Detection      │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │      Execution Layer        │
        │ Scanner Orchestration       │
        │ (PentestAgent Integration)  │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │         Workflow            │
        │ Attack Surface              │
        │ Attack Graph                │
        │ Test Planning               │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │        Analysis Layer       │
        │ Risk • Coverage • Posture   │
        │ Validation                  │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │     LLM Enrichment Layer    │
        │ Security Reasoning          │
        │ Vulnerability Interpretation│
        │ Narrative Generation        │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │          Reports            │
        │ JSON • Markdown • OWASP     │
        └─────────────────────────────┘
```

---

# 🚀 Enhanced Pipeline Flow

```text
Configuration (Target Selector)
      │
      ▼
Preflight System
      │
      ▼
Scanner Execution Layer
      │
      ▼
Application Context Construction
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
Test Plan Generation
      │
      ▼
Validation Execution
      │
      ▼
Analysis Layer (Risk / Coverage / Posture)
      │
      ▼
LLM Enrichment Layer
      │
      ▼
Report Generation
```

---

# ⚙️ Capabilities

## 🔌 Scanner System

The scanner system is fully plugin-based and registry-driven.

Key characteristics:

- Modular scanner plugins
- Centralized registry execution
- Deterministic execution order
- Schema-enforced outputs (safe_wrap)

Each scanner operates independently and returns structured results without shared mutable state.

---

##  ⚙️ Execution Layer

The Execution Layer is responsible for orchestrating scanner execution.

It provides:

- Deterministic scanner orchestration
- Registry-based plugin execution
- Integration capability with external execution engines (PentestAgent-compatible design)

Note: This layer is not agentic and does not perform autonomous decision-making.

---

## 📊 AnalysisLayer

The Analysis Layer transforms raw scan outputs into structured security intelligence.

It includes:

- Coverage analysis
- Risk scoring
- Security posture evaluation  
- Validation completeness assessment

All outputs are deterministic and schema-driven.

---

## 🤖 LLM Enrichment Layer

The LLM Enrichment Layer provides semantic interpretation over deterministic security results.

Capabilities include:

- Vulnerability interpretation
- Attack vector reasoning
- Risk narrative generation
- Mitigation recommendations
- Bilingual output (English + Chinese)          

The LLM layer does not control execution flow.

# 📄 Reporting Enhancements

Local WPCTF now supports dual-output reporting:

## Structured Report (JSON)

Machine-readable format
Used for automation, dashboards, and downstream processing

```text
output/report.json
```

## LLM Report (Markdown)

Human-readable security analysis
Narrative-based vulnerability explanation
Security reasoning summary

```text
output/llm_analysis.md
```

---

# 🧱 Architecture Evolution

## Before v1.1.x

```text
Scanners → Analysis → Report
```

## After v1.2.0

```text
Preflight → Scanner Execution → Workflow → Analysis → LLM Enrichment → Report
```

---

# ⚠️ Current Limitations

- LLM does not control execution flow
- No autonomous decision-making loop exists
- PentestAgent is execution-oriented, not agentic
- Attack graph is not AI-generated
- No adaptive scanning strategy yet

---

# 🔮 Roadmap

## v1.2.1
- LLM-driven attack prioritization
- Structured reasoning output standardization
- Attack graph enrichment layer

## v1.3
- AI-assisted execution orchestration
- Adaptive scanning workflows
- Tool-use based PentestAgent evolution

## v2.0
- Full AI Security Agent architecture
- Autonomous attack path generation
- Closed-loop reasoning system

---

# 🎯 Project Vision

Local WPCTF is evolving into a modular AI-assisted security reasoning framework.

It bridges deterministic security scanning with structured LLM-based interpretation, enabling scalable and extensible security analysis pipelines.

From security scanning → to structured security intelligence

> From security scanning → to AI-driven security reasoning systems