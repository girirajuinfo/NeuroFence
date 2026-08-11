import unittest
import torch

from sandbox.loader import ModelLoader
from tracker.hooks import HookManager


MODEL_PATH = "models/tiny-gpt2"


class TestHookManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.tokenizer, cls.model = ModelLoader.load(MODEL_PATH)

    def setUp(self):
        self.hook_manager = HookManager()

    def test_register_hooks(self):
        """Verify hooks are registered."""

        self.hook_manager.register_hooks(self.model)

        self.assertGreater(len(self.hook_manager.handles), 0)

        self.hook_manager.remove_hooks()

    def test_capture_outputs(self):
        """Verify activations are captured."""

        self.hook_manager.register_hooks(self.model)

        inputs = self.tokenizer(
            "What is Artificial Intelligence?",
            return_tensors="pt"
        )

        with torch.no_grad():
            self.model(**inputs)

        outputs = self.hook_manager.get_outputs()

        self.assertGreater(len(outputs), 0)

        self.hook_manager.remove_hooks()

    def test_remove_hooks(self):
        """Verify hooks are removed."""

        self.hook_manager.register_hooks(self.model)

        self.hook_manager.remove_hooks()

        self.assertEqual(len(self.hook_manager.handles), 0)


if __name__ == "__main__":
    unittest.main()