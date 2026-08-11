import shutil
import tempfile
import unittest
from pathlib import Path

from sandbox.validator import ModelValidator


class TestModelValidator(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary model directory before each test.
        """
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """
        Remove the temporary directory after each test.
        """
        shutil.rmtree(self.temp_dir)

    def test_valid_model_directory(self):
        (self.temp_dir / "config.json").touch()
        (self.temp_dir / "tokenizer_config.json").touch()
        (self.temp_dir / "model.safetensors").touch()

        valid, _ = ModelValidator.validate(self.temp_dir)

        self.assertTrue(valid)

    def test_missing_config(self):
        (self.temp_dir / "tokenizer_config.json").touch()
        (self.temp_dir / "model.safetensors").touch()

        valid, message = ModelValidator.validate(self.temp_dir)

        self.assertFalse(valid)
        self.assertIn("config.json", message)

    def test_missing_weights(self):
        (self.temp_dir / "config.json").touch()
        (self.temp_dir / "tokenizer_config.json").touch()

        valid, message = ModelValidator.validate(self.temp_dir)

        self.assertFalse(valid)
        self.assertIn("weights", message)

    def test_invalid_directory(self):
        valid, _ = ModelValidator.validate("this_folder_does_not_exist")

        self.assertFalse(valid)


if __name__ == "__main__":
    unittest.main()