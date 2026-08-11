"""
anomaly.py

Analyze neuron activations collected during model execution.
"""

import torch

from utils import logger


class ActivationAnalyzer:
    """
    Analyze activation tensors and calculate statistics.
    """

    def calculate_mean(self, activation):
        """
        Calculate the mean value of an activation tensor.

        Args:
            activation (torch.Tensor)

        Returns:
            float
        """
        return torch.mean(activation.float()).item()

    def calculate_std(self, activation):
        """
        Calculate the standard deviation of an activation tensor.

        Args:
            activation (torch.Tensor)

        Returns:
            float
        """
        return torch.std(activation.float()).item()

    def find_spikes(self, activation, threshold=3.0):
        """
        Find activation values greater than the threshold.

        Args:
            activation (torch.Tensor)
            threshold (float)

        Returns:
            int: Number of spike values.
        """
        return int(torch.sum(activation > threshold).item())

    def find_dormant_neurons(self, activation, threshold=0.01):
        """
        Count activation values close to zero.

        Args:
            activation (torch.Tensor)
            threshold (float)

        Returns:
            int: Number of dormant neurons.
        """
        return int(torch.sum(torch.abs(activation) < threshold).item())

    def generate_statistics(self, activation):
        """
        Generate statistics for a single activation tensor.

        Args:
            activation (torch.Tensor)

        Returns:
            dict
        """
        return {
            "mean": self.calculate_mean(activation),
            "std": self.calculate_std(activation),
            "spikes": self.find_spikes(activation),
            "dormant_neurons": self.find_dormant_neurons(activation),
        }

    def analyze(self, activations):
        """
        Analyze all captured layer activations.

        Args:
            activations (dict)

        Returns:
            dict
        """
        logger.info("Analyzing captured activations...")

        results = {}

        for layer_name, activation in activations.items():

            # Handle tuple/list outputs from the HookManager
            if isinstance(activation, list):
                if not activation:
                    continue
                activation = activation[0]

            if not isinstance(activation, torch.Tensor):
                continue

            results[layer_name] = self.generate_statistics(activation)

        logger.success(
            f"Generated statistics for {len(results)} layers."
        )

        return results