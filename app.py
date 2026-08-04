"""
app.py

NeuroFence Core Engine

Workflow:
Validate Model
    ↓
Load Model
    ↓
Load Prompts
    ↓
Register Hooks
    ↓
Run Prompt
    ↓
Capture Activations
    ↓
Analyze Activations
    ↓
Calculate Risk Score
    ↓
Generate Reports
"""

import json
from pathlib import Path

import torch

from detector.anomaly import ActivationAnalyzer
from detector.scorer import RiskScorer
from fuzzer.generator import PromptGenerator
from sandbox.loader import ModelLoader
from sandbox.model_info import ModelInfo
from sandbox.validator import ModelValidator
from tracker.activation_tracker import ActivationTracker
from tracker.hooks import HookManager
from utils import logger


MODEL_PATH = "models/tiny-gpt2"
PROMPT_FILE = "fuzzer/prompts.txt"
REPORTS_DIR = Path("reports")


def save_json_reports(layer_statistics, scan_summary):
    """
    Save analysis results to JSON files.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    layer_statistics_file = REPORTS_DIR / "layer_statistics.json"
    scan_summary_file = REPORTS_DIR / "scan_summary.json"

    with layer_statistics_file.open("w", encoding="utf-8") as file:
        json.dump(layer_statistics, file, indent=4)

    with scan_summary_file.open("w", encoding="utf-8") as file:
        json.dump(scan_summary, file, indent=4)

    logger.success("JSON reports generated successfully.")


def main():
    logger.info("Starting NeuroFence Core Engine...")

    # -------------------------------------------------
    # Step 1 - Validate model directory
    # -------------------------------------------------

    is_valid, message = ModelValidator.validate(MODEL_PATH)

    if not is_valid:
        logger.error(message)
        return

    # -------------------------------------------------
    # Step 2 - Load tokenizer and model
    # -------------------------------------------------

    tokenizer, model = ModelLoader.load(MODEL_PATH)

    if tokenizer is None or model is None:
        logger.error("Unable to continue because the model could not be loaded.")
        return

    # -------------------------------------------------
    # Step 3 - Extract model metadata
    # -------------------------------------------------

    metadata = ModelInfo.extract(model, MODEL_PATH)

    # -------------------------------------------------
    # Step 4 - Load prompts
    # -------------------------------------------------

    generator = PromptGenerator(PROMPT_FILE)

    if not generator.load_prompts():
        return

    prompt = generator.get_prompt()

    logger.info(f"Running prompt: {prompt}")

    # -------------------------------------------------
    # Step 5 - Register hooks
    # -------------------------------------------------

    hook_manager = HookManager()
    hook_manager.register_hooks(model)

    # -------------------------------------------------
    # Step 6 - Tokenize prompt
    # -------------------------------------------------

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    # -------------------------------------------------
    # Step 7 - Run model
    # -------------------------------------------------

    with torch.no_grad():
        model(**inputs)

    # -------------------------------------------------
    # Step 8 - Capture activations
    # -------------------------------------------------

    tracker = ActivationTracker()

    tracker.store(
        hook_manager.get_outputs()
    )

    hook_manager.remove_hooks()

    # -------------------------------------------------
    # Step 9 - Analyze activations
    # -------------------------------------------------

    analyzer = ActivationAnalyzer()

    layer_statistics = analyzer.analyze(
        tracker.get_activations()
    )

    # -------------------------------------------------
    # Step 10 - Calculate risk
    # -------------------------------------------------

    scorer = RiskScorer()

    scan_summary = scorer.score(
        layer_statistics
    )

    # -------------------------------------------------
    # Step 11 - Save JSON reports
    # -------------------------------------------------

    save_json_reports(
        layer_statistics,
        scan_summary
    )

    # -------------------------------------------------
    # Step 12 - Display metadata
    # -------------------------------------------------

    print("\n========== MODEL INFORMATION ==========\n")

    for key, value in metadata.items():
        print(f"{key:20}: {value}")

    # -------------------------------------------------
    # Step 13 - Display risk summary
    # -------------------------------------------------

    print("\n========== RISK SUMMARY ==========\n")

    print(f"Risk Level          : {scan_summary['risk_level']}")
    print(f"Risk Score          : {scan_summary['risk_score']}")
    print(f"Total Spikes        : {scan_summary['total_spikes']}")
    print(f"Dormant Neurons     : {scan_summary['total_dormant_neurons']}")

    # -------------------------------------------------
    # Step 14 - Display activation summary
    # -------------------------------------------------

    layer_names = tracker.get_layer_names()

    print("\n========== ACTIVATION SUMMARY ==========\n")

    print(f"Captured Layers : {len(layer_names)}")

    print("\nFirst 10 Layers:")

    for layer in layer_names[:10]:
        print(f" - {layer}")

    logger.success("Day 4 Detection Engine completed successfully.")


if __name__ == "__main__":
    main()