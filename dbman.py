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

class DBMan():

    def __init__(self, 
                 main_dir='results', 
                 db_dir='db'):

        self.MAIN_DIR = main_dir 
        self.DB_DIR = db_dir
    
        ## Check for arguments
        import sys
        args = sys.argv[1:]

        if len(args) > 0 and (args[0] == '--wizard' or args[0] == '-w'):
            self.wizard()
            quit()

        ## Move working directory to main dir
        print('[*] Changing working directory to ', main_dir)
        os.chdir(main_dir)
        
        ## Check for main log file
        if 'main.csv' in glob.glob('*.csv'):

            print('[*] Main log found!')
        else:
            print('[!] Warning: Main log not found.')

    def init_main(self):

        main = open('main.csv', 'w')

        fieldnames = ['id', 'Algorithm', 'Environment', 
                     'Repetitions','Repetition_id', 
                     'Average','Median', 'Maximum', 'Minimum']

        writer = csv.DictWriter(main, fieldnames=fieldnames)

        writer.writeheader()

        main.close()
        print('[*] Main log file created. So fresh!')
    
    def get_main(self):
        return pd.read_csv('main.csv')

    def get_db(self, db_id):
        ## Change working dir
        os.chdir(self.DB_DIR)

        ## File name
        fname = str(db_id)+'.csv'
        f = pd.read_csv(fname)

        ## Back to main dir
        os.chdir('../')

        return f 

    def wizard(self):

        ## Clean terminal
        print('\033c')
        print('Welcome to dbman wizard!')
        print('')
        print('-'*4, ' Options ', '-'*4)
        print('[1] Reset db and main logger')
        print('[2] Create db file system')
        print('[0] Exit')
        print('')

        s = 99
        while s not in range(3):
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

if __name__ == '__main__':
    
    import seaborn as sns
    sns.set_style('darkgrid')

    dbman = DBMan()

    sns.set_style('darkgrid')

    mainlog = dbman.get_main()

    from ggplot import * 

    a = ggplot(mainlog, aes(x='Algorithm', 
                            y='Average')) + geom_boxplot()
    m = ggplot(mainlog, aes(x='Algorithm', 
                            y='Minimum')) + geom_boxplot()
    M = ggplot(mainlog, aes(x='Algorithm', 
                            y='Maximum')) + geom_boxplot()

    a.show()
    m.show()
    M.show()

    sns.lineplot(x="id", y="Average",
                 data=mainlog)
    plt.show()

