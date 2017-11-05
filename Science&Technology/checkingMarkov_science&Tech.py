import pandas as pd
import numpy as np
from os import path
import matplotlib.pyplot as plt

semester = ['Spring', 'Fall']
classification_list = ['FR', 'SO', 'JR', 'SR']
# classification_list = ['SR']


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

if __name__ == '__main__':

        for classification in classification_list:
            print(classification)
            for i in range(5):
                print('This is ' + str(i) + 'try')
                path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/'  + classification
                file_name = '/TransitionProbabilityMatrixSuccess.txt'
                data = pd.read_csv( path_to_get +file_name, sep=" ", header=None)
                check_regular_markov_chain(data, i)
