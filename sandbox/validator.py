"""
validator.py

Validate that a Hugging Face model directory contains
the required files before loading.
"""

from pathlib import Path
from utils import logger


class ModelValidator:
    """
    Validates a Hugging Face model directory.
    """

    REQUIRED_FILES = [
        "config.json",
        "tokenizer_config.json"
    ]

    WEIGHT_FILES = [
        "model.safetensors",
        "pytorch_model.bin"
    ]

    OPTIONAL_FILES = [
        "tokenizer.json"
    ]

    @staticmethod
    def validate(model_path):
        """
        Validate the model directory.

        Args:
            model_path (str): Path to the model folder.

        Returns:
            tuple:
                (True, "Valid model directory")
                or
                (False, "Reason for failure")
        """

        path = Path(model_path)

        logger.info(f"Validating model directory: {path}")

        if not path.exists():
            logger.error("Model directory does not exist.")
            return False, "Model directory does not exist."

        if not path.is_dir():
            logger.error("Provided path is not a directory.")
            return False, "Provided path is not a directory."

        for filename in ModelValidator.REQUIRED_FILES:
            file_path = path / filename

            if not file_path.exists():
                logger.error(f"Missing required file: {filename}")
                return False, f"Missing required file: {filename}"

        weight_found = False

        for weight_file in ModelValidator.WEIGHT_FILES:
            if (path / weight_file).exists():
                weight_found = True
                break

        if not weight_found:
            logger.error(
                "Missing model weights (model.safetensors or pytorch_model.bin)."
            )
            return (
                False,
                "Missing model weights (model.safetensors or pytorch_model.bin)."
            )

        optional_file = path / "tokenizer.json"

        if optional_file.exists():
            logger.info("tokenizer.json found.")
        else:
            logger.warning("tokenizer.json not found (may be acceptable).")

        logger.success("Model directory validation successful.")

        return True, "Valid model directory"