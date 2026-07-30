"""
hooks.py

Reusable PyTorch forward hook manager for NeuroFence.
"""

import torch

from utils import logger


class HookManager:
    """
    Register and remove forward hooks.
    """

    def __init__(self):
        self.handles = []
        self.outputs = {}

    def _hook(self, layer_name):
        """
        Create a hook function for a layer.
        """

        def hook(module, inputs, output):
            # Store a single tensor output
            if isinstance(output, torch.Tensor):
                self.outputs[layer_name] = output.detach().cpu()

            # Store tensor outputs from tuples/lists
            elif isinstance(output, (tuple, list)):
                tensors = [
                    item.detach().cpu()
                    for item in output
                    if isinstance(item, torch.Tensor)
                ]

                if tensors:
                    self.outputs[layer_name] = tensors

        return hook

    def register_hooks(self, model):
        """
        Register hooks on every module in the model.
        """

        # Remove existing hooks if they were already registered
        if self.handles:
            self.remove_hooks()

        logger.info("Registering forward hooks...")

        self.outputs.clear()

        for name, module in model.named_modules():
            handle = module.register_forward_hook(
                self._hook(name)
            )
            self.handles.append(handle)

        logger.success(f"Registered {len(self.handles)} hooks.")

    def remove_hooks(self):
        """
        Remove all registered hooks.
        """

        logger.info("Removing hooks...")

        for handle in self.handles:
            handle.remove()

        self.handles.clear()

        logger.success("All hooks removed.")

    def get_outputs(self):
        """
        Return captured layer outputs.
        """

        return self.outputs.copy()