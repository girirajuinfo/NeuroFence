# 🛡️ NeuroFence
## AI-Powered LLM Backdoor & Weight Poisoning Detection Framework

![Status](https://img.shields.io/badge/Status-Under%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-AI-red)
![License](https://img.shields.io/badge/License-MIT-green)

> Detecting hidden backdoors and malicious behaviors in Large Language Models before deployment.

---

# 📌 About NeuroFence

NeuroFence is an AI Security project developed as part of the **InfoTact Cyber Security Internship**.

The project focuses on detecting hidden backdoors and weight poisoning attacks in Large Language Models (LLMs) using adversarial prompt testing, neuron activation analysis, and anomaly detection.

Instead of trusting an AI model blindly, NeuroFence analyzes how the model behaves internally and identifies suspicious activation patterns that may indicate malicious modifications.

---

# 🎯 Project Objectives

- Securely load open-source LLMs.
- Generate adversarial and fuzzed prompts.
- Capture internal neuron activation patterns.
- Detect suspicious model behavior.
- Calculate an AI security risk score.
- Generate professional security reports.
- Visualize analysis through a desktop application.

---

# 🚀 Key Features

- 🔒 Secure Model Loader
- 🧠 Prompt Fuzzer
- 📊 Activation Tracking
- ⚠️ Backdoor Detection Engine
- 📈 Risk Score Calculation
- 📄 PDF Security Report Generator
- 🖥️ PyQt6 Desktop GUI
- 📦 Offline AI Security Analysis

---

# 🏗️ System Architecture

```text
              Open Source LLM
                     │
                     ▼
          Secure Model Loader
                     │
                     ▼
        Adversarial Prompt Fuzzer
                     │
                     ▼
        Neuron Activation Tracker
                     │
                     ▼
      Detection & Risk Analysis Engine
                     │
                     ▼
        Security Report Generator
                     │
                     ▼
             Desktop Dashboard
```

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Language | Python 3.12 |
| AI Framework | PyTorch |
| LLM | Hugging Face Transformers |
| Safe Model Loading | SafeTensors |
| GUI | PyQt6 |
| Reports | ReportLab |
| Data Processing | NumPy, Pandas |
| Visualization | Matplotlib |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
NeuroFence/
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
│
├── assets/
├── docs/
├── models/
├── sandbox/
├── fuzzer/
├── tracker/
├── detector/
├── reports/
├── gui/
├── tests/
└── utils/
```

---

# 📅 Development Roadmap

## Phase 1
- Repository Setup
- Git Workflow
- Documentation

## Phase 2
- Secure Model Loader
- Sandbox Environment

## Phase 3
- Prompt Fuzzer
- Activation Tracking

## Phase 4
- Detection Engine
- Risk Scoring

## Phase 5
- GUI Development
- PDF Report Generation

## Phase 6
- Testing
- Bug Fixes
- Performance Optimization

## Phase 7
- Documentation
- Final Demonstration
- Release v1.0

---

# 📊 Current Progress

- ✅ Repository Created
- ✅ Git Branch Strategy
- ✅ Initial Project Structure
- ⏳ Secure Model Loader
- ⏳ Prompt Fuzzer
- ⏳ Activation Tracker
- ⏳ Detection Engine
- ⏳ GUI Development
- ⏳ PDF Report
- ⏳ Final Documentation

---

# 🌿 Git Workflow

```text
main
│
└── develop
      │
      ├── feature/core-engine
      └── feature/gui-fuzzer
```

- `main` → Stable releases
- `develop` → Integration branch
- `feature/core-engine` → Core AI detection modules
- `feature/gui-fuzzer` → GUI, Prompt Fuzzer & Reports

---

# 👥 Team

| Member | Responsibility |
|----------|----------------|
| **Giriraju C M** | Team Lead, Project Architecture, Model Loader, Detection Engine, GitHub Management, Integration |
| **Nikita** | Prompt Fuzzer, Activation Tracker, GUI Development, PDF Report Generation |

---

# 📌 Project Status

> 🚧 **Under Active Development**

This repository is actively being developed as part of the InfoTact Internship Program.

---

# 🤝 Contribution Workflow

1. Create or switch to your assigned feature branch.
2. Implement your assigned module.
3. Commit with meaningful messages.
4. Push your branch.
5. Create a Pull Request to `develop`.
6. After review and testing, merge into `develop`.
7. Stable milestones are merged into `main`.

---

# 📜 License

This project is released under the MIT License.

---

# 📧 Contact

**Project Lead:** Giriraju C M

- GitHub: https://github.com/girirajuinfo
- Repository: https://github.com/girirajuinfo/NeuroFence

---

## ⭐ Future Scope

- Transformer Layer Heatmaps
- Multi-Model Comparison
- Explainable AI Risk Analysis
- Model Fingerprinting
- Advanced Backdoor Detection
- Enterprise Security Dashboard

---

> **"Securing AI Models Before They Secure the World."**