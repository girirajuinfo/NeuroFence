"""
generator.py

Load and manage prompt datasets for NeuroFence.
"""

import random
from pathlib import Path

from utils import logger


class PromptGenerator:
    """
    Load prompts from a text file.
    """

    def __init__(self, prompt_file):
        self.prompt_file = Path(prompt_file)
        self.prompts = []

    def load_prompts(self):
        """
        Load prompts from the text file.
        """

        logger.info(f"Loading prompts from {self.prompt_file}")

        if not self.prompt_file.exists():
            logger.error("Prompt file not found.")
            return False

        with self.prompt_file.open("r", encoding="utf-8") as file:
            self.prompts = [
                line.strip()
                for line in file
                if line.strip()
            ]

        logger.success(f"Loaded {len(self.prompts)} prompts.")

        return True

    def get_all_prompts(self):
        """
        Return every loaded prompt.
        """
        return self.prompts.copy()

    def get_prompt(self):
        """
        Return one random prompt.
        """

        if not self.prompts:
            logger.warning("No prompts loaded.")
            return None

        return random.choice(self.prompts)

    def shuffle_prompts(self):
        """
        Shuffle prompt order.
        """

        random.shuffle(self.prompts)

        logger.info("Prompt order shuffled.")