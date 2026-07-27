from pathlib import Path

REQUIRED_FILES = [
    "config.json",
    "tokenizer.json"
]

OPTIONAL_MODEL_FILES = [
    "model.safetensors",
    "pytorch_model.bin"
]


def validate_model(model_path):
    model_path = Path(model_path)

    if not model_path.exists():
        print("❌ Model directory not found.")
        return False

    missing = []

    for file in REQUIRED_FILES:
        if not (model_path / file).exists():
            missing.append(file)

    model_exists = False

    for file in OPTIONAL_MODEL_FILES:
        if (model_path / file).exists():
            model_exists = True

    if not model_exists:
        missing.append("model.safetensors OR pytorch_model.bin")

    if missing:
        print("\n❌ Validation Failed\n")

        for item in missing:
            print(f"Missing: {item}")

        return False

    print("\n✅ Model validation successful.")
    return True


if __name__ == "__main__":
    validate_model("models")