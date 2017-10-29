import numpy as np
import pandas as pd
from pandas import ExcelWriter


path = '/Users/Pankaj/Major-Change-Prediction/All Major/Data/Updated/Majors Changed Updated.xlsx'
xls = pd.ExcelFile(path)
fall_data = xls.parse('Fall 2016')
spring_data = xls.parse('Spring 2017')


sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
classification_list = ['FR', 'SO', 'JR', 'SR']

total_majors = len(sciene_and_technology)
probability_matrix = np.zeros((total_majors ,total_majors))

def cleanup_data(df):

    # need to remove the major change from Bachelor in Nursing(NURS-BS) to Registered Bachelor in Nursing(NURS-BSN)
    # not a actual major change
    df = df.drop( df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

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
        classified_data = df[df['Class'] == classification]
        classified_data.to_excel(writer, classification)
        writer.save()

def main():
    clean_df1 = cleanup_data(fall_data)
    clean_df2 = cleanup_data(spring_data)


    result = fall_data.groupby(['Major Beginning of Semester']).agg({'Major End of Semester': 'count'}).rename(columns={'Major End of Semester': 'COUNT'}).reset_index()

    print(result)

    classify_data(clean_df1, 'fall')
    classify_data(clean_df2, 'spring')

if __name__ == "__main__":
    main()
