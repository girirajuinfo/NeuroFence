"""
logger.py

Simple logging utility for NeuroFence.

This module provides consistent logging functions
for information, success, warning, and error messages.
"""

from datetime import datetime


def _timestamp():
    """
    Return the current date and time.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def info(message):
    """
    Display an informational message.
    """
    print(f"[{_timestamp()}] [INFO] {message}")


def success(message):
    """
    Display a success message.
    """
    print(f"[{_timestamp()}] [SUCCESS] {message}")


def warning(message):
    """
    Display a warning message.
    """
    print(f"[{_timestamp()}] [WARNING] {message}")


def error(message):
    """
    Display an error message.
    """
    print(f"[{_timestamp()}] [ERROR] {message}")