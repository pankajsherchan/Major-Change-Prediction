import numpy as np
import pandas as pd
import os


only_fall_data = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/fall.xlsx'

only_spring_data = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/spring.xlsx'

data_path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/ScienceTech_BothSemester.xlsx'

xls = pd.ExcelFile(data_path)
FR = xls.parse('FR')
SO = xls.parse('SO')
JR = xls.parse('JR')
SR = xls.parse('SR')

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


sciene_and_technology = [major for major_list in sciene_and_technology.values() for major in major_list]


total_freshman = len(FR)
total_sophomore = len(SO)
total_junior = len(JR)
total_senior = len(SR)


classification_list = ['FR', 'SO', 'JR', 'SR']

# Initialize probability matrix and number matrix
matrix_size = len(sciene_and_technology)
probability_matrix = np.zeros((matrix_size,matrix_size))
number_matrix = np.zeros((matrix_size,matrix_size))

probability_matrix_success = np.zeros((matrix_size,matrix_size))
number_matrix_success = np.zeros((matrix_size,matrix_size))

def create_probability_matrix(df1):

    scienceAndTechnologyPerClassification = []
    for index, major in enumerate(sciene_and_technology):
        scienceAndTechnologyPerClassification.append(len(df1 [df1['Major Beginning of Semester'] == major].index))

    # checking if the major A has changed to major B
    for index, major in enumerate(sciene_and_technology):
        for index2, major2 in enumerate(sciene_and_technology):
            a = df1[(df1['Major Beginning of Semester'] == major) & (df1['Major End of Semester'] == sciene_and_technology[index2])]
            number_matrix[index][index2] = len(a.index)


    #convert into probability
    for row in range(probability_matrix.shape[0]):
        for column in range(probability_matrix.shape[1]):
            probability_matrix[row][column] = number_matrix[row][column] / scienceAndTechnologyPerClassification[row]

    return probability_matrix, number_matrix

def create_probability_matrix_success(df):

    scienceAndTechnologyPerClassification_success = []
    for index, major in enumerate(sciene_and_technology):

        success = df[(df['Major Beginning of Semester'] == major) &(
               df['Cum GPA Beginning of Semester'] < df['Cum GPA End of Semester'])]
        scienceAndTechnologyPerClassification_success.append(len(success.index))


    # get the total number of success
    for index, major in enumerate(sciene_and_technology):
        major_success = 0
        for index2, major2 in enumerate(sciene_and_technology):
            a = df[ ( df['Major Beginning of Semester'] == major) & (
            df['Major End of Semester'] == sciene_and_technology[index2]) & (df['Cum GPA Beginning of Semester'] < df['Cum GPA End of Semester'])]
            number_matrix_success[index][index2] = len(a.index)

    #convert into probability
    for row in range(number_matrix_success.shape[0]):
        for column in range(number_matrix_success.shape[1]):
            probability_matrix_success[row][column] =  number_matrix_success[row][column] / scienceAndTechnologyPerClassification_success[row]

    return probability_matrix_success, number_matrix_success


def main(classification):

    # Initialize data to be freshman fall semester data
    # Initialize total to fall freshman
    data = FR

    # Conditions to set the right data and total
    if(classification == 'FR'):
        data = FR
    elif (classification == 'SO'):
        data = SO
    elif (classification == 'JR'):
        data = JR
    elif (classification == 'SR'):
        data = SR

    # create probability matrix
    pm = create_probability_matrix(data)

    # create probability success matrix
    pm_success = create_probability_matrix_success(data)


    path_to_save = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/' + classification

    try:
        os.makedirs(path_to_save)
    except OSError:
        if not os.path.isdir(path_to_save):
            raise

    np.savetxt(os.path.join(path_to_save, 'TransitionProbabilityMatrixSuccess.txt'), pm_success[0])
    np.savetxt(os.path.join(path_to_save, 'TransitionNumberMatrixSuccess.txt'), pm_success[1])

    np.savetxt(os.path.join(path_to_save, 'TransitionProbabilityMatrix.txt'), pm[0])
    np.savetxt(os.path.join(path_to_save, 'TransitionNumberMatrix.txt'), pm[1])



if __name__ == "__main__":
    # this loop runs 8 times ( 4 classificaiton (FR, SO, JR, SR) * 2 semester (Fall , Spring))
    for classification in classification_list:
            main(classification)

