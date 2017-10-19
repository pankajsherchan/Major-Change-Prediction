import numpy as np
import pandas as pd
from pandas import ExcelWriter


df = pd.read_excel('Majors Changed.xlsx')
sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_total_students_enrolled = [781, 110, 444, 403, 57, 51, 0]

df = df.drop(df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

print(df.describe())
print('Data related to nursing major')
# print(sum(unnecessary_data))

sciene_and_technology_total_students_enrolled[-1] = 14499 - sum(sciene_and_technology_total_students_enrolled)

print('Total number of students enrolled')
print(sciene_and_technology_total_students_enrolled)


#https://www2.southeastern.edu/Administration/Inst-Research/Acadprog/data.cgi?majors.txt
#Enrollement  data
#FALL 2016
#Office of Science & Technology
# 1. Chemistry =  110
# 2. Computer Science = 322 , Information Technology = 122 , so total = 444
# 3. Biology = 781
# 4. Mathematics = 57
# 5. Engeneering Technology = 314 , AAS Industrial technology = 89, BS Occupational Health, Safety & Environment = 147,
#               Total = 314 + 89 = 403
# 6. Physics = 51
# 7. Others


# print(df['Major End of Semester'])
# df.loc[(df['Major End of Semester'] not in sciene_and_technology)] = 'Others'

for data in df['Major End of Semester']:
    if(data not in sciene_and_technology):
        df.loc[df['Major End of Semester'] == data, 'Major End of Semester'] = 'Others'

for data in df['Major Beginning of Semester']:
    if(data not in sciene_and_technology):
        df.loc[df['Major Beginning of Semester'] == data, 'Major Beginning of Semester'] = 'Others'

        # (df['Major End of Semester'] == data) ['Major End of Semester'] = 'Others'
        # print(df['Major End of Semester'])
        # print('Am I here')


df.to_csv('Science&TechnologyDataAfterCleaning.csv', sep='\t', encoding='utf-8', index = False)

writer = ExcelWriter('Science&TechnologyDataAfterCleaning.xlsx')
df.to_excel(writer,'Sheet5', index = False)
writer.save()


probability_matrix = np.zeros((7,7))

data = df.values

for index, major in enumerate(sciene_and_technology):
    for index2, major2 in enumerate(sciene_and_technology):
        a = sum((df['Major Beginning of Semester'] == major) & (df['Major End of Semester'] == sciene_and_technology[index2]))
        probability_matrix[index][index2] = a


print(probability_matrix)

probability_matrix = np.array(probability_matrix)
#
for row in range(probability_matrix.shape[0]):
        print('row number' , row)
        print(probability_matrix[row], 'Probability Matirx row')
        b = [x for i, x in enumerate(probability_matrix[row]) if i != row]
        print('Total major changed' , sum(b))
        probability_matrix[row][row] = sciene_and_technology_total_students_enrolled[row] - sum(b)

print('After reassinging the non changed value')
print(probability_matrix)

for row in range(probability_matrix.shape[0]):
    for column in range(probability_matrix.shape[1]):
        probability_matrix[row][column] = probability_matrix[row][column] / sciene_and_technology_total_students_enrolled[row]

print('After assigning probability')
print(probability_matrix)

np.savetxt('TransitionProbabilityMatrix.txt', probability_matrix)