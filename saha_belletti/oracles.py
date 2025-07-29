"""
Oracle implementations for the quantum K-coloring problem.

This module provides a unified interface to all oracle implementations:
- Simple Oracle (minimum depth, maximum width)
- Minimal Oracle (minimum width, maximum depth)
- Balanced Oracle (balanced depth and width)
- Original Oracle (from the original research paper)
"""

from .simple import simple_system
from .minimal import minimal_system
from .balanced import balanced_system
from .original import original_system

__all__ = [
    'simple_system',
    'minimal_system', 
    'balanced_system',
    'original_system'
]
