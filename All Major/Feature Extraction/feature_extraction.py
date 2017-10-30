import numpy as np
import pandas as pd
import os



major_by_class = '/Users/Pankaj/Major-Change-Prediction/All Major/Major by Class.xlsx'
only_fall_data = '/Users/Pankaj/Major-Change-Prediction/All Major/All Major_fall.xlsx'

only_spring_data = '/Users/Pankaj/Major-Change-Prediction/All Major/All Major_spring.xlsx'

xls = pd.ExcelFile(only_fall_data)
fall_FR = xls.parse('FR')
fall_SO = xls.parse('SO')
fall_JR = xls.parse('JR')
fall_SR = xls.parse('SR')

xls_spring = pd.ExcelFile(only_spring_data)
spring_FR = xls_spring.parse('FR')
spring_SO = xls_spring.parse('SO')
spring_JR = xls_spring.parse('JR')
spring_SR = xls_spring.parse('SR')


#parsing the major by class data
major_by_class_data = pd.ExcelFile(major_by_class)
major_by_class_fall2016 = major_by_class_data.parse('Fall 2016')
major_by_class_spring2017 = major_by_class_data.parse('Spring 2017')
major_by_class_spring2017 = major_by_class_spring2017.drop( major_by_class_spring2017[major_by_class_spring2017['Major'] == 'NURS-BSN'].index)


all_majors_total_fall_FR = major_by_class_fall2016[ ['Major' , 'FR Freshman' ] ].sort_values('Major') ['FR Freshman']
all_majors_total_fall_SO = major_by_class_fall2016[ ['Major' , 'SO Sophomore' ] ].sort_values('Major') ['SO Sophomore']

all_majors_total_fall_JR = major_by_class_fall2016[ ['Major' , 'JR Junior' ] ].sort_values('Major')['JR Junior']

all_majors_total_fall_SR = major_by_class_fall2016[ ['Major' , 'SR Senior' ] ].sort_values('Major') ['SR Senior']


all_majors_total_spring_FR = major_by_class_spring2017[ ['Major' , 'FR Freshman' ] ].sort_values('Major') ['FR Freshman']
all_majors_total_spring_SO = major_by_class_spring2017[ ['Major' , 'SO Sophomore' ] ].sort_values('Major') ['SO Sophomore']

all_majors_total_spring_JR = major_by_class_spring2017[ ['Major' , 'JR Junior' ] ].sort_values('Major') ['JR Junior']

all_majors_total_spring_SR = major_by_class_spring2017[ ['Major' , 'SR Senior' ] ].sort_values('Major') ['SR Senior']


#sciene_and_technology = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS', 'Others']
sciene_and_technology_division = ['BIOL-BS', 'CHEM-BS', 'CS-BS' , 'IT-BS',  'MATH-BS', 'PHYS-BS']

all_majors = major_by_class_fall2016['Major'].unique()

print(len(all_majors))

# another approach of finding the all majors
fall_FR = xls.parse('FR')
fall_SO = xls.parse('SO')
fall_JR = xls.parse('JR')
fall_SR = xls.parse('SR')

spring_FR = xls_spring.parse('FR')
spring_SO = xls_spring.parse('SO')
spring_JR = xls_spring.parse('JR')
spring_SR = xls_spring.parse('SR')

data_to_find_majors = [fall_FR, fall_SO, fall_JR, fall_SR, spring_FR, spring_SO, spring_JR, spring_SR]

#updating the all majors to be the actual data
# need to check if it is unique or not
all_majors_begin = set([item for sublist in data_to_find_majors for item in sublist['Major Beginning of Semester']])

all_majors_end = set([item for sublist in data_to_find_majors for item in sublist['Major End of Semester']])


#all_majors = set(list(all_majors_begin) +  list(all_majors_end))
#print(len(all_majors))

#
# all_majors_check = []
# for data in data_to_find_majors:
#     # A = reduce(lambda x, y: x + y, l)
#     # B = sum(l, [])
#     # C = [item for sublist in l for item in sublist]
#
#     all_majors_check.append(data['Major Beginning of Semester'])
#     all_majors_check.append(data['Major End of Semester'])
#     print(len(all_majors_check))




#divided_majors = np.array([ [major+ 'Higher' , major + 'Lower']  for major in all_majors]).ravel()

total_freshman_fall = 3626
total_freshman_spring = 2627

total_sophomore_fall = 2131
total_sophomore_spring = 2001

total_junior_fall = 2019
total_junior_spring = 1980

total_senior_fall = 3087
total_senior_spring = 3060

sciene_and_technology_total_students_enrolled_fall_freshman = [330, 44, 135, 55, 13, 25, 3024]
sciene_and_technology_total_students_enrolled_sprint_freshman = [233, 25, 97, 43, 5, 16, 2208]

sciene_and_technology_total_students_enrolled_fall_sophomore = [162, 22, 54, 39, 8, 8, 1838]
sciene_and_technology_total_students_enrolled_spring_sophomore = [143, 15, 50, 40, 11, 12, 1730]


sciene_and_technology_total_students_enrolled_fall_junior = [124, 16, 48, 40, 11, 6, 1774]
sciene_and_technology_total_students_enrolled_spring_junior = [119, 14, 49, 48, 10, 6, 1734]


sciene_and_technology_total_students_enrolled_fall_senior = [155, 24, 84, 70, 23, 10, 2721]
sciene_and_technology_total_students_enrolled_spring_senior = [156, 24, 87, 69, 22, 10, 3060]



all_students_total_students_enrolled_fall_freshman = []


classification_list = ['FR', 'SO', 'JR', 'SR']

# Initialize probability matrix and number matrix
matrix_size = len(all_majors)
probability_matrix = np.zeros((matrix_size,matrix_size))
number_matrix = np.zeros((matrix_size,matrix_size))

probability_matrix_success = np.zeros((matrix_size,matrix_size))
number_matrix_success = np.zeros((matrix_size,matrix_size))

all_good_beginning_major = []
all_good_ending_major = []

def select_best_majors(semester, classification):
    path_to_get = '/Users/Pankaj/Major-Change-Prediction/All Major/Feature Extraction/' + semester + '/' + classification

    xls = pd.ExcelFile(path_to_get + '/GoodMajor.xlsx')
    beginning_major  = xls.parse('GoodMajorBeginning')
    ending_major  = xls.parse('GoodMajorEnd')

    all_good_beginning_major.append(beginning_major)
    all_good_ending_major.append(ending_major)

def find_intersection_majors(all_good_beginning_major, all_good_ending_major):
    intersection_beginning = []
    intersection_ending = []
    for index, good_major_df in enumerate(all_good_beginning_major):
        if(index < len(all_good_beginning_major) - 2):
            intersection_beginning  = pd.merge(good_major_df, all_good_beginning_major[index +1], how='inner', on=['col'])

    for index, good_major_df in enumerate(all_good_ending_major):
        if(index < len(all_good_beginning_major) - 2):
            intersection_ending = pd.merge(good_major_df, all_good_ending_major[index + 1], how='inner', on=['col'])

    print(intersection_beginning, 'Beginning')
    print(intersection_ending, 'Ending')

    total_good_majors = pd.concat([intersection_ending, intersection_beginning])

    total_filtered_good_majors = total_good_majors['col'].unique()

    print(total_filtered_good_majors)
    np.savetxt('FilteredGoodMajors.txt', np.array(total_filtered_good_majors), delimiter=" ", fmt="%s")



def save_good_majors(data, semester, classification):

    df_begining =  data['Major Beginning of Semester'].value_counts().reset_index()
    df_end = data['Major End of Semester'].value_counts().reset_index()
    df_begining.columns = ['col', 'count']
    df_end.columns = ['col', 'count']

    path_to_save = '/Users/Pankaj/Major-Change-Prediction/All Major/Feature Extraction/' + semester + '/' + classification

    try:
        os.makedirs(path_to_save)
    except OSError:
        if not os.path.isdir(path_to_save):
            raise

    writer = pd.ExcelWriter( os.path.join(path_to_save ,  'GoodMajor.xlsx'))

    # writer = pd.ExcelWriter(howmanymajors + '_' + semester + '.xlsx')
    # for i, classification in enumerate(classification_list):
    #     classified_data = df[df['Class'] == classification]
    #     classified_data.to_excel(writer, classification)
    #     writer.save()

    # for i, classification in enumerate(classification_list):
    #     classified_data = df[df['Class'] == classification]
    #     classified_data.to_excel(writer,  )
    #     writer.save()
    # np.savetxt( os.path.join(path_to_save, 'GoodMajorBeginning.txt'), df_begining[0])
    # np.savetxt( os.path.join(path_to_save, 'GoodMajorEnd.txt') , df_end)
    # np.savetxt(os.path.join(path_to_save, 'TransitionProbabilityMatrix.txt'), pm[0])

    #print(df_begining)
    # only select the top 25 major
    df_begining[0: 10].to_excel(writer,  'GoodMajorBeginning')
    df_end[0: 10].to_excel(writer, 'GoodMajorEnd')
    writer.save()


def main(classification, semester):

    # Initialize data to be freshman fall semester data
    # Initialize total to fall freshman
    data = fall_FR
    total = all_majors_total_fall_FR

    # Conditions to set the right data and total
    if(classification == 'FR' and semester == 'Fall'):
        data = fall_FR
        total = all_majors_total_fall_FR
    elif (classification == 'SO' and semester == 'Fall'):
        data = fall_SO
        total = all_majors_total_fall_SO
    elif (classification == 'JR' and semester == 'Fall'):
        data = fall_JR
        total = all_majors_total_fall_JR
    elif (classification == 'SR' and semester == 'Fall'):
        data = fall_SR
        total = all_majors_total_fall_SR
    elif (classification == 'FR' and semester == 'Spring'):
        data = spring_FR
        total = all_majors_total_spring_FR
    elif (classification == 'SO' and semester == 'Spring'):
        data = spring_SO
        total = all_majors_total_spring_SO
    elif (classification == 'JR' and semester == 'Spring'):
        data = spring_JR
        total = all_majors_total_spring_JR
    elif (classification == 'SR' and semester == 'Spring'):
        data = spring_SR
        total = all_majors_total_spring_SR

    # create probability matrix

    save_good_majors(data, semester, classification)


if __name__ == "__main__":

    #this loop runs 8 times ( 4 classificaiton (FR, SO, JR, SR) * 2 semester (Fall , Spring))
    for classification in classification_list:
        for semester in ['Spring', 'Fall']:
            main(classification, semester)

    for classification in classification_list:
        for semester in ['Spring', 'Fall']:
            select_best_majors(semester, classification)

    find_intersection_majors(all_good_beginning_major, all_good_ending_major)





