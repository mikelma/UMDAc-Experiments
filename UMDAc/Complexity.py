'''
Problem complexity as model's number of weight and biases.
'''

import keras
import numpy as np

def Complexity(model):
    ## Get weights
    w = model.get_weights()
    ## Sum number of weight and biases
    s = 0 
    for layer in w:

        if len(layer.shape) == 1:
            s += layer.shape[0]
        else:
            s += layer.shape[0]*layer.shape[1]

    return s
