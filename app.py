"""
app.py

NeuroFence Core Engine

Workflow

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
Calculate Risk
    ↓
Generate JSON Reports
    ↓
Generate PDF Report
    ↓
Return Results
"""

import json
from pathlib import Path

import torch

from detector.anomaly import ActivationAnalyzer
from detector.scorer import RiskScorer
from fuzzer.generator import PromptGenerator
from reports.pdf_generator import PDFReportGenerator
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
    Save JSON reports.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    layer_statistics_path = REPORTS_DIR / "layer_statistics.json"
    scan_summary_path = REPORTS_DIR / "scan_summary.json"

    with layer_statistics_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            layer_statistics,
            file,
            indent=4
        )

    with scan_summary_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            scan_summary,
            file,
            indent=4
        )

    logger.success("JSON reports generated successfully.")


def main():

    logger.info("Starting NeuroFence Core Engine...")

    hook_manager = HookManager()
    tracker = ActivationTracker()

    try:

        # ------------------------------------------
        # Validate model
        # ------------------------------------------

        is_valid, message = ModelValidator.validate(
            MODEL_PATH
        )

        if not is_valid:
            logger.error(message)
            return

        # ------------------------------------------
        # Load model
        # ------------------------------------------

        tokenizer, model = ModelLoader.load(
            MODEL_PATH
        )

        if tokenizer is None or model is None:

            logger.error(
                "Unable to continue because the model could not be loaded."
            )

            return

        # ------------------------------------------
        # Metadata
        # ------------------------------------------

        metadata = ModelInfo.extract(
            model,
            MODEL_PATH
        )

        # ------------------------------------------
        # Prompt Generator
        # ------------------------------------------

        generator = PromptGenerator(
            PROMPT_FILE
        )

        if not generator.load_prompts():
            return

        prompt = generator.get_prompt()

        logger.info(
            f"Running prompt: {prompt}"
        )

        # ------------------------------------------
        # Register Hooks
        # ------------------------------------------

        hook_manager.register_hooks(model)

        # ------------------------------------------
        # Tokenize
        # ------------------------------------------

        inputs = tokenizer(
            prompt,
            return_tensors="pt"
        )

        # ------------------------------------------
        # Forward Pass
        # ------------------------------------------

        with torch.no_grad():

            model(**inputs)

        # ------------------------------------------
        # Store Activations
        # ------------------------------------------

        tracker.store(
            hook_manager.get_outputs()
        )

        # ------------------------------------------
        # Analyze
        # ------------------------------------------

        analyzer = ActivationAnalyzer()

        layer_statistics = analyzer.analyze(
            tracker.get_activations()
        )

        # ------------------------------------------
        # Risk Score
        # ------------------------------------------

        scorer = RiskScorer()

        scan_summary = scorer.score(
            layer_statistics
        )

        # ------------------------------------------
        # Save JSON
        # ------------------------------------------

        save_json_reports(
            layer_statistics,
            scan_summary
        )
                # ------------------------------------------
        # Generate PDF Report
        # ------------------------------------------

        pdf_generator = PDFReportGenerator()

        pdf_path = pdf_generator.generate(
            metadata=metadata,
            risk_summary=scan_summary,
            prompt_count=len(generator.get_all_prompts())
        )

        # ------------------------------------------
        # Display Model Information
        # ------------------------------------------

        print("\n========== MODEL INFORMATION ==========\n")

        for key, value in metadata.items():
            print(f"{key:20}: {value}")

        # ------------------------------------------
        # Display Risk Summary
        # ------------------------------------------

        print("\n========== RISK SUMMARY ==========\n")

        print(f"Risk Level          : {scan_summary['risk_level']}")
        print(f"Risk Score          : {scan_summary['risk_score']}")
        print(f"Total Spikes        : {scan_summary['total_spikes']}")
        print(
            f"Dormant Neurons     : "
            f"{scan_summary['total_dormant_neurons']}"
        )

        # ------------------------------------------
        # Display Activation Summary
        # ------------------------------------------

        layer_names = tracker.get_layer_names()

        print("\n========== ACTIVATION SUMMARY ==========\n")

        print(f"Captured Layers : {len(layer_names)}")

        print("\nFirst 10 Layers:")

        for layer in layer_names[:10]:
            print(f" - {layer}")

        # ------------------------------------------
        # Report Paths
        # ------------------------------------------

        print("\n========== REPORTS ==========\n")

        print("Layer Statistics : reports/layer_statistics.json")
        print("Scan Summary     : reports/scan_summary.json")
        print(f"PDF Report       : {pdf_path}")

        logger.success(
            "Day 5 backend pipeline completed successfully."
        )

        # ------------------------------------------
        # Backend API Response
        # ------------------------------------------

        return {
            "metadata": metadata,
            "activation_summary": {
                "captured_layers": len(layer_names)
            },
            "risk_score": scan_summary,
            "statistics": layer_statistics,
            "pdf_report_path": pdf_path,
            "scan_summary": scan_summary
        }

    except Exception as error:

        logger.error(f"Unexpected error: {error}")

        raise

    finally:

        # Always remove hooks if they are still registered
        if hook_manager.handles:
            hook_manager.remove_hooks()

        # Always clear stored activations
        tracker.clear()

        logger.info("Memory cleanup completed.")


if __name__ == "__main__":
    main()