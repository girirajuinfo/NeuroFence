"""
scorer.py

Calculate a risk level based on activation statistics.
"""

from utils import logger


class RiskScorer:
    """
    Assign a risk level using activation statistics.
    """

    def score(self, statistics):
        """
        Calculate the overall scan risk.

        Args:
            statistics (dict)

        Returns:
            dict
        """

        total_spikes = 0
        total_dormant = 0

        for layer_stats in statistics.values():
            total_spikes += layer_stats["spikes"]
            total_dormant += layer_stats["dormant_neurons"]

        score = total_spikes + total_dormant

        if score == 0:
            level = "Safe"
        elif score <= 10:
            level = "Low"
        elif score <= 25:
            level = "Medium"
        elif score <= 50:
            level = "High"
        else:
            level = "Critical"

        logger.success(
            f"Risk assessment completed: {level}"
        )

        return {
            "risk_level": level,
            "risk_score": score,
            "total_spikes": total_spikes,
            "total_dormant_neurons": total_dormant,
        }