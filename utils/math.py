# Python Imports
# Third-Party Imports
# Project Imports


def clamp(value: float, minimum_value: float, maximum_value: float) -> float:
    return max(min(maximum_value, value), minimum_value)


def get_percentage_value_from_normalised(normalised_value: float):
    return normalised_value * 100


def get_normalised_value_from_percentage(percentage_value: float):
    return percentage_value / 100
