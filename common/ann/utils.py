from math import exp


def sigmoid_function(x):
    return 1 / (1 + exp(-x))


def step_function(x, threshold=0.5):
    return 1 if x > threshold else 0
