import numpy as np
import pandas as pd
from pandas import ExcelWriter



path = 'Majors Changed.xlsx'
xls = pd.ExcelFile(path)
df1 = xls.parse('Fall 2016')
df2 = xls.parse('Spring 2017')

df = pd.read_excel('Majors Changed.xlsx')
sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_total_students_enrolled_fall = [781, 110, 444, 403, 57, 51, 0]
sciene_and_technology_total_students_enrolled_spring = [645,71,261,203,48,50, 0]

sciene_and_technology_total_students_enrolled_fall[-1] = 14499 - sum(sciene_and_technology_total_students_enrolled_fall)
sciene_and_technology_total_students_enrolled_spring[-1] = 10000 - sum(sciene_and_technology_total_students_enrolled_spring)

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


probability_matrix = np.zeros((7,7))

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
