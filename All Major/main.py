import numpy as np
import pandas as pd
from pandas import ExcelWriter


df = pd.read_csv('Majors Changed.csv', index_col=None)



data_vales = df.values

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


sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS']


sciene_and_technology_data = df[
    (df['Major Beginning of Semester'] == 'BIOL-BS') | (df['Major Beginning of Semester'] == 'CS-BS') |
    (df['Major Beginning of Semester'] == 'CHEM-BS') | (df['Major Beginning of Semester'] == 'IT-BS') |
    (df['Major Beginning of Semester'] == 'MATH-BS') | (df['Major Beginning of Semester'] == 'PHYS-BS')
    ]

sciene_and_technology_data.to_csv('Science&TechnologyData.csv', sep='\t', encoding='utf-8', index = False)



writer = ExcelWriter('Science&TechnologyData.xlsx')
sciene_and_technology_data.to_excel(writer,'Sheet5', index = False)
writer.save()



    # | (df['Major Beginning of Semester'] == 'CHEM-BS') |
    # (df['Major Beginning of Semester'] == 'CS-BS') | (df['Major Beginning of Semester'] == 'IT-BS') |
    # (df['Major Beginning of Semester'] == 'MATH-BS') | (df['Major Beginning of Semester'] == 'PHYS-BS')
    #
    #     ]


#check = np.where(data['Major Beginning of Semester'] == 'BIOL-BS' or data['Major Beginning of Semester'] == 'CHEM-BS' )

# sciene_and_technology_data = data[
#
#                                   data['Major Beginning of Semester'] == 'BIOL-BS',
#                                   data['Major Beginning of Semester'] == 'CHEM-BS'
#                                   # data['Major Beginning of Semester'] == 'CS-BS'or
#                                   # data['Major Beginning of Semester'] == 'IT-BS' or
#                                   # data['Major Beginning of Semester'] == 'MATH-BS' or
#                                   # data['Major Beginning of Semester'] == 'PHYS-BS')
#                                 ]

print(sciene_and_technology_data.head())

print(df.describe())

data_major_beginningOfSemester = sciene_and_technology_data.groupby('Major Beginning of Semester')

# print(data_major_beginningOfSemester.head())
# print('some gap please')
# print(data_major_beginningOfSemester.count())



