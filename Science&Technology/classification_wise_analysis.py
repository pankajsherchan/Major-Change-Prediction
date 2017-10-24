import numpy as np
import pandas as pd
from pandas import ExcelWriter


path = '/Users/Pankaj/Major-Change-Prediction/Science&Technology/Both Semester.xlsx'
xls = pd.ExcelFile(path)
FR = xls.parse('FR')
SO = xls.parse('SO')
JR = xls.parse('JR')
SR = xls.parse('SR')


sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_total_students_enrolled_fall = [781, 110, 444, 403, 57, 51, 0]
sciene_and_technology_total_students_enrolled_spring = [645,71,261,203,48,50, 0]

classification_list = ['FR', 'SO', 'JR', 'SR']


sciene_and_technology_total_students_enrolled_fall[-1] = 14499 - sum(sciene_and_technology_total_students_enrolled_fall)
sciene_and_technology_total_students_enrolled_spring[-1] = 10000 - sum(sciene_and_technology_total_students_enrolled_spring)
total_students_enrolled = sciene_and_technology_total_students_enrolled_fall + sciene_and_technology_total_students_enrolled_spring


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

def classify_data(df, semester):
    writer = pd.ExcelWriter(semester + '.xlsx')
    for i, classification in enumerate(classification_list):
        print(classification)
        classified_data = df[df['Class'] == classification]
        print(classification)
        print(classified_data)

        classified_data.to_excel(writer, classification)
        #df2.to_excel(writer, 'Sheet' + (i+1))
        writer.save()
        #classified_data.to_excel(classification + '.excel', sep='\t', encoding='utf-8', index=False)



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


    #create probability matrix
    pm1 = create_probability_matrix(FR, total_students_enrolled)
    pm2 = create_probability_matrix(SO, total_students_enrolled)


    # #pm2 = create_probability_matrix(df2, sciene_and_technology_total_students_enrolled_spring)
    #
    # print('Pm1')
    # print(pm1)
    #
    #
    # print('Pm 2')
    # print(pm2)
    #
    # final_pm = [x / 2 for x in (pm1 + pm2)]
    #
    # print('Final Pm')
    # print(final_pm)
    #
    # np.savetxt('TransitionProbabilityMatrix.txt', final_pm)

    np.savetxt('FR transitionmatrix', pm1)


if __name__ == "__main__":
    main()
