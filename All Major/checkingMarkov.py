import pandas as pd
import numpy as np
from os import path
import matplotlib.pyplot as plt

semester = ['Spring', 'Fall']
classification_list = ['FR', 'SO', 'JR', 'SR']


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

    #print(exponent_transition_matrix)

    # is_Regular = True
    #
    # for row  in transition_matrix.shape[0]:
    #     for column in transition_matrix.shape[1]:
    #
    #         if(transition_matrix[row][column] == 0):
    #             is_Regular = False
    #             transition_matrix = np.dot(transition_matrix, transition_matrix)


if __name__ == '__main__':

    # this loop runs 8 times ( 4 classificaiton (FR, SO, JR, SR) * 2 semester (Fall , Spring))
    # checking if all the individual 8 are regular markov chains.
    for classification in classification_list:
        for semester in ['Spring', 'Fall']:

            path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/' + semester + classification
            file_name = '/TransitionProbabilityMatrixSuccess.txt'

            data = pd.read_csv( path_to_get +file_name, sep=" ", header=None)
            #check_regular_markov_chain(data, 200)

    # combinig transition matrix year wise (FR , SO , JR, SR of both semesters)
    for classification in classification_list:

        fall_data = []
        spring_data = []
        for semester in ['Spring', 'Fall']:
            path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/' + semester + classification
            file_name = '/TransitionProbabilityMatrixSuccess.txt'

            if semester == 'Spring':
                spring_data = np.array(pd.read_csv( path_to_get +file_name, sep=" ", header=None))
            else:
                fall_data = np.array(pd.read_csv( path_to_get +file_name, sep=" ", header=None))

        overall_data = ( np.array(fall_data) + np.array(spring_data) )/ 2

        check_regular_markov_chain(overall_data, 2500)
        #check_normality(overall_data)