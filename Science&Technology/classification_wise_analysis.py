import numpy as np
import pandas as pd
import os



only_fall_data = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/fall.xlsx'

only_spring_data = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/spring.xlsx'


xls = pd.ExcelFile(only_fall_data)
fall_FR = xls.parse('FR')
fall_SO = xls.parse('SO')
fall_JR = xls.parse('JR')
fall_SR = xls.parse('SR')

xls_spring = pd.ExcelFile(only_spring_data)
spring_FR = xls_spring.parse('FR')
spring_SO = xls_spring.parse('SO')
spring_JR = xls_spring.parse('JR')
spring_SR = xls_spring.parse('SR')





sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_division = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS']

divided_majors = np.array([ [major+ 'Higher' , major + 'Lower']  for major in sciene_and_technology]).ravel()

total_freshman_fall = 3626
total_freshman_spring = 2627

total_sophomore_fall = 2131
total_sophomore_spring = 2001

total_junior_fall = 2019
total_junior_spring = 1980

total_senior_fall = 3087
total_senior_spring = 3060

sciene_and_technology_total_students_enrolled_fall_freshman = [330, 44, 135, 55, 13, 25, 3024]
sciene_and_technology_total_students_enrolled_sprint_freshman = [233, 25, 97, 43, 5, 16, 2208]

sciene_and_technology_total_students_enrolled_fall_sophomore = [162, 22, 54, 39, 8, 8, 1838]
sciene_and_technology_total_students_enrolled_spring_sophomore = [143, 15, 50, 40, 11, 12, 1730]


sciene_and_technology_total_students_enrolled_fall_junior = [124, 16, 48, 40, 11, 6, 1774]
sciene_and_technology_total_students_enrolled_spring_junior = [119, 14, 49, 48, 10, 6, 1734]


sciene_and_technology_total_students_enrolled_fall_senior = [155, 24, 84, 70, 23, 10, 2721]
sciene_and_technology_total_students_enrolled_spring_senior = [156, 24, 87, 69, 22, 10, 3060]



classification_list = ['FR', 'SO', 'JR', 'SR']

# Initialize probability matrix and number matrix
probability_matrix = np.zeros((7,7))
number_matrix = np.zeros((7,7))

probability_matrix_success = np.zeros((7,7))
number_matrix_success = np.zeros((7,7))

def create_probability_matrix(df1, sciene_and_technology_total_students_enrolled_persemester):

    # checking if the major A has changed to major B
    for index, major in enumerate(sciene_and_technology):
        for index2, major2 in enumerate(sciene_and_technology):
            a = df1[(df1['Major Beginning of Semester'] == major) & (df1['Major End of Semester'] == sciene_and_technology[index2])]
            number_matrix[index][index2] = len(a.index)

    # since the data have only major change data. we need to update the major staying
    # from Major A to major A. Total students in a Major A of a semester - total students changing major from A
    for row in range(number_matrix.shape[0]):
        all_other_rows = [x for i, x in enumerate(number_matrix[row]) if i != row]
        number_matrix[row][row] = sciene_and_technology_total_students_enrolled_persemester[row] - sum(all_other_rows)


    #convert into probability
    for row in range(probability_matrix.shape[0]):
        for column in range(probability_matrix.shape[1]):
            probability_matrix[row][column] = number_matrix[row][column] / sciene_and_technology_total_students_enrolled_persemester[row]

    return probability_matrix, number_matrix

def create_probability_matrix_success(df, total):

    # get the total number of success
    success = []
    for index, major in enumerate(sciene_and_technology):
        major_success = 0
        for index2, major2 in enumerate(sciene_and_technology):
            a = df[ ( df['Major Beginning of Semester'] == major) & (
            df['Major End of Semester'] == sciene_and_technology[index2]) & (df['Cum GPA Beginning of Semester'] < df['Cum GPA End of Semester'])]
            number_matrix_success[index][index2] = len(a.index)
            major_success += len(a.index)
        success.append(major_success)

    # update the diagonal
    for row in range(number_matrix_success.shape[0]):
        all_other_rows = [x for i, x in enumerate(number_matrix_success[row]) if i != row]
        number_matrix_success[row][row] = success[row] - sum(
            all_other_rows)


        # convert into probability
    for row in range(number_matrix_success.shape[0]):
        for column in range(number_matrix_success.shape[1]):
            probability_matrix_success[row][column] = number_matrix_success[row][column] / \
                                             sum(success)

    return probability_matrix_success, number_matrix_success

def main(classification, semester):

    # Initialize data to be freshman fall semester data
    # Initialize total to fall freshman
    data = fall_FR
    total = sciene_and_technology_total_students_enrolled_fall_freshman

    # Conditions to set the right data and total
    if(classification == 'FR' and semester == 'Fall'):
        data = fall_FR
        total = sciene_and_technology_total_students_enrolled_fall_freshman
    elif (classification == 'SO' and semester == 'Fall'):
        data = fall_SO
        total = sciene_and_technology_total_students_enrolled_fall_sophomore
    elif (classification == 'JR' and semester == 'Fall'):
        data = fall_JR
        total = sciene_and_technology_total_students_enrolled_fall_junior
    elif (classification == 'SR' and semester == 'Fall'):
        data = fall_SR
        total = sciene_and_technology_total_students_enrolled_fall_senior
    elif (classification == 'FR' and semester == 'Spring'):
        data = spring_FR
        total = sciene_and_technology_total_students_enrolled_sprint_freshman
    elif (classification == 'SO' and semester == 'Spring'):
        data = spring_SO
        total = sciene_and_technology_total_students_enrolled_spring_sophomore
    elif (classification == 'JR' and semester == 'Spring'):
        data = spring_JR
        total = sciene_and_technology_total_students_enrolled_spring_junior
    elif (classification == 'SR' and semester == 'Spring'):
        data = spring_SR
        total = sciene_and_technology_total_students_enrolled_spring_senior

    # create probability matrix
    pm = create_probability_matrix(data, total)

    # create probability success matrix
    pm_success = create_probability_matrix_success(data, total)


    path_to_save = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Result/'+semester + classification

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
        for semester in ['Spring', 'Fall']:
            main(classification, semester)

