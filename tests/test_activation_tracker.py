import unittest
import torch

from tracker.activation_tracker import ActivationTracker


class TestActivationTracker(unittest.TestCase):

    def setUp(self):
        self.tracker = ActivationTracker()

    def test_store_activations(self):
        """Verify activations are stored correctly."""

        sample = {
            "layer1": torch.tensor([1, 2, 3]),
            "layer2": torch.tensor([4, 5, 6]),
        }

        self.tracker.store(sample)

        self.assertEqual(len(self.tracker.get_activations()), 2)

    def test_get_layer_names(self):
        """Verify layer names are returned."""

        sample = {
            "layer1": torch.tensor([1]),
            "layer2": torch.tensor([2]),
        }

        self.tracker.store(sample)

        names = self.tracker.get_layer_names()

        self.assertIn("layer1", names)
        self.assertIn("layer2", names)

    def test_get_activation(self):
        """Verify a specific activation can be retrieved."""

        tensor = torch.tensor([1, 2, 3])

        self.tracker.store({
            "layer1": tensor
        })

        self.assertTrue(
            torch.equal(
                self.tracker.get_activation("layer1"),
                tensor
            )
        )

    def test_clear(self):
        """Verify activations are cleared."""

        self.tracker.store({
            "layer1": torch.tensor([1])
        })

        self.tracker.clear()

        self.assertEqual(
            len(self.tracker.get_activations()),
            0
        )


if __name__ == "__main__":
    unittest.main()