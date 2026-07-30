# Day 1

Completed:

- Created secure model loader
- Added model validation module
- Installed project dependencies
- Tested model loading
- Tested validation logicg

## Day 2 - Secure Model Loading and Metadata Extraction

### Objective
Implemented the backend components required to safely validate and load a local Hugging Face model and extract its metadata.

### Files Added
- utils/logger.py
- sandbox/model_info.py
- tests/test_loader.py

### Files Updated
- sandbox/validator.py
- sandbox/loader.py
- app.py

### Features Implemented
- Custom logging utility
- Model directory validation
- Local Hugging Face tokenizer loading
- Local Hugging Face model loading
- Metadata extraction
- Basic unit tests

### Testing
Successfully tested:
- Valid model directory
- Missing config.json
- Missing model weights
- Invalid directory path

All tests passed successfully.

### Result
The backend can now:
- Validate a model directory
- Load a Hugging Face model
- Load a tokenizer
- Extract model metadata
- Provide metadata for future GUI integration


# Day 3 – Prompt Fuzzer & Activation Tracking

## Objective
Implemented the prompt fuzzing pipeline and neuron activation tracking for NeuroFence.

## Completed Tasks
- Created PromptGenerator to load prompts from `fuzzer/prompts.txt`.
- Added 25 safe prompts for backend testing.
- Implemented reusable HookManager using PyTorch forward hooks.
- Implemented ActivationTracker to store and manage layer activations.
- Integrated prompt execution and activation capture into `app.py`.
- Improved HookManager to support tensor and tuple/list outputs.
- Prevented duplicate hook registration.
- Added unit tests for PromptGenerator, ActivationTracker, and HookManager.

## Testing
Executed the complete backend test suite.

Result:
- 14 tests passed successfully.
- No failures.
- No errors.

## Outcome
NeuroFence can now:
- Load prompts from a file.
- Execute prompts using the loaded model.
- Register and remove forward hooks.
- Capture neuron activations.
- Store activation data for future anomaly detection.