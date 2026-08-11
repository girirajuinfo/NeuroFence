"""
model_info.py

Extract metadata from a loaded Hugging Face model.
"""

from pathlib import Path

from utils import logger


class ModelInfo:
    """
    Extract useful metadata from a loaded model.
    """

    @staticmethod
    def extract(model, model_path):
        """
        Extract metadata from a Hugging Face model.

        Args:
            model: Loaded Hugging Face model.
            model_path (str): Local model directory.

        Returns:
            dict: Model metadata.
        """

        logger.info("Extracting model metadata...")

        config = model.config

        metadata = {
            "model_name": Path(model_path).name,
            "architecture": model.__class__.__name__,
            "hidden_size": getattr(config, "hidden_size", "Unknown"),
            "num_layers": getattr(config, "num_hidden_layers", "Unknown"),
            "vocab_size": getattr(config, "vocab_size", "Unknown"),
            "total_parameters": sum(
                parameter.numel()
                for parameter in model.parameters()
            )
        }

        logger.success("Metadata extracted successfully.")

        return metadata