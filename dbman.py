'''
--- DBMAN ---
Data base manager for UMDAc-Neural-Network project.
'''

import csv
import os
import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

class DBMan():

    def __init__(self, 
                 main_dir='results', 
                 db_dir='db'):

        self.MAIN_DIR = main_dir 
        self.DB_DIR = db_dir

        def _chdir_main(main_dir):
            ## Move working directory to main dir
            print('[*] Changing working directory to ', main_dir)
            os.chdir(main_dir)
    
        ## Check for arguments
        import sys
        args = sys.argv[1:]

        if len(args) > 0:

            if args[0] == '--builder' or args[0] == '-w':
                self.builder()
                quit()

            elif args[0] == '--evaluate':
                _chdir_main(main_dir)
                
                ids = args[1].split(',')
                ids = list(map(int, ids))

                self.evaluate(ids)
                quit()

            elif args[0] == '--plot':
                _chdir_main(main_dir)
                ID = int(args[1].split(',')[0])
                self.plot_db(ID)
                quit()

            elif args[0] == '-h' or args[0] == '--help':
                print('''Welcome to dbman's help page''', '\n')
                print('Examples of use:')
                print('  python dbman.py [args] [options]', '\n')
                print('-w, --builder             Wizard to help with db filesystem')
                print('--evaluate id0, id1...   Evaluate specified id experiments')
                print('--plot id                Plot graph of a certain experiment. Requires specifying id number.')
                print('-h                       Show this help page')
                quit()

        _chdir_main(main_dir)
        
        ## Check for main log file
        if 'main.csv' in glob.glob('*.csv'):

            print('[*] Main log found!')
        else:
            print('[!] Warning: Main log not found.')

    def init_main(self):

        main = open('main.csv', 'w')

        fieldnames = ['id', 'Algorithm', 'Environment', 
                     'Repetitions','Repetition_id',
                     'Population', 'Generations', 
                     'Survivors', 'Random survivors', 'n', 'Noise',
                     'Average', 'Median', 'Maximum', 'Minimum']

        writer = csv.DictWriter(main, fieldnames=fieldnames)

        writer.writeheader()

        main.close()
        print('[*] Main log file created. So fresh!')
    
    def get_main(self):
        return pd.read_csv('main.csv')

    def get_eval(self):
        return pd.read_csv('evaluation.csv')

    def get_db(self, db_id):
        ## Change working dir
        os.chdir(self.DB_DIR)

        ## File name
        fname = str(db_id)+'.csv'
        f = pd.read_csv(fname)

        ## Back to main dir
        os.chdir('../')

        return f 

    def plot_db(self, ID):

        sns.set_style('darkgrid')

        data = self.get_db(ID)

        data_max = data['Maximum'].values.tolist()
        data_min = data['Minimum'].values.tolist()
        data_avg = data['Average'].values.tolist()

        x = list(range(len(data_max)))

        plt.plot(x, data_avg, label='Average')
        plt.plot(x, data_max, label='Maximum')
        plt.plot(x, data_min, label='Minimum')
        plt.legend()

        plt.show()

    def builder(self):

        ## Clean terminal
        print('\033c')
        print('Welcome to dbman builder!')
        print('')
        print('-'*4, ' Options ', '-'*4)
        print('[1] Reset db and main logger')
        print('[2] Create db file system')
        print('[3] Create or reset evaluation db')
        print('[0] Exit')
        print('')

        s = None
        while s not in range(4):
            s = int(input('Select a given option >'))

        print('')

        if s == 0:
            print('Bie!')
            quit()

        elif s == 1:

            if input('Are you sure you want to reset all db and main logger? Existing data will be  deleted! [y/N] ') == 'y':

                ## Move working directory to main dir
                print('[*] Changing working directory to ', self.MAIN_DIR)
                os.chdir(self.MAIN_DIR)

                ## Clean all data from db
                os.system('rm '+self.DB_DIR+'/*')
                print('[*] db cleaned!')

                ## Reset mainlog
                self.init_main()

            else:
                print('')
                print('Nothing to do, quitting...')
                quit()

        elif s == 2:

            if input('Are you sure you want to reset all db and main logger? Existing data will be  deleted! [y/N] ') == 'y':

                ## Create filesystem
                os.system('mkdir '+self.MAIN_DIR)
                print('[*] Main directory created as: '+self.MAIN_DIR)

                ## Move working directory to main dir
                print('[*] Changing working directory to ', self.MAIN_DIR)
                os.chdir(self.MAIN_DIR)

                os.system('mkdir '+self.DB_DIR)
                print('[*] db directory created as: '+self.DB_DIR)

                ## Reset mainlog
                self.init_main()

            else:
                print('')
                print('Nothing to do, quitting...')
                quit()

        elif s == 3:
            if input('Are you sure you want to reset the evaluation log? Existing data will be deleted! [y/N] ') == 'y':
                ## Move working directory to main dir
                print('[*] Changing working directory to ', self.MAIN_DIR)
                os.chdir(self.MAIN_DIR)

                # Build eval db
                evalog = open('evaluation.csv', 'w')

                evalfields=['id','Algorithm', 
                            'Environment', 
                            'Total reward'] 

                writer = csv.DictWriter(evalog, fieldnames=evalfields)

                writer.writeheader()

                evalog.close()

                print('[*] Evaluation log file created. So fresh!')

            else:
                print('Nothing to do. Quitting...')
                quit()


    def evaluate(self, ids):

        from tqdm import tqdm
        from UMDAc.UMDAc import UMDAc
        from UMDAc.Wrappers.Gym import Gym
        from GA.GA import GA

        max_steps = input('Maximum step number [None]:')
        if max_steps == '':
            max_steps = None

        else:
            max_steps = int(max_steps)
        
        action_mode = None
        while action_mode not in range(2): 
            action_mode = input('action mode [0:raw/1:argmax]:')
            action_mode = int(action_mode)

        if action_mode == 0:
            action_mode = 'raw'
        elif action_mode == 1:
            action_mode = 'argmax'

        repetitions = input('Repetitions [100]:')
        if repetitions == '':
            repetitions = 100
        else:
            repetitions = int(repetitions)

        print('')
        print('--- Selected options ---')
        print('Maximum steps: ', max_steps)
        print('Action mode: ', action_mode)
        print('Repetitions: ', repetitions)
        print('')

        if input('Are you sure to continue? [N/y] >') != 'y':
            print('aborting...')
            quit()

        print('')

        ## Open evaluation log
        evalog = open('evaluation.csv', 'a')

                
        evalwriter = csv.DictWriter(evalog, 
            fieldnames=['id','Algorithm', 
                        'Environment', 
                        'Total reward']) 

        for ID in ids:

            print('Experiment: ', ID)

            ## Get experiment's environment
            mainlog = self.get_main()
            env = mainlog.loc[mainlog['id']==ID]['Environment']
            env = list(env)[0]

            ## Get algorithm used in experiment
            alg = mainlog.loc[mainlog['id']==ID]['Algorithm']
            alg = list(alg)[0]

            ## Init env
            problem = Gym(env,
                          iterations=1,
                          max_steps=max_steps,
                          action_mode=action_mode)

            ## Select algorithm
            if alg == 'UMDAc':

                algorithm = UMDAc(model=None,
                             problem=problem,
                             gen_size=None)
                
            elif alg == 'GA':

                algorithm = GA(model=None,
                             problem=problem,
                             gen_size=None)
            else:
                print('Error, invalid algorithm name, name found:', alg) 
                quit()

            algorithm.load_model('db/'+str(ID)+'.h5')

            for i in tqdm(range(repetitions)):
                ## Evaluate specimen, render enabled
                tr = problem.evaluate(specimen=None,
                                     model=algorithm.model,
                                     render=False,
                                     verbose=False)

                evalwriter.writerow({'id':ID,
                                     'Algorithm':alg,
                                     'Environment':env,
                                     'Total reward':tr})
        evalog.close()

if __name__ == '__main__':
    
    import seaborn as sns

    # sns.set_style('darkgrid')

    dbman = DBMan()

    data = dbman.get_eval()

    # data = data.loc[data['Environment']=='LunarLanderContinuous-v2']
    # data = data.loc[data['Environment']=='CartPole-v0']

    # sns.catplot(x = 'Environment', y ='Total reward', 
    #             hue='Algorithm', kind='box', data=data) 
    # plt.show()

    # sns.catplot(x = 'Environment', y ='Total reward', 
    #             hue='Algorithm', split=False, 
    #             kind='violin',data=data) 

    # plt.show()

    sns.set_style('whitegrid')
    sns.set(font_scale=1.3)

    g = sns.catplot(x = 'Environment', y ='Total reward', 
                hue='Algorithm', split=True, 
                kind='violin',data=data) 

    g.set_xticklabels(rotation=10)

    plt.show()
