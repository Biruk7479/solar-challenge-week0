"""
Test module for data validation utilities
"""
import pytest


def test_environment_setup():
    """Test that the environment is properly configured"""
    import pandas as pd
    import numpy as np
    import matplotlib
    import seaborn
    
    assert pd.__version__ >= '2.0.0'
    assert np.__version__ >= '1.24.0'
    

def test_data_directory_structure():
    """Test that required directories exist"""
    import os
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if main directories exist
    assert os.path.exists(os.path.join(base_dir, 'notebooks'))
    assert os.path.exists(os.path.join(base_dir, 'src'))
    assert os.path.exists(os.path.join(base_dir, 'scripts'))
    assert os.path.exists(os.path.join(base_dir, 'tests'))
