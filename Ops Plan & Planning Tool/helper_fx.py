import numpy as np
def custom_round_hiring_needs(value):
    """
    Rounds a value to the nearest 0.5 or whole number based on its proximity to 0.5 or 1.0.
    
    Parameters:
    - value: float, the value to round
    
    Returns:
    - Rounded value as a float
    """
    int_value = int(value)
    abs_value = abs(value - int_value)
    if abs_value > 0.5 and abs_value < 1.0:
        return np.round(value)
    elif abs_value >= 0.1:
        return np.floor(value) + 0.5
    else:
        return 0