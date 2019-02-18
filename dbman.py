import csv
import os
import glob

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

class DBMan():

    def __init__(self, main_dir, db_dir):

        self.MAIN_DIR = main_dir 
        self.DB_DIR = db_dir

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

    def avg_main(commons=[]):
        pass

    def get_db(self, db_id):
        ## Change working dir
        os.chdir(self.DB_DIR)

        ## File name
        fname = str(db_id)+'.csv'
        f = pd.read_csv(fname)

        ## Back to main dir
        os.chdir('../')

        return f 

    def avg_db():
        pass

if __name__ == '__main__':
    
    import seaborn as sns
    sns.set_style('darkgrid')

    dbman = DBMan(main_dir='results',
                  db_dir='db')

    #if input('Delete existing and create NEW main log? [y/N]') == 'y':
    #    dbman.init_main()
    #    quit()

    # a = dbman.get_db(4)

    sns.set_style('darkgrid')
    #
    # p = sns.relplot(x='Generation', y='Avg_rwd', kind='line',
    #                data=a) 
    # plt.show()

    #quit()

    mainlog = dbman.get_main()

    from ggplot import * 

    # p = ggplot(mainlog, aes('id', 'Average'))
    # p +=  geom_point() + geom_line() + stat_smooth(color='blue')

    # p.show()

    # p = sns.lineplot(x="id", y="Average", 
    #                  hue='Algorithm',
    #                  style="event",
    #                  data=mainlog)

    a = ggplot(mainlog, aes(x='Algorithm', y='Average')) + geom_boxplot()
    m = ggplot(mainlog, aes(x='Algorithm', y='Minimum')) + geom_boxplot()
    M = ggplot(mainlog, aes(x='Algorithm', y='Maximum')) + geom_boxplot()

    # a.show()
    # m.show()
    # M.show()
    sns.lineplot(x="id", y="Average",
                 data=mainlog)
    plt.show()
