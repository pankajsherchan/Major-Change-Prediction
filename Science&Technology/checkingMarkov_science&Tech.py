import pandas as pd
import numpy as np
from os import path
import matplotlib.pyplot as plt

semester = ['Spring', 'Fall']
classification_list = ['FR', 'SO', 'JR', 'SR']
classification_list = ['FR']


def scale_dataset(Y):
        mean = np.mean(Y)
        std = np.std(Y)
        Y = (Y - mean) / std
        return Y

def check_normality(M):

    T = range(M.shape[0])
    for i in range(M.shape[1]):
        plt.plot(T, scale_dataset(M[:, i]))

    plt.show()
    return 0


def check_regular_markov_chain(transition_matrix, power):
    exponent_transition_matrix = np.linalg.matrix_power(transition_matrix, power)
    print('Total non zeros ' , np.count_nonzero(exponent_transition_matrix))
    print(exponent_transition_matrix)
if __name__ == '__main__':

    # this loop runs 8 times ( 4 classificaiton (FR, SO, JR, SR) * 2 semester (Fall , Spring))
    # checking if all the individual 8 are regular markov chains.
    for classification in classification_list:

            path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/' + classification
            file_name = '/TransitionProbabilityMatrix.txt'

           # '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/FR/ TransitionProbabilityMatrix.txt

            data = pd.read_csv( path_to_get +file_name, sep=" ", header=None)
            #check_regular_markov_chain(data, 200)

    # combinig transition matrix year wise (FR , SO , JR, SR of both semesters)
    for i in range(1):
        print('This is ' + str(i) + 'try')
        for classification in classification_list:

            spring_data = []
            path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/'  + classification
            file_name = '/TransitionProbabilityMatrix.txt'
            data = np.array(pd.read_csv( path_to_get +file_name, sep=" ", header=None))

            check_regular_markov_chain(data, 150)
            #check_normality(overall_data)