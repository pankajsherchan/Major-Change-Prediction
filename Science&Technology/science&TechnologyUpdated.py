import numpy as np
import pandas as pd
from pandas import ExcelWriter


path = '/Users/Pankaj/Major-Change-Prediction/All Major/Data/Updated/Majors Changed Updated.xlsx'
xls = pd.ExcelFile(path)
fall_data = xls.parse('Fall 2016')
spring_data = xls.parse('Spring 2017')

sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_total_students_enrolled_fall = [781, 110, 444, 403, 57, 51, 0]
sciene_and_technology_total_students_enrolled_spring = [645,71,261,203,48,50, 0]
classification_list = ['FR', 'SO', 'JR', 'SR']


sciene_and_technology_total_students_enrolled_fall[-1] = 10863 - sum(sciene_and_technology_total_students_enrolled_fall)
sciene_and_technology_total_students_enrolled_spring[-1] = 9668 - sum(sciene_and_technology_total_students_enrolled_spring)

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

def classify_data(df, semester):
    writer = pd.ExcelWriter(semester + '.xlsx')
    for i, classification in enumerate(classification_list):
        print(classification)
        classified_data = df[df['Class'] == classification]
        print(classification)
        print(classified_data)

        classified_data.to_excel(writer, classification)
        writer.save()


def main():
    clean_df1 = cleanup_data(fall_data, sciene_and_technology_total_students_enrolled_fall, 'fall')
    clean_df2 = cleanup_data(spring_data, sciene_and_technology_total_students_enrolled_spring, 'spring')

    classify_data(clean_df1, 'fall')
    classify_data(clean_df2, 'spring')

if __name__ == "__main__":
    main()
