"""
loader.py

Safely load a Hugging Face model and tokenizer
from a validated local directory.
"""

from pathlib import Path

from transformers import AutoModel, AutoTokenizer

from utils import logger


class ModelLoader:
    """
    Loads a Hugging Face model and tokenizer.
    """

    @staticmethod
    def load(model_path):
        """
        Load the tokenizer and model from a local directory.

        Args:
            model_path (str): Path to the local model directory.

        Returns:
            tuple:
                (tokenizer, model) on success
                (None, None) on failure
        """

        model_path = Path(model_path)

        logger.info(f"Loading model from: {model_path}")

        try:
            tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True
            )

            logger.success("Tokenizer loaded successfully.")

            model = AutoModel.from_pretrained(
                model_path,
                local_files_only=True
            )

            logger.success("Model loaded successfully.")

            return tokenizer, model

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None, None