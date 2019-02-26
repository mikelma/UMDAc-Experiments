import numpy as np
import os
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt

import keras

from keras.models import Model
from keras.layers import Input, Dense

from UMDAc.UMDAc import UMDAc
from UMDAc.Wrappers.Gym import Gym

from Complexity import Complexity

## Initialize model

a = Input(shape=(8,))
b = Dense(4, activation='tanh')(a)

model = Model(inputs=a, outputs=b)

## Model info
model.summary()

## Define model's complexity
n = Complexity(model) 

### HYPERPARAMETERS ###
ALGORITHM = 'UMDAc'

# ENV_NAME = 'CartPole-v0'
ENV_NAME = 'LunarLanderContinuous-v2'

REPETITIONS = 10
ACTION_MODE = 'raw'

GENERATIONS = 3*n
GEN_SIZE = 6*n

SURV = .5
RAND_SURV = .3 
NOISE = .0 

MAX_STEPS = 200
ITERATIONS = 3

MAIN_DIR = 'test_results'
DB_DIR = 'db'
#######################

## Print info 
print('')
print('-'*4, ' PARAMETERS ', '-'*4)
print('Algorithm: ', ALGORITHM)
print('Environment: ', ENV_NAME)
print('Repetitions: ', REPETITIONS)
print('Complexity: ', n)
print('')
print('Generations: ', GENERATIONS)
print('Population size: ', GEN_SIZE)
print('')
print('Max steps: ', MAX_STEPS)
print('Iterations: ', ITERATIONS)
print('')

# if input('Run experiment? [y/N]') != 'y':
#     ## Quit
#     print('')
#     print('Nothing to do, quitting...')
#     quit()

MAIN_FIELDS = ['id', 'Algorithm', 'Environment', 
             'Repetitions','Repetition_id',
             'Population', 'Generations', 
             'Survivors', 'Random survivors', 'n', 'Noise',
             'Average','Median', 'Maximum', 'Minimum']

DB_FIELDS = ['Generation', 'Average', 'Median', 'Maximum', 'Minimum']

## Move working directory
os.chdir(MAIN_DIR)

## List files in db and find next id
import glob

s = glob.glob(os.getcwd()+'/'+DB_DIR+'/*csv')

if len(s) > 0:

    for i, d in enumerate(s):
        s[i] = d.split(os.getcwd()+'/'+DB_DIR+'/')[1]
        s[i] = int(s[i].split('.csv')[0])

    ID = max(s) + 1 ## Initial ID

else:
    ID = 0

for repetiton_id in range(REPETITIONS):

    ## Initialize Gym problem 
    problem = Gym(ENV_NAME,
                  iterations=ITERATIONS,
                  max_steps=MAX_STEPS,
                  action_mode=ACTION_MODE)

    ## Initialize UMDAc
    umdac = UMDAc(model,
                 problem=problem,
                 gen_size=GEN_SIZE)

    ## Write to db
    db = open(DB_DIR+'/'+str(ID)+'.csv', 'w')

    dbwriter = csv.DictWriter(db, fieldnames=DB_FIELDS) 
    dbwriter.writeheader()

    print('Repetition: ', repetiton_id)
    print('id: ', ID)

    ### TRAINING ###
    for generation in tqdm(range(GENERATIONS)):

        ## Train
        history = umdac.train(surv=SURV, 
                    rand_surv=RAND_SURV,
                    noise=NOISE)

        last_avg = history['avg'][-1]
        last_median = np.median(list(umdac.fitness.values()))
        last_max = history['max'][-1]
        last_min = history['min'][-1]

        ## Write generation data to db log
        dbwriter.writerow({'Generation':generation,
                           'Average':last_avg,
                           'Median':last_median,
                           'Maximum':last_max,
                           'Minimum':last_min})

        ## Save best specimen to .h5 file 
        if max(history['max']) == history['max'][-1]:

            names = list(umdac.fitness.keys())
            f = list(umdac.fitness.values())

            best = umdac.gen[names[f.index(max(f))]]
            umdac.save_specimen(best, DB_DIR+'/'+str(ID)+'.h5')

    db.close()

    ## Write experiment info to main logger
    mainlog = open('main.csv', 'a')

    mainwriter = csv.DictWriter(mainlog, fieldnames=MAIN_FIELDS)

    mainwriter.writerow({'id':ID, 
                    'Algorithm':ALGORITHM,
                    'Environment':ENV_NAME,
                    'Repetitions':REPETITIONS,
                    'Repetition_id':repetiton_id,
                    'Generations':GENERATIONS,
                    'Population':GEN_SIZE,
                    'Survivors':SURV,
                    'Random survivors':RAND_SURV if RAND_SURV != None else .0,
                    'n':n,
                    'Noise':NOISE if NOISE != None else .0,
                    'Average':last_avg,
                    'Median':last_median,
                    'Maximum':last_max,
                    'Minimum':last_min}) 
    mainlog.close()

    ## Upddate experiment id
    ID += 1
    print('')

