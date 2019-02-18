import numpy as np

import keras
from keras.datasets import boston_housing


class Boston():

    def __init__(self, data_indx=0):
        
        ## Load dataset
        (self.x_train, self.y_train), (self.x_test, 
                    self.y_test) = boston_housing.load_data()

        self.indx = data_indx

    def evaluate(self, specimen, model, 
                 verbose=False, test_data=False):
            
        ## Load specimen
        model.set_weights(specimen)
        
        if not test_data:
            e = model.evaluate(x=self.x_train,
                                  y=self.y_train,
                                  verbose=0)
        else:
            e = model.evaluate(x=self.x_test,
                                  y=self.y_test,
                                  verbose=0)
        if len(e) > 1:

            if verbose:
                print('Fitness: ', e[self.indx])
            return e[self.indx]    

        else:

            if verbose:
                print('Fitness: ', e)
            return e

if __name__ == '__main__':
    
    boston = Boston()

    print('x train: ', boston.x_train.shape)
    print('y train: ', boston.y_train.shape)

    print('')
    print('x test: ', boston.x_test.shape)
    print('y test: ', boston.y_test.shape)

    print('')
    print(boston.x_train[0])
    print(boston.y_train[0])

