import numpy as np
import pandas as pd
from pandas import ExcelWriter


path = '/Users/Pankaj/Major-Change-Prediction/All Major/Data/Old/Majors Changed.xlsx'
xls = pd.ExcelFile(path)
df1 = xls.parse('Fall 2016')
df2 = xls.parse('Spring 2017')

df = pd.read_excel('/Users/Pankaj/Major-Change-Prediction/All Major/Data/Old/Majors Changed.xlsx')

sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_total_students_enrolled_fall = [781, 110, 444, 403, 57, 51, 0]
sciene_and_technology_total_students_enrolled_spring = [645,71,261,203,48,50, 0]

sciene_and_technology_total_students_enrolled_fall[-1] = 14499 - sum(sciene_and_technology_total_students_enrolled_fall)
sciene_and_technology_total_students_enrolled_spring[-1] = 10000 - sum(sciene_and_technology_total_students_enrolled_spring)


probability_matrix = np.zeros((7,7))


def create_probability_matrix(df1, total_students_df1):

    average_total_students = total_students_df1

    for index, major in enumerate(sciene_and_technology):
        for index2, major2 in enumerate(sciene_and_technology):
            a = df1[(df1['Major Beginning of Semester'] == major) & (df1['Major End of Semester'] == sciene_and_technology[index2])]
            # 4 because of 4 semester(Fall and Spring) before graduation
            probability_matrix[index][index2] = 8 * len(a.index)

    #update the diagonal
    for row in range(probability_matrix.shape[0]):
        all_other_rows = [x for i, x in enumerate(probability_matrix[row]) if i != row]

        probability_matrix[row][row] = average_total_students[row] - sum(all_other_rows)


    #convert into probability
    for row in range(probability_matrix.shape[0]):
        for column in range(probability_matrix.shape[1]):
            probability_matrix[row][column] = probability_matrix[row][column] / average_total_students[row]

    return probability_matrix


def main():
    clean_df1 = cleanup_data(df1, sciene_and_technology_total_students_enrolled_fall, 'fall')
    clean_df2 = cleanup_data(df2, sciene_and_technology_total_students_enrolled_spring, 'spring')

    clean_df1.to_csv('cleaned_data_fall.csv', sep='\t', encoding='utf-8', index=False)
    clean_df2.to_csv('cleaned_data_spring.csv', sep='\t', encoding='utf-8', index=False)

    writer = ExcelWriter('cleaned_data.xlsx')
    clean_df1.to_excel(writer, 'Fall Data', index=False)
    clean_df2.to_excel(writer, 'Spring Data', index = False)
    writer.save()


    #create probability matrix
    pm1 = create_probability_matrix(clean_df1, sciene_and_technology_total_students_enrolled_fall)
    pm2 = create_probability_matrix(clean_df2, sciene_and_technology_total_students_enrolled_spring)

    #pm2 = create_probability_matrix(df2, sciene_and_technology_total_students_enrolled_spring)

    print('Pm1')
    print(pm1)


    print('Pm 2')
    print(pm2)

    final_pm = [x / 2 for x in (pm1 + pm2)]

    print('Final Pm')
    print(final_pm)

    np.savetxt('TransitionProbabilityMatrix.txt', final_pm)


if __name__ == "__main__":
    main()
