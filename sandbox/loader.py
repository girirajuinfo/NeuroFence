from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "distilgpt2"

def load_model():
    try:
        print(f"Loading model: {MODEL_NAME}")

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float32
        )

        print("\nModel loaded successfully!\n")

        print(f"Model Name      : {MODEL_NAME}")
        print(f"Model Type      : {model.config.model_type}")
        print(f"Hidden Size     : {model.config.n_embd}")
        print(f"Layers          : {model.config.n_layer}")
        print(f"Vocabulary Size : {model.config.vocab_size}")

        return tokenizer, model

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    load_model()