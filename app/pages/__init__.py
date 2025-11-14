"""
Pages Package
=============
Contains all page components for the dashboard.
"""

from .origin import show_origin_page
from .data_exploration import show_data_exploration_page
from .eda import show_eda_page
from .conclusions import show_conclusions_page

__all__ = [
    'show_origin_page',
    'show_data_exploration_page',
    'show_eda_page',
    'show_conclusions_page'
]
