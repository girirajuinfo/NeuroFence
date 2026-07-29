from sandbox.validator import ModelValidator
from sandbox.loader import ModelLoader
from sandbox.model_info import ModelInfo
from utils import logger


MODEL_PATH = "models/tiny-gpt2"


def main():
    logger.info("Starting NeuroFence Core Engine...")

    is_valid, message = ModelValidator.validate(MODEL_PATH)

    if not is_valid:
        logger.error(message)
        return

    tokenizer, model = ModelLoader.load(MODEL_PATH)

    if model is None:
        logger.error("Unable to continue because the model could not be loaded.")
        return

    metadata = ModelInfo.extract(model, MODEL_PATH)

    logger.info("Model Metadata:")

    for key, value in metadata.items():
        print(f"{key:20}: {value}")

    logger.success("NeuroFence backend is ready.")


if __name__ == "__main__":
    main()