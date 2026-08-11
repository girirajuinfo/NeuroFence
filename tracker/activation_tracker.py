"""
activation_tracker.py

Store and manage captured neuron activations.
"""

from utils import logger


class ActivationTracker:
    """
    Stores activations captured by the HookManager.
    """

    def __init__(self):
        self.activations = {}

    def clear(self):
        """
        Remove all previously stored activations.
        """

        self.activations.clear()

        logger.info("Previous activations cleared.")

    def store(self, outputs):
        """
        Store captured layer outputs.

        Args:
            outputs (dict): Dictionary of layer outputs.
        """

        self.activations = outputs.copy()

        logger.success(
            f"Stored activations from {len(self.activations)} layers."
        )

    def get_activations(self):
        """
        Return all stored activations.
        """

        return self.activations.copy()

    def get_layer_names(self):
        """
        Return a list of captured layer names.
        """

        return list(self.activations.keys())

    def get_activation(self, layer_name):
        """
        Return the activation for one layer.

        Args:
            layer_name (str): Name of the layer.

        Returns:
            Tensor or None
        """

        return self.activations.get(layer_name)