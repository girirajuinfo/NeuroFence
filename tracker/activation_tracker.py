class ActivationTracker:

    def __init__(self):
        self.activations = {}

    def clear(self):
        self.activations.clear()

    def save(self, layer_name, tensor):
        self.activations[layer_name] = tensor

    def get_all(self):
        return self.activations