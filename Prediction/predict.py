import numpy as np
import pandas as pd


data_path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/classification_wise_data.xlsx'

data_path_for_number_by_major = '/Users/Pankaj/Major-Change-Prediction/Prediction/Major by Class.xlsx'

xls = pd.ExcelFile(data_path_for_number_by_major)
Fall_data_by_major = xls.parse('Fall 2016')

sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']


major_type = Fall_data_by_major['Majors']
fall_freshman = Fall_data_by_major['FR Freshman']

print(major_type)
print(fall_freshman)

for fall_data in Fall_data_by_major:
    print(fall_data)
    # for major in sciene_and_technology:
    #     if()




# for data in Fall_data_by_major:
#     print(Fall_data_by_major['FR'])

#
# xls = pd.ExcelFile(data_path)
# FR = xls.parse('FR')
# SO = xls.parse('SO')
# JR = xls.parse('JR')
# SR = xls.parse('SR')





# Initialize number of freshman , sophomore, juniors, seniors for each major
#



# calculate the probability transition matrix for freshman, sophomores, juniors and seniors
# 4 ----> 7 by 7 matrix


# Use Bayes Theorem to calculate the total probability

# 1 ------> 7 by 7 matrix























#
#
#
# sciene_and_technology_total_students_enrolled_fall = [781 / 4, 110 / 4, 444 / 4, 403 / 4, 57 / 4, 51 / 4, 0 / 4]
# total_freshman = 6313
#
# sciene_and_technology_total_students_enrolled_fall[-1] = total_freshman - sum(sciene_and_technology_total_students_enrolled_fall)
#
# print(sciene_and_technology_total_students_enrolled_fall)
#
# sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS', 'IT-BS', 'MATH-BS', 'PHYS-BS', 'Others']
#
# probability_matrix = np.zeros((7,7))
#
#
#
#
# def create_probability_matrix(df1, total_students_df1):
#
#     total_students_df1 = total_students_df1
#
#     for index, major in enumerate(sciene_and_technology):
#         for index2, major2 in enumerate(sciene_and_technology):
#             a = df1[(df1['Major Beginning of Semester'] == major) & (df1['Major End of Semester'] == sciene_and_technology[index2])]
#             print('Check check')
#             print(a)
#             probability_matrix[index][index2] = len(a.index)
#
#     #update the diagonal
#     for row in range(probability_matrix.shape[0]):
#         all_other_rows = [x for i, x in enumerate(probability_matrix[row]) if i != row]
#
#         probability_matrix[row][row] = total_students_df1[row] - sum(all_other_rows)
#
#
#     return probability_matrix
#     #convert into probability
#     # for row in range(probability_matrix.shape[0]):
#     #     for column in range(probability_matrix.shape[1]):
#     #         probability_matrix[row][column] = probability_matrix[row][column] / total_students_df1[row]
#     #
#     # return probability_matrix
#
#
# def main():
#     return 0
#
#
# if __name__ == '__main__':
#
#     pm1 = create_probability_matrix(FR, sciene_and_technology_total_students_enrolled_fall)
#     #pm2 = create_probability_matrix(SO, 2135)
#     #pm3 = create_probability_matrix(JR, 2022)
#     #pm4 = create_probability_matrix(SR, 3089)
#
#     np.savetxt('FR transitionmatrix', pm1)
