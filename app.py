"""
app.py

NeuroFence Core Engine + GUI Integration Layer

Workflow

Validate Model
    ↓
Load Model
    ↓
Extract Metadata
    ↓
Load Prompts
    ↓
Register Hooks
    ↓
Run Model
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

This module contains the backend pipeline (unchanged logic, existing
modules only) plus a thin controller that wires the existing PyQt6 GUI
(gui/main_window.py, gui/dashboard.py) to that pipeline.

Run modes
    python app.py            -> headless backend pipeline
    python app.py --gui      -> NeuroFence desktop console
"""

import json
import os
import subprocess
import sys
import time
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

LAYER_STATISTICS_PATH = REPORTS_DIR / "layer_statistics.json"
SCAN_SUMMARY_PATH = REPORTS_DIR / "scan_summary.json"
PDF_REPORT_PATH = REPORTS_DIR / "NeuroFence_Report.pdf"


class ScanCancelled(Exception):
    """Raised internally when the user stops a running scan."""


# ==========================================================
# Reports
# ==========================================================

def save_json_reports(layer_statistics, scan_summary):
    """
    Save JSON reports.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with LAYER_STATISTICS_PATH.open("w", encoding="utf-8") as file:
        json.dump(layer_statistics, file, indent=4)

    with SCAN_SUMMARY_PATH.open("w", encoding="utf-8") as file:
        json.dump(scan_summary, file, indent=4)

    logger.success("JSON reports generated successfully.")


# ==========================================================
# Model preparation (used by both CLI and GUI)
# ==========================================================

def _directory_size(model_path):
    """
    Return a human readable size for a model directory.
    """

    path = Path(model_path)

    if not path.exists():
        return "Unknown"

    total = sum(
        file.stat().st_size
        for file in path.rglob("*")
        if file.is_file()
    )

    if total >= 1024 ** 3:
        return f"{total / 1024 ** 3:.2f} GB"

    if total >= 1024 ** 2:
        return f"{total / 1024 ** 2:.2f} MB"

    return f"{total / 1024:.2f} KB"


def prepare_model(model_path):
    """
    Validate the model, load it and extract its metadata.

    Returns:
        tuple: (tokenizer, model, metadata)

    Raises:
        ValueError: validation failed.
        RuntimeError: loading failed.
    """

    is_valid, message = ModelValidator.validate(model_path)

    if not is_valid:
        logger.error(message)
        raise ValueError(message)

    tokenizer, model = ModelLoader.load(model_path)

    if tokenizer is None or model is None:
        message = "Unable to continue because the model could not be loaded."
        logger.error(message)
        raise RuntimeError(message)

    metadata = ModelInfo.extract(model, model_path)

    # Presentation-only extras (backend modules stay untouched)
    try:
        device = str(next(model.parameters()).device)
    except StopIteration:
        device = "cpu"

    metadata["device"] = device.upper()
    metadata["model_size"] = _directory_size(model_path)

    return tokenizer, model, metadata


# ==========================================================
# Pipeline
# ==========================================================

def run_pipeline(
    model_path=MODEL_PATH,
    prompt_file=PROMPT_FILE,
    tokenizer=None,
    model=None,
    metadata=None,
    progress=None,
    should_stop=None,
):
    """
    Execute the complete NeuroFence pipeline.

    Args:
        model_path (str): Local model directory.
        prompt_file (str): Prompt dataset.
        tokenizer / model / metadata: Optional preloaded objects
            (the GUI loads the model when the folder is selected).
        progress (callable): progress(stage_name, percent).
        should_stop (callable): returns True to cancel the scan.

    Returns:
        dict: Backend API response.
    """

    def report(stage, percent):
        logger.info(stage)
        if progress is not None:
            progress(stage, percent)

    def check_stop():
        if should_stop is not None and should_stop():
            raise ScanCancelled("Scan stopped by user.")

    hook_manager = HookManager()
    tracker = ActivationTracker()

    started_at = time.time()

    try:
        # ------------------------------------------
        # Validate + Load + Metadata
        # ------------------------------------------

        if tokenizer is None or model is None or metadata is None:
            report("Validating and loading model...", 5)
            tokenizer, model, metadata = prepare_model(model_path)

        report("Model ready.", 15)
        check_stop()

        # ------------------------------------------
        # Prompts
        # ------------------------------------------

        report("Loading prompts...", 20)

        generator = PromptGenerator(prompt_file)

        if not generator.load_prompts():
            raise RuntimeError("Prompt file could not be loaded.")

        prompts = generator.get_all_prompts()

        if not prompts:
            raise RuntimeError("No prompts available.")

        # ------------------------------------------
        # Register Hooks
        # ------------------------------------------

        report("Registering hooks...", 30)

        hook_manager.register_hooks(model)

        # ------------------------------------------
        # Run Model + Capture Activations
        # ------------------------------------------

        total = len(prompts)

        for index, prompt in enumerate(prompts, start=1):

            check_stop()

            inputs = tokenizer(prompt, return_tensors="pt")

            with torch.no_grad():
                model(**inputs)

            percent = 30 + int(40 * index / total)

            report(
                f"Running prompt {index} / {total}",
                percent,
            )

        tracker.store(hook_manager.get_outputs())

        check_stop()

        # ------------------------------------------
        # Analyze
        # ------------------------------------------

        report("Analyzing activations...", 75)

        analyzer = ActivationAnalyzer()

        layer_statistics = analyzer.analyze(tracker.get_activations())

        check_stop()

        # ------------------------------------------
        # Risk Score
        # ------------------------------------------

        report("Calculating risk...", 85)

        scorer = RiskScorer()

        scan_summary = scorer.score(layer_statistics)

        # ------------------------------------------
        # JSON Reports
        # ------------------------------------------

        report("Generating JSON reports...", 90)

        save_json_reports(layer_statistics, scan_summary)

        # ------------------------------------------
        # PDF Report
        # ------------------------------------------

        report("Generating PDF report...", 95)

        pdf_generator = PDFReportGenerator()

        pdf_path = pdf_generator.generate(
            metadata=metadata,
            risk_summary=scan_summary,
            prompt_count=total,
        )

        layer_names = tracker.get_layer_names()

        execution_time = time.time() - started_at

        report("Scan Completed Successfully", 100)

        logger.success("NeuroFence pipeline completed successfully.")

        return {
            "metadata": metadata,
            "activation_summary": {
                "captured_layers": len(layer_names),
                "layer_names": layer_names,
            },
            "risk_score": scan_summary,
            "statistics": layer_statistics,
            "scan_summary": scan_summary,
            "prompt_count": total,
            "execution_time": execution_time,
            "pdf_report_path": pdf_path,
            "layer_statistics_path": str(LAYER_STATISTICS_PATH),
            "scan_summary_path": str(SCAN_SUMMARY_PATH),
        }

    finally:

        # Always remove hooks if they are still registered
        if hook_manager.handles:
            hook_manager.remove_hooks()

        # Always clear stored activations
        tracker.clear()

        logger.info("Memory cleanup completed.")


def main():
    """
    Headless backend entry point.
    """

    logger.info("Starting NeuroFence Core Engine...")

    try:
        results = run_pipeline(MODEL_PATH, PROMPT_FILE)

    except Exception as error:
        logger.error(f"Unexpected error: {error}")
        return None

    metadata = results["metadata"]
    scan_summary = results["scan_summary"]

    print("\n========== MODEL INFORMATION ==========\n")

    for key, value in metadata.items():
        print(f"{key:20}: {value}")

    print("\n========== RISK SUMMARY ==========\n")

    print(f"Risk Level          : {scan_summary['risk_level']}")
    print(f"Risk Score          : {scan_summary['risk_score']}")
    print(f"Total Spikes        : {scan_summary['total_spikes']}")
    print(
        f"Dormant Neurons     : "
        f"{scan_summary['total_dormant_neurons']}"
    )

    layer_names = results["activation_summary"]["layer_names"]

    print("\n========== ACTIVATION SUMMARY ==========\n")

    print(f"Captured Layers : {len(layer_names)}")

    print("\nFirst 10 Layers:")

    for layer in layer_names[:10]:
        print(f" - {layer}")

    print("\n========== REPORTS ==========\n")

    print(f"Layer Statistics : {results['layer_statistics_path']}")
    print(f"Scan Summary     : {results['scan_summary_path']}")
    print(f"PDF Report       : {results['pdf_report_path']}")

    return results


# ==========================================================
# GUI integration
# ==========================================================

def run_gui():
    """
    Launch the NeuroFence PyQt6 desktop console and connect the
    existing GUI to the existing backend pipeline.
    """

    from PyQt6.QtCore import QObject, QThread, pyqtSignal
    from PyQt6.QtWidgets import QApplication, QMessageBox

    # gui/main_window.py imports "dashboard" directly, so the gui
    # folder must be importable.
    gui_dir = Path(__file__).resolve().parent / "gui"
    if str(gui_dir) not in sys.path:
        sys.path.insert(0, str(gui_dir))

    from gui.main_window import MainWindow

    # ------------------------------------------------------
    # Logger bridge: backend logger -> GUI console + terminal
    # ------------------------------------------------------

    class LoggerBridge(QObject):
        """Mirror utils.logger output into the GUI console."""

        message = pyqtSignal(str, str)

        LEVELS = ("info", "success", "warning", "error")

        def __init__(self):
            super().__init__()
            self._originals = {}

        def install(self):
            for name in self.LEVELS:
                original = getattr(logger, name)
                self._originals[name] = original
                setattr(logger, name, self._wrap(name, original))

        def restore(self):
            for name, original in self._originals.items():
                setattr(logger, name, original)
            self._originals.clear()

        def _wrap(self, name, original):
            def wrapped(text):
                original(text)  # keep terminal logging
                self.message.emit(str(text), name.upper())
            return wrapped

    # ------------------------------------------------------
    # Worker: runs the pipeline off the UI thread
    # ------------------------------------------------------

    class ScanWorker(QObject):
        """Runs run_pipeline() in a background thread."""

        progress = pyqtSignal(str, int)
        finished = pyqtSignal(dict)
        failed = pyqtSignal(str)
        cancelled = pyqtSignal()

        def __init__(self, model_path, tokenizer, model, metadata):
            super().__init__()
            self.model_path = model_path
            self.tokenizer = tokenizer
            self.model = model
            self.metadata = metadata
            self._stop = False

        def stop(self):
            self._stop = True

        def run(self):
            try:
                results = run_pipeline(
                    model_path=self.model_path,
                    prompt_file=PROMPT_FILE,
                    tokenizer=self.tokenizer,
                    model=self.model,
                    metadata=self.metadata,
                    progress=lambda stage, percent:
                        self.progress.emit(stage, int(percent)),
                    should_stop=lambda: self._stop,
                )

            except ScanCancelled:
                self.cancelled.emit()

            except Exception as error:  # never crash the app
                self.failed.emit(str(error))

            else:
                self.finished.emit(results)

    class LoadWorker(QObject):
        """Validates, loads and inspects a model off the UI thread."""

        loaded = pyqtSignal(object, object, dict)
        invalid = pyqtSignal(str)
        failed = pyqtSignal(str)

        def __init__(self, model_path):
            super().__init__()
            self.model_path = model_path

        def run(self):
            try:
                tokenizer, model, metadata = prepare_model(
                    self.model_path
                )

            except ValueError as error:
                self.invalid.emit(str(error))

            except Exception as error:
                self.failed.emit(str(error))

            else:
                self.loaded.emit(tokenizer, model, metadata)

    # ------------------------------------------------------
    # Controller: connects GUI signals to backend calls
    # ------------------------------------------------------

    class NeuroFenceController(QObject):
        """Signal-slot bridge between the dashboard and the backend."""

        def __init__(self, window):
            super().__init__()

            self.window = window
            self.dashboard = window.dashboard

            self.tokenizer = None
            self.model = None
            self.metadata = None
            self.pdf_path = None

            self.thread = None
            self.worker = None

            self.bridge = LoggerBridge()
            self.bridge.message.connect(self._on_log)
            self.bridge.install()

            self.dashboard.model_selected.connect(self.load_model)
            self.dashboard.scan_requested.connect(self.start_scan)
            self.dashboard.stop_requested.connect(self.stop_scan)
            self.dashboard.export_requested.connect(self.export_pdf)

        # ---- logging ------------------------------------

        def _on_log(self, message, level):
            self.dashboard.log(message, level)

        # ---- model loading ------------------------------

        def load_model(self, model_path):

            if self._busy():
                return

            self.tokenizer = None
            self.model = None
            self.metadata = None

            self.thread = QThread()
            self.worker = LoadWorker(model_path)
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.loaded.connect(self._on_model_loaded)
            self.worker.invalid.connect(self._on_model_invalid)
            self.worker.failed.connect(self._on_model_failed)

            for signal in (
                self.worker.loaded,
                self.worker.invalid,
                self.worker.failed,
            ):
                signal.connect(lambda *_: self._cleanup_thread())

            self.thread.start()

        def _on_model_loaded(self, tokenizer, model, metadata):
            self.tokenizer = tokenizer
            self.model = model
            self.metadata = metadata

            self.dashboard.show_metadata(metadata)

            generator = PromptGenerator(PROMPT_FILE)

            if generator.load_prompts():
                self.dashboard.set_prompt_count(
                    len(generator.get_all_prompts())
                )

            self.dashboard.enable_scan(True)

        def _on_model_invalid(self, message):
            self.dashboard.enable_scan(False)
            QMessageBox.warning(
                self.window,
                "Invalid Model",
                f"Model validation failed:\n\n{message}",
            )

        def _on_model_failed(self, message):
            self.dashboard.enable_scan(False)
            QMessageBox.critical(
                self.window,
                "Model Load Error",
                f"The model could not be loaded:\n\n{message}",
            )

        # ---- scanning -----------------------------------

        def start_scan(self):

            if self._busy():
                return

            if self.model is None or self.tokenizer is None:
                QMessageBox.warning(
                    self.window,
                    "No Model Loaded",
                    "Load a model before starting a scan.",
                )
                self.dashboard.scan_failed("No model loaded.")
                return

            self.pdf_path = None

            self.thread = QThread()
            self.worker = ScanWorker(
                self.dashboard.selected_model_path,
                self.tokenizer,
                self.model,
                self.metadata,
            )
            self.worker.moveToThread(self.thread)

            self.thread.started.connect(self.worker.run)
            self.worker.progress.connect(self._on_progress)
            self.worker.finished.connect(self._on_scan_finished)
            self.worker.failed.connect(self._on_scan_failed)
            self.worker.cancelled.connect(self._on_scan_cancelled)

            for signal in (
                self.worker.finished,
                self.worker.failed,
                self.worker.cancelled,
            ):
                signal.connect(lambda *_: self._cleanup_thread())

            self.thread.start()

        def stop_scan(self):
            if isinstance(self.worker, ScanWorker):
                self.worker.stop()

        def _on_progress(self, stage, percent):
            self.dashboard.set_stage(stage, percent)

        def _on_scan_finished(self, results):
            self.pdf_path = results.get("pdf_report_path")

            self.dashboard.show_scan_results(results)

            self.dashboard.log(
                f"Layer Statistics : {results['layer_statistics_path']}",
                "INFO",
            )
            self.dashboard.log(
                f"Scan Summary     : {results['scan_summary_path']}",
                "INFO",
            )
            self.dashboard.log(
                f"PDF Report       : {self.pdf_path}",
                "SUCCESS",
            )

        def _on_scan_failed(self, message):
            self.dashboard.scan_failed(message)

        def _on_scan_cancelled(self):
            self.dashboard.log(
                "Scan stopped safely. Hooks removed and memory released.",
                "WARNING",
            )
            self.dashboard.enable_scan(True)

        # ---- report export ------------------------------

        def export_pdf(self):

            path = Path(self.pdf_path or PDF_REPORT_PATH)

            if not path.exists():
                QMessageBox.critical(
                    self.window,
                    "Report Not Found",
                    "The PDF report does not exist yet.\n"
                    "Run a scan before exporting.",
                )
                self.dashboard.log(
                    "PDF report not found.",
                    "ERROR",
                )
                return

            self.dashboard.log(f"Opening report: {path}", "INFO")

            try:
                if sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", str(path)])
                elif os.name == "nt":
                    os.startfile(str(path))  # noqa: S606
                else:
                    subprocess.Popen(["xdg-open", str(path)])

            except Exception as error:
                QMessageBox.critical(
                    self.window,
                    "Unable to Open Report",
                    f"The PDF report could not be opened:\n\n{error}",
                )
                self.dashboard.log(
                    f"Unable to open report: {error}",
                    "ERROR",
                )

        # ---- threads ------------------------------------

        def _busy(self):
            return self.thread is not None and self.thread.isRunning()

        def _cleanup_thread(self):
            if self.thread is not None:
                self.thread.quit()
                self.thread.wait()
                self.thread = None
            self.worker = None

        def shutdown(self):
            self.stop_scan()
            self._cleanup_thread()
            self.bridge.restore()

    app = QApplication(sys.argv)
    app.setApplicationName("NeuroFence")
    app.setApplicationDisplayName("NeuroFence Security Console")
    app.setStyle("Fusion")

    window = MainWindow()
    controller = NeuroFenceController(window)

    app.aboutToQuit.connect(controller.shutdown)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    # Default entry point stays the backend engine.
    # Pass --gui (or --ui) to open the desktop console instead.
    if "--gui" in sys.argv or "--ui" in sys.argv:
        run_gui()
    else:
        main()