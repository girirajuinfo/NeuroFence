import torch

from fuzzer.generator import PromptGenerator
from sandbox.loader import ModelLoader
from sandbox.model_info import ModelInfo
from sandbox.validator import ModelValidator
from tracker.activation_tracker import ActivationTracker
from tracker.hooks import HookManager
from utils import logger


MODEL_PATH = "models/tiny-gpt2"
PROMPT_FILE = "fuzzer/prompts.txt"


def main():
    logger.info("Starting NeuroFence Core Engine...")

    # Step 1: Validate model directory
    is_valid, message = ModelValidator.validate(MODEL_PATH)

    if not is_valid:
        logger.error(message)
        return

    # Step 2: Load tokenizer and model
    tokenizer, model = ModelLoader.load(MODEL_PATH)

    if model is None or tokenizer is None:
        logger.error("Unable to continue because the model could not be loaded.")
        return

    # Step 3: Load prompts
    generator = PromptGenerator(PROMPT_FILE)

    if not generator.load_prompts():
        return

    prompt = generator.get_prompt()

    logger.info(f"Running prompt: {prompt}")

    # Step 4: Register hooks
    hook_manager = HookManager()
    hook_manager.register_hooks(model)

    # Step 5: Tokenize the prompt
    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    # Step 6: Run the model
    with torch.no_grad():
        model(**inputs)

    # Step 7: Store activations
    tracker = ActivationTracker()

    tracker.store(
        hook_manager.get_outputs()
    )

    # Step 8: Remove hooks
    hook_manager.remove_hooks()

    # Step 9: Extract metadata
    metadata = ModelInfo.extract(model, MODEL_PATH)

    logger.info("Model Metadata")

    for key, value in metadata.items():
        print(f"{key:20}: {value}")

    print()

    layer_names = tracker.get_layer_names()

    logger.info(
        f"Captured activations from {len(layer_names)} layers."
    )

    print("\nFirst 10 captured layers:")

    for layer in layer_names[:10]:
        print(layer)

    logger.success("Day 3 pipeline completed successfully.")


if __name__ == "__main__":
    main()