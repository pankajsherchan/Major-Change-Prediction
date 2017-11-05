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
sciene_and_technology['IndustrialTechnology'] = ['IT-AAS', 'IT-BS']
sciene_and_technology['InformationTechnology'] = ['ITEC-BS']
sciene_and_technology['Math'] = ['MATH-BS']
sciene_and_technology['Physics'] = ['PHYS-BS']
sciene_and_technology['Others'] = ['Others']


major_list = [major for major_list in sciene_and_technology.values() for major in major_list]

print(type(major_list))


sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'ENTC-BS', 'IT-AAS', 'IT-BS', 'ITEC-BS',  'MATH-BS', 'PHYS-BS', 'Others']
classification_list = ['FR', 'SO', 'JR', 'SR']



# print('Major Beginning of semster spring', len(spring_data['Major Beginning of Semester'].unique()))
#
# print('Major End of semster fall' , len(fall_data['Major End of Semester'].unique()))
# print('Major End of semester Spring', len(spring_data['Major End of Semester'].unique()))
#
#
# # instead of just science and technology, this time use all majors
# all_majors =  list(set( spring_data['Major Beginning of Semester']) | set(fall_data['Major Beginning of Semester'])  | set(fall_data['Major End of Semester']) |set(spring_data['Major End of Semester']))
# classification_list = ['FR', 'SO', 'JR', 'SR']

# total_majors = len(all_majors)
# probability_matrix = np.zeros((total_majors ,total_majors))
#
def cleanup_data(df):

    # need to remove the major change from Bachelor in Nursing(NURS-BS) to Registered Bachelor in Nursing(NURS-BSN)
    # not a actual major change
    df = df.drop( df[(df['Major Beginning of Semester'] == 'NURS-BS') & (df['Major End of Semester'] == 'NURS-BSN')].index)

    # change all the other majors(other than science and technology)  to others
    for data1, data2 in zip(df['Major End of Semester'], df['Major Beginning of Semester']):
        if (data1 not in major_list):
            df.loc[df['Major End of Semester'] == data1, 'Major End of Semester'] = 'Others'

        if (data2 not in major_list):
            df.loc[df['Major Beginning of Semester'] == data2, 'Major Beginning of Semester'] = 'Others'

    return df

    # # change all the other majors(other than science and technology)  to others
    # for data1, data2  in zip(df['Major End of Semester'], df['Major Beginning of Semester']):
    #     if (data1 not in major_list):
    #         # df.ix['Major End of Semester', 'Major End of Semester'] = 'Others'
    #         df.ix[df['Major End of Semester'] == data1, 'Major End of Semester'] = 'Others'
    #
    #     if (data2 not in major_list):
    #         # df.ix[ df['Major Beginning of Semester'] == data2 , 'Major Beginning of Semester'] = 'Others'
    #         # df.loc[df['Major End of Semester'] == data1, 'Major End of Semester'] = 'Others'
    #
    #         df.ix[ df['Major Beginning of Semester'] == data2, 'Major Beginning of Semester'] = 'Others'


    return df

def classify_data(df, semester, howmanymajors):
    writer = pd.ExcelWriter(howmanymajors + '_' + semester + '.xlsx')
    for i, classification in enumerate(classification_list):
        classified_data = df[df['Class'] == classification]
        classified_data.to_excel(writer, classification, index = False)
        writer.save()

def main():

    print(total_data.head())
    print(len(total_data))

    clean_df = cleanup_data(total_data)

    print('Summary of the clean data')
    print(clean_df.head())
    # result = fall_data.groupby(['Major Beginning of Semester']).agg({'Major End of Semester': 'count'}).rename(columns={'Major End of Semester': 'COUNT'}).reset_index()

    classify_data(clean_df, 'BothSemester', 'ScienceTech')
    # classify_data(clean_df2, 'spring' , 'All Major')

if __name__ == "__main__":
    main()
