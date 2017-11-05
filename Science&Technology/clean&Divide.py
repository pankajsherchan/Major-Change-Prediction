import numpy as np
import pandas as pd
from pandas import ExcelWriter

# path = '/Users/Pankaj/Major-Change-Prediction/All Major/Data/Updated/Majors Changed Updated.xlsx'
path = '/Users/Pankaj/Major-Change-Prediction/All Major/Majors Changed-2.xlsx'

pd.options.mode.chained_assignment = None
xls = pd.ExcelFile(path)
fall_2010 = xls.parse('Fall 2010')
spring_2011 = xls.parse('Spring 2011')
fall_2011 = xls.parse('Fall 2011')
spring_2012 = xls.parse('Spring 2012')
fall_2012 = xls.parse('Fall 2012')
spring_2013 = xls.parse('Spring 2013')
fall_2013 = xls.parse('Fall 2013')
spring_2014 = xls.parse('Spring 2014')
fall_2014 = xls.parse('Fall 2014')
spring_2015 = xls.parse('Spring 2015')
fall_2015 = xls.parse('Fall 2015')
spring_2016 = xls.parse('Spring 2016')
fall_2016 = xls.parse('Fall 2016')
spring_2017 = xls.parse('Spring 2017')


total_data = [fall_2010, spring_2011, spring_2011, fall_2011, spring_2012, fall_2012, spring_2013, fall_2013, spring_2014, fall_2014, spring_2015, spring_2016, fall_2016, spring_2017]
    #, fall_2013, spring_2014, fall_2014, spring_2015, fall_2015, spring_2016, fall_2016, spring_2017]

total_data = pd.concat(total_data)


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


major_list = [major for major_list in sciene_and_technology.values() for major in major_list]

classification_list = ['FR', 'SO', 'JR', 'SR']



def cleanup_data(df):

    # need to remove the major change from Bachelor in Nursing(NURS-BS) to Registered Bachelor in Nursing(NURS-BSN)
    # not a actual major change
    df = df.drop( df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

    df.loc[ df['Major Beginning of Semester'] == 'IT-AAS' , 'Major Beginning of Semester'] = 'IT-BS'
    df.loc[ df['Major End of Semester'] == 'IT-AAS' , 'Major End of Semester'] = 'IT-BS'


    # change all the other majors(other than science and technology)  to others
    for data1, data2 in zip(df['Major End of Semester'], df['Major Beginning of Semester']):
        if (data1 not in major_list):
            df.loc[df['Major End of Semester'] == data1, 'Major End of Semester'] = 'Others'

        if (data2 not in major_list):
            df.loc[df['Major Beginning of Semester'] == data2, 'Major Beginning of Semester'] = 'Others'

    return df

def classify_data(df, semester, howmanymajors):
    writer = pd.ExcelWriter(howmanymajors + '_' + semester + '.xlsx')
    for i, classification in enumerate(classification_list):
        classified_data = df[df['Class'] == classification]
        classified_data.to_excel(writer, classification, index = False)
        writer.save()

def main():
    clean_df = cleanup_data(total_data)
    classify_data(clean_df, 'BothSemester', 'ScienceTech')

if __name__ == "__main__":
    main()
