# Python Imports
# Third-Party Imports
# Project Imports


def clamp(value: float, minimum_value: float, maximum_value: float) -> float:
    return max(min(maximum_value, value), minimum_value)


def get_percentage_value_from_normalised(normalised_value: float, normalised_minimum: float = 0,
                                         normalised_maximum: float = 100):
    return normalised_value / (normalised_maximum - normalised_minimum) * 100


def get_normalised_value_from_percentage(percentage_value: float, normalised_minimum: float = 0,
                                         normalised_maximum: float = 100):
    return percentage_value * (normalised_maximum - normalised_minimum) / 100
