import numpy as np
import pandas as pd
from pandas import ExcelWriter
from os.path import join as pjoin
import os
import hickle as hkl
from os import path



path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Both Semester.xlsx'
divided_data_path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/divided_data.xlsx'
classification_wise_data = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/classification_wise_data.xlsx'

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

#
# sciene_and_technology_total_students_enrolled_fall[-1] = 14499 - sum(sciene_and_technology_total_students_enrolled_fall)
# sciene_and_technology_total_students_enrolled_spring[-1] = 10000 - sum(sciene_and_technology_total_students_enrolled_spring)
# total_students_enrolled = sciene_and_technology_total_students_enrolled_fall + sciene_and_technology_total_students_enrolled_spring


probability_matrix = np.zeros((7,7))
number_matrix = np.zeros((7,7))

probability_matrix_success = np.zeros((7,7))
number_matrix_success = np.zeros((7,7))

def cleanup_data(df, total_students, semester):

    # need to remove the major change from Bachelor in Nursing(NURS-BS) to Registered Bachelor in Nursing(NURS-BSN)
    # not a actual major change
    df = df.drop(df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

    # change all the other majors(other than science and technology)  to others
    for data1, data2  in zip(df['Major End of Semester'], df['Major Beginning of Semester']):
        if (data1 not in sciene_and_technology):
            df.loc[df['Major End of Semester'] == data1, 'Major End of Semester'] = 'Others'

        if (data2 not in sciene_and_technology):
            df.loc[df['Major Beginning of Semester'] == data2, 'Major Beginning of Semester'] = 'Others'

    return df

def save_data(df, semester):

    # extract clean the data to excel file
    df.to_csv('Science&TechnologyDataAfterCleaning.csv', sep='\t', encoding='utf-8', index=False)

    writer = ExcelWriter('Science&TechnologyDataAfterCleaning.xlsx')
    df.to_excel(writer, 'Sheet5', index=False)
    writer.save()

def classify_data(df, semester):
    writer = pd.ExcelWriter(semester + '.xlsx')
    for i, classification in enumerate(classification_list):
        classified_data = df[df['Class'] == classification]

        classified_data.to_excel(writer, classification)
        #df2.to_excel(writer, 'Sheet' + (i+1))
        writer.save()
        #classified_data.to_excel(classification + '.excel', sep='\t', encoding='utf-8', index=False)

def divide_low_high_grade_major(df):
    for index , major in enumerate(sciene_and_technology):

            df.loc[ (df['Cum GPA End of Semester'] <= 3.0) & (df['Major End of Semester'] == major), 'Major End of Semester'] = major + 'Lower'
            df.loc[ (df['Cum GPA Beginning of Semester'] <= 3.0) & (df['Major Beginning of Semester'] == major) ,'Major Beginning of Semester'] = major + 'Lower'

            df.loc[ (df['Cum GPA End of Semester'] > 3.0) & (df['Major End of Semester'] == major), 'Major End of Semester'] = major + 'Higher'
            df.loc[ (df['Cum GPA Beginning of Semester'] > 3.0) & (df['Major Beginning of Semester'] == major) , 'Major Beginning of Semester'] = major + 'Higher'
    return df

def create_probability_matrix(df1, sciene_and_technology_total_students_enrolled_persemester):


    for index, major in enumerate(sciene_and_technology):
        for index2, major2 in enumerate(sciene_and_technology):
            a = df1[(df1['Major Beginning of Semester'] == major) & (df1['Major End of Semester'] == sciene_and_technology[index2])]
            number_matrix[index][index2] = len(a.index)

    #update the diagonal
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

    data = fall_FR
    total = sciene_and_technology_total_students_enrolled_fall_freshman

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

    print(classification, semester)

    #create probability matrix
    pm = create_probability_matrix(data, total)
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
    for classification in classification_list:
        for semester in ['Spring', 'Fall']:
            main(classification, semester)

