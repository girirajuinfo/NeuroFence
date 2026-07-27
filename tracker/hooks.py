activation_outputs = {}

def activation_hook(name):
    def hook(module, inputs, outputs):
        activation_outputs[name] = outputs.detach()

    return hook