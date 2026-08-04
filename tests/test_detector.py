import unittest
import torch

from detector.anomaly import ActivationAnalyzer
from detector.scorer import RiskScorer


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.analyzer = ActivationAnalyzer()
        self.scorer = RiskScorer()

    def test_mean(self):
        tensor = torch.tensor([1.0, 2.0, 3.0])

        self.assertAlmostEqual(
            self.analyzer.calculate_mean(tensor),
            2.0,
            places=5
        )

    def test_std(self):
        tensor = torch.tensor([1.0, 2.0, 3.0])

        self.assertGreater(
            self.analyzer.calculate_std(tensor),
            0
        )

    def test_spikes(self):
        tensor = torch.tensor([0.0, 5.0, 6.0])

        self.assertEqual(
            self.analyzer.find_spikes(tensor),
            2
        )

    def test_dormant(self):
        tensor = torch.tensor([0.0, 0.005, 1.0])

        self.assertEqual(
            self.analyzer.find_dormant_neurons(tensor),
            2
        )

    def test_analyze(self):
        activations = {
            "layer": torch.tensor([0.0, 5.0])
        }

        result = self.analyzer.analyze(activations)

        self.assertIn("layer", result)
        self.assertIn("mean", result["layer"])
        self.assertIn("std", result["layer"])
        self.assertIn("spikes", result["layer"])
        self.assertIn("dormant_neurons", result["layer"])

    def test_risk_score(self):
        statistics = {
            "layer": {
                "spikes": 2,
                "dormant_neurons": 3
            }
        }

        result = self.scorer.score(statistics)

        self.assertEqual(result["risk_score"], 5)
        self.assertEqual(result["risk_level"], "Low")


if __name__ == "__main__":
    unittest.main()