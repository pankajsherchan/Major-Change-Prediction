import pandas as pd
import numpy as np


classification_list = ['FR', 'SO', 'JR']


def check_regular_markov_chain(transition_matrix, power):
    exponent_transition_matrix = np.linalg.matrix_power(transition_matrix, power)
    print('Total non zeros ' , np.count_nonzero(exponent_transition_matrix))

def final_transitionmatrix_result():
    classification_wise_success_probability = get_classification_wise_success_probability()

    data_array = []
    for index, classification in enumerate(classification_list):
        path_to_get = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/' + classification
        file_name = '/TransitionProbabilityMatrixSuccess.txt'
        data = pd.read_csv(path_to_get + file_name, sep=" ", header=None)
        data = data * classification_wise_success_probability[index]
        data_array.append(data)

    final_matrix = np.zeros(( len(data_array[0]), len(data_array[0]) ))
    for array in data_array:
        final_matrix += array

    return final_matrix

def get_classification_wise_success_probability():
    data_path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/ScienceTech_BothSemester.xlsx'
    classification_wise_success = []
    xls = pd.ExcelFile(data_path)

    for classification in classification_list:
            df = xls.parse(classification)
            success = df[ (df['Cum GPA Beginning of Semester'] < df['Cum GPA End of Semester']) ]
            classification_wise_success.append(len(success))

    classification_wise_success_probability = [ x / sum(classification_wise_success) for x in classification_wise_success]
    return classification_wise_success_probability

def cleanup_data(df):

    # need to remove the major change from Bachelor in Nursing(NURS-BS) to Registered Bachelor in Nursing(NURS-BSN)
    # not a actual major change
    df = df.drop( df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

    df.loc[ df['Major Beginning of Semester'] == 'IT-AAS' , 'Major Beginning of Semester'] = 'IT-BS'
    df.loc[ df['Major End of Semester'] == 'IT-AAS' , 'Major End of Semester'] = 'IT-BS'

    df = df.drop( df[ df['Cum GPA End of Semester'] == '#NULL!' ].index )

    return df

if __name__ == '__main__':
    final = final_transitionmatrix_result()
    # for i in range(10):
    #     check_regular_markov_chain(final,i )


    path = '/Users/Pankaj/Major-Change-Prediction/All Major/Majors Changed-2.xlsx'
    pd.options.mode.chained_assignment = None
    xls = pd.ExcelFile(path)

    spring_2017 = xls.parse('Spring 2017')

    sciene_and_technology = {}
    sciene_and_technology['Biology'] = ['BIOL-BS']
    sciene_and_technology['Chemistry'] = ['CHEM-BS']
    sciene_and_technology['Computer'] = ['CS-BS']
    sciene_and_technology['EngineeringTechnology'] = ['ENTC-BS']
    sciene_and_technology['IndustrialTechnology'] = ['IT-BS']
    sciene_and_technology['InformationTechnology'] = ['ITEC-BS']
    sciene_and_technology['Math'] = ['MATH-BS']
    sciene_and_technology['Physics'] = ['PHYS-BS']
    sciene_and_technology['Others'] = ['Others']

    major_list = [major for major_list in sciene_and_technology.values() for major in major_list]
    classification_list = ['FR', 'SO', 'JR']
    df = cleanup_data(spring_2017)

    number_matrix_success = []
    for index, major in enumerate(major_list):
        a = df[ ( df['Major Beginning of Semester'] == major) &  (df['Cum GPA Beginning of Semester'] < df['Cum GPA End of Semester'])]
        number_matrix_success.append(len(a.index))

    # define the initial state
    initial_state = [x / sum(number_matrix_success) for x in number_matrix_success]
    print(initial_state)
    initial_state = np.array(initial_state)
    print(type(final))
    for i in range(100):
        print(str(i+1) + 'Round')
        initial_state = initial_state.dot(final)
    # intial success rate for stem

