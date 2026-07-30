import unittest

from fuzzer.generator import PromptGenerator


class TestPromptGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = PromptGenerator("fuzzer/prompts.txt")
        self.generator.load_prompts()

    def test_load_prompts(self):
        """Verify prompts load successfully."""
        self.assertGreater(len(self.generator.get_all_prompts()), 0)

    def test_get_prompt(self):
        """Verify a prompt is returned."""
        prompt = self.generator.get_prompt()

        self.assertIsNotNone(prompt)
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 0)

    def test_shuffle_prompts(self):
        """Verify shuffling keeps the same prompts."""

        before = sorted(self.generator.get_all_prompts())

        self.generator.shuffle_prompts()

        after = sorted(self.generator.get_all_prompts())

        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()