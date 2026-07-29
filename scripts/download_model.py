from pathlib import Path

from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "sshleifer/tiny-gpt2"
SAVE_DIR = Path("models/tiny-gpt2")


def main():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading tokenizer: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print(f"Downloading model: {MODEL_NAME}")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    tokenizer.save_pretrained(SAVE_DIR)
    model.save_pretrained(SAVE_DIR)

    print(f"\nModel saved to: {SAVE_DIR.resolve()}")


if __name__ == "__main__":
    main()