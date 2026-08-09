# NeuroFence

## AI-Powered LLM Backdoor & Weight Poisoning Detection Framework

NeuroFence is an AI security and model forensics framework designed to analyze Large Language Models (LLMs) for suspicious internal activation patterns that may indicate potential model poisoning or backdoor-related behavior.

The system performs offline analysis of local Hugging Face models by validating the model, loading it safely, executing security test prompts, capturing neuron activations using PyTorch forward hooks, analyzing activation statistics, calculating a risk score, and generating detailed security reports.

NeuroFence also provides a desktop graphical user interface (GUI) that allows users to select a local model, start a security scan, monitor scan progress, and view the analysis results.

---

## Key Features

* Local Hugging Face model validation
* Safe model and tokenizer loading
* Model metadata extraction
* Adversarial and security test prompt generation
* PyTorch forward-hook based activation monitoring
* Layer-wise activation analysis
* Activation spike detection
* Dormant neuron detection
* Statistical anomaly analysis
* Risk scoring
* JSON report generation
* Professional PDF report generation
* Desktop GUI dashboard
* Scan progress monitoring
* Activation summary
* Scan history support
* PDF export
* Backend memory cleanup
* Automated unit testing

---

# Problem Statement

Large Language Models are increasingly downloaded from public repositories and integrated into applications. However, a model can potentially be modified, poisoned, or embedded with hidden malicious behavior before deployment.

Traditional security checks mainly focus on the external behavior of an application. NeuroFence approaches the problem from a model-forensics perspective by observing internal neuron activation patterns while the model processes different test prompts.

The objective is to provide security indicators that can help researchers and developers identify unusual model behavior and investigate potentially compromised models.

---

# Solution

NeuroFence provides an offline analysis pipeline that:

1. Validates a local Hugging Face model.
2. Loads the model and tokenizer.
3. Extracts model architecture information.
4. Generates security test prompts.
5. Executes prompts against the model.
6. Captures internal layer activations.
7. Calculates activation statistics.
8. Detects spikes and dormant neurons.
9. Calculates an overall risk score.
10. Generates JSON and PDF security reports.
11. Displays the results through a graphical dashboard.

---

# System Architecture

```text
                         NeuroFence
                             |
              +--------------+--------------+
              |                             |
              v                             v
        Desktop GUI                   Core Backend
              |                             |
              |                  +----------+----------+
              |                  |                     |
              v                  v                     v
       Model Selection      Model Validation     Model Loader
              |                  |                     |
              |                  +----------+----------+
              |                             |
              |                             v
              |                      Metadata Extractor
              |                             |
              |                             v
              |                       Prompt Generator
              |                             |
              |                             v
              |                       Hook Manager
              |                             |
              |                             v
              |                     Activation Tracker
              |                             |
              |                             v
              |                      Detection Engine
              |                             |
              |                             v
              |                       Risk Scorer
              |                             |
              +-----------------------------+
                                            |
                                            v
                                   Report Generation
                                      /          \
                                     v            v
                                  JSON           PDF
```

---

# Scan Workflow

```text
User
 |
 v
Select Local Model
 |
 v
Model Validation
 |
 v
Model & Tokenizer Loading
 |
 v
Metadata Extraction
 |
 v
Load Security Test Prompts
 |
 v
Register PyTorch Hooks
 |
 v
Execute Prompts
 |
 v
Capture Layer Activations
 |
 v
Activation Analysis
 |
 v
Risk Assessment
 |
 v
Generate JSON Reports
 |
 v
Generate PDF Report
 |
 v
Display Results in GUI
 |
 v
Cleanup
```

---

# Project Structure

```text
NeuroFence/
│
├── app.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
│
├── assets/
│
├── detector/
│   ├── anomaly.py
│   └── scorer.py
│
├── docs/
│   └── Project_Diary.md
│
├── fuzzer/
│   ├── generator.py
│   └── prompts.txt
│
├── gui/
│   ├── main_window.py
│   └── dashboard.py
│
├── models/
│   └── tiny-gpt2/
│
├── reports/
│   ├── layer_statistics.json
│   ├── scan_summary.json
│   ├── pdf_generator.py
│   └── NeuroFence_Report.pdf
│
├── sandbox/
│   ├── loader.py
│   ├── validator.py
│   └── model_info.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_fuzzer.py
│   ├── test_hooks.py
│   ├── test_activation_tracker.py
│   └── test_detector.py
│
├── tracker/
│   ├── hooks.py
│   └── activation_tracker.py
│
└── utils/
    └── logger.py
```

---

# Backend Components

## Model Validator

**File:** `sandbox/validator.py`

Validates the selected model directory before loading.

It checks for required Hugging Face model files such as:

* `config.json`
* `tokenizer_config.json`
* `tokenizer.json` when applicable
* `model.safetensors` or `pytorch_model.bin`

This prevents invalid or incomplete model directories from being loaded.

---

## Model Loader

**File:** `sandbox/loader.py`

Responsible for loading:

* Hugging Face tokenizer
* Hugging Face model

The loader also handles model-loading errors and reports failures through the project logger.

---

## Model Metadata Extractor

**File:** `sandbox/model_info.py`

Extracts important model information:

* Model name
* Architecture
* Number of layers
* Hidden size
* Vocabulary size
* Total parameters

Example:

```text
Model Name        : tiny-gpt2
Architecture      : GPT2Model
Layers            : 2
Vocabulary Size   : 50257
Parameters        : 102714
```

---

# Adversarial Prompt Fuzzer

**Files:**

```text
fuzzer/generator.py
fuzzer/prompts.txt
```

The Prompt Generator loads predefined prompts used to exercise the model during security analysis.

The current prompt collection includes categories such as:

* General knowledge
* Mathematics
* Programming
* Translation
* Summarization
* Cybersecurity

The generator supports:

* Loading prompts
* Retrieving individual prompts
* Retrieving all prompts
* Shuffling prompt order

The prompt system is designed to be extensible so additional security-oriented prompts can be added later.

---

# Activation Monitoring

## PyTorch Hook Manager

**File:** `tracker/hooks.py`

NeuroFence uses PyTorch forward hooks to observe internal model layer outputs during inference.

The Hook Manager provides:

* Forward-hook registration
* Layer output capture
* Hook removal
* Captured-output management

Hooks are removed after scanning to prevent unnecessary resource usage and repeated registrations.

---

## Activation Tracker

**File:** `tracker/activation_tracker.py`

Stores captured activations and organizes them by layer.

It provides functionality to:

* Store activations
* Retrieve activation data
* Retrieve layer names
* Clear previous activations

This activation data is passed to the detection engine for analysis.

---

# AI Detection Engine

## Activation Analyzer

**File:** `detector/anomaly.py`

The Activation Analyzer performs statistical analysis on captured neuron activations.

It calculates:

* Mean activation
* Standard deviation
* Activation spikes
* Dormant neurons
* Layer-level statistics

Example:

```json
{
    "mean": 0.002,
    "std": 0.025,
    "spikes": 0,
    "dormant_neurons": 2
}
```

---

# Risk Scoring

## Risk Scorer

**File:** `detector/scorer.py`

The Risk Scorer converts the activation-analysis results into an overall security assessment.

Supported risk levels:

```text
Safe
Low
Medium
High
Critical
```

The scan summary contains:

* Risk level
* Risk score
* Total activation spikes
* Total dormant neurons

The score is an analytical indicator based on the current detection logic.

---

# Reporting

## JSON Reports

NeuroFence generates two primary JSON reports:

```text
reports/layer_statistics.json
reports/scan_summary.json
```

### Layer Statistics

Contains statistical information for individual model layers.

### Scan Summary

Contains the overall risk assessment.

Example:

```json
{
    "risk_level": "Critical",
    "risk_score": 227,
    "total_spikes": 0,
    "total_dormant_neurons": 227
}
```

---

# PDF Security Report

**File:** `reports/pdf_generator.py`

NeuroFence generates a professional PDF report:

```text
reports/NeuroFence_Report.pdf
```

The report includes:

* Project name
* Scan date
* Model name
* Architecture
* Number of layers
* Total parameters
* Risk score
* Security verdict
* Prompt statistics
* Scan summary

---

# Graphical User Interface

NeuroFence provides a desktop GUI for interacting with the security-analysis backend.

## Main Window

**File:** `gui/main_window.py`

Provides the main application window and application-level interface.

---

## Dashboard

**File:** `gui/dashboard.py`

The dashboard provides:

### Toolbar

* Upload Model
* Start Scan
* Stop Scan
* Export PDF

### Model Information

Displays:

* Model name
* Architecture
* Number of layers
* Vocabulary size
* Total parameters

### AI Security Score

Displays the calculated:

* Risk level
* Risk score
* Security assessment

### Scan Progress

Provides visual feedback while the model is being analyzed.

### Console Log

Displays backend scan messages and status information.

### Activation Summary

Displays captured activation information and layer statistics.

### Scan Statistics

Displays overall scan information.

### Scan History

Provides visibility into previous scan results.

### Status Bar

Displays the current application state.

---

# Team Contributions

## Giriraju C M

**Role:** Core Engine & AI Security Backend

Responsibilities:

* Backend architecture
* Model validation
* Model loading
* Model metadata extraction
* Prompt-generation backend
* PyTorch forward hooks
* Activation tracking
* Activation analysis
* Spike detection
* Dormant neuron detection
* Risk scoring
* JSON report generation
* PDF report generation
* Backend pipeline integration
* Exception handling
* Memory cleanup
* Automated backend testing
* Git and backend documentation

---

## Nikita

**Role:** GUI & Fuzzer Integration

Responsibilities:

* GUI development
* Main window
* Dashboard interface
* Model selection interface
* Scan controls
* Progress display
* Console/log interface
* Activation viewer
* Scan status display
* Prompt/fuzzer GUI integration
* GUI/backend integration support

---

# Technologies Used

| Technology                | Purpose                                      |
| ------------------------- | -------------------------------------------- |
| Python                    | Core programming language                    |
| PyTorch                   | Model execution and activation hooks         |
| Hugging Face Transformers | LLM loading and inference                    |
| Hugging Face Hub          | Model ecosystem support                      |
| ReportLab                 | PDF report generation                        |
| PyQt6                     | Desktop GUI                                  |
| JSON                      | Structured scan reports                      |
| unittest                  | Automated testing                            |
| Git                       | Version control                              |
| GitHub                    | Source-code collaboration                    |
| Kali Linux                | Development and security testing environment |

---

# Installation

## Clone the Repository

```bash
git clone https://github.com/girirajuinfo/NeuroFence.git
cd NeuroFence
```

## Create Virtual Environment

```bash
python3 -m venv venv
```

## Activate Environment

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Model Requirements

NeuroFence works with local Hugging Face model directories.

A typical model directory contains:

```text
model/
├── config.json
├── tokenizer_config.json
├── tokenizer.json
└── model.safetensors
```

The files must be valid and compatible with each other.

Empty placeholder files are not valid model files.

---

# Running the Application

## Backend

From the project root:

```bash
python3 app.py
```

## GUI

```bash
python3 app.py --gui
```

---

# Testing

Run the complete test suite:

```bash
python3 -m unittest discover tests -v
```

Individual modules can be tested with:

```bash
python3 -m unittest tests.test_loader -v
```

```bash
python3 -m unittest tests.test_fuzzer -v
```

```bash
python3 -m unittest tests.test_hooks -v
```

```bash
python3 -m unittest tests.test_activation_tracker -v
```

```bash
python3 -m unittest tests.test_detector -v
```

---

# End-to-End Testing

A complete scan verifies:

```text
Model Validator
      ↓
Model Loader
      ↓
Metadata Extractor
      ↓
Prompt Generator
      ↓
Hook Manager
      ↓
Activation Tracker
      ↓
Activation Analyzer
      ↓
Risk Scorer
      ↓
JSON Reports
      ↓
PDF Generator
      ↓
GUI Dashboard
```

The application also performs cleanup after scanning by:

* Removing registered hooks
* Clearing activation data
* Releasing temporary resources
* Logging cleanup status

---

# Security Analysis

NeuroFence currently analyzes internal activation behavior using statistical indicators.

### Activation Mean

Measures the average activation value.

### Standard Deviation

Measures the variation of activation values.

### Activation Spikes

Identifies unusually high activation values according to the configured analysis logic.

### Dormant Neurons

Identifies neurons with very low activation values according to the configured threshold.

### Risk Score

Combines the detected indicators into an overall security assessment.

---

# Limitations

NeuroFence is a prototype AI security and model-forensics framework.

A `High` or `Critical` result does **not automatically prove** that a model contains a backdoor or has been poisoned.

Activation behavior can vary depending on:

* Model architecture
* Model size
* Prompt content
* Inference conditions
* Threshold configuration
* Normal model behavior

The current system should therefore be considered a **security-analysis indicator**, not a definitive malware or backdoor detector.

---

# Future Scope

Future versions can include:

* Advanced backdoor detection algorithms
* Trusted model baseline comparison
* Trigger-prompt analysis
* Activation heatmaps
* Layer visualization
* Configurable detection thresholds
* Larger LLM support
* Batch model scanning
* Model-to-model comparison
* Advanced anomaly detection
* Improved dashboard visualization
* Persistent scan history
* Additional AI security checks

---

# Project Status

NeuroFence currently provides an integrated prototype capable of:

* Loading local Hugging Face models
* Validating model files
* Extracting model metadata
* Running security test prompts
* Capturing internal layer activations
* Performing activation analysis
* Detecting activation spikes and dormant neurons
* Calculating risk scores
* Generating JSON reports
* Generating PDF security reports
* Displaying scan information through a desktop GUI
* Cleaning up hooks and activation data after scanning

---

# Git Workflow

The project uses feature branches with `develop` as the integration branch.

```text
feature/core-engine
        |
        v
     develop
        |
        v
       main
```

### Giriraju

```text
feature/core-engine
```

### Nikita

```text
feature/gui-fuzzer
```

Changes are reviewed through Pull Requests before integration into `develop`.

---

# Team

### Giriraju C M

Core Engine • Backend • AI Security Analysis

GitHub: `https://github.com/girirajuinfo`

### Nikita

GUI • Fuzzer Integration • User Interface

---

# Disclaimer

NeuroFence is an educational and research-oriented AI security project.

The generated risk score and activation statistics should be treated as security indicators and should be investigated further before making production deployment or security decisions.

---

# License

This project is licensed under the terms specified in the repository `LICENSE` file.
