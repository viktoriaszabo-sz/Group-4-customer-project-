import pandas as pd

# this only works on my laptop so far
file_path = "C:/Users/vikiv/OneDrive - Hämeen ammattikorkeakoulu/learnwell_dataset.xlsx"

# Specify the engine (e.g., 'openpyxl' or 'pyxlsb')
engine = 'openpyxl'

df = pd.read_excel(file_path, engine=engine)


# have to convert the numbers into ints bc they are strings originally for some reason 
string_columns = ['ID',	'Start time','Completion time',	'Email','Name',	'Last modified time',	
                  'Year of birth','Gender','Do you have previous studies or degrees?',	
                  'In which school do you study at HAMK?',	
                  'What is your degree programme in Bioeconomy?',	
                  'What is your degree programme in Wellbeing?',	
                  'What is your degree programme in Entrepreneurship, Business and Technology?',	
                  'What is your degree programme in Professional Teacher Education?',	
                  'Study mode',	'Phase of studies', 
                  'My answers may be used for research purposes and connected with each other and with other study register data.'] # no converting !!!
columns_to_convert = df.columns.difference(string_columns)
df[columns_to_convert] = df[columns_to_convert].astype(float) 

#   "columns_to_convert" contains the columns with the values in it 
bad1_columns = df[['LP101', 'LP103', 'LP107', 'LP109']]
bad2_columns = df[['WB101', 'WB102', 'WB103', 'WB104', 'WB105', 'WB106', 'WB107', 'WB108', 'WB109', 'WB401', 'WB402', 'WB403']]
good_columns = df.drop(columns = df[['ID',	'Start time','Completion time',	'Email','Name',	'Last modified time',	
                                    'Year of birth','Gender','Do you have previous studies or degrees?',	
                                    'In which school do you study at HAMK?',	
                                    'What is your degree programme in Bioeconomy?',	
                                    'What is your degree programme in Wellbeing?',	
                                    'What is your degree programme in Entrepreneurship, Business and Technology?',	
                                    'What is your degree programme in Professional Teacher Education?',	
                                    'Study mode',	'Phase of studies', 
                                    'My answers may be used for research purposes and connected with each other and with other study register data.',
                                    'LP101', 'LP103', 'LP107', 'LP109', 'WB101', 'WB102', 'WB103', 'WB104', 'WB105', 'WB106', 'WB107', 'WB108', 'WB109', 'WB401', 'WB402', 'WB403']])

#df.insert(3, "Sum of good", good_columns.sum(axis=1), allow_duplicates=True) # true = allows duplicates in the column 
#df.insert(4, "Sum of bad", bad_columns.sum(axis=1), allow_duplicates=True) # true = allows duplicates in the column 

# CATEGORIES
learning_category = df[['LP102', 'LP104', 'LP105', 'LP106', 'LP108', 'LP110', 'LP111', 'LP112']]
support_category = df[['LE101', 'LE102', 'LE103', 'LE104', 'LE105', 'LE106', 'LE107', 'LE108', 'LE109', 'LE110', 'LE111', 'LE112', 'LE113', 'LE114', 'LE115', 'LE116', 'LE201', 'LE202', 'LE203', 'LE204', 'LE205', 'LE206', 'LE207', 'LE208', 'LE209', 'LE210', 'LE211', 'LE301', 'LE302', 'LE303', 'LE304', 'LE305', 'LE306']]
competence_category = df[['CD101', 'CD102', 'CD103', 'CD104', 'CD105', 'CD106', 'CD107', 'CD108', 'CD201', 'CD202', 'CD203', 'CD204', 'CD205', 'CD206', 'CD207']]
wellbeing_category = df[['WB101', 'WB102', 'WB103', 'WB104', 'WB105', 'WB106', 'WB107', 'WB108', 'WB109', 'WB201', 'WB202', 'WB203', 'WB204', 'WB205', 'WB206', 'WB207', 'WB301', 'WB302', 'WB303', 'WB304', 'WB305', 'WB401', 'WB402', 'WB403', 'WB404', 'WB405', 'WB406']]
filler_category = df[['PR101', 'PR102', 'PR103', 'CP101', 'CP102', 'CP103', 'EN101', 'SD101', 'SD102', 'CO101', 'CO102', 'DS101', 'DS102', 'DS103', 'IN101', 'IN102', 'PR103']]

#inserting the new columns
badL_sum = bad1_columns.sum(axis=1)
badW_sum = bad2_columns.sum(axis=1)
learning_sum = learning_category.sum(axis= 1) - badL_sum
support_sum = support_category.sum(axis= 1)
competence_sum = competence_category.sum(axis= 1)
wellbeing_sum = wellbeing_category.sum(axis= 1) - badW_sum
filler_sum = filler_category.sum(axis= 1)

new_columns_data = {
    "Sum of learning": learning_sum,
    "Sum of support": support_sum,
    "Sum of competence": competence_sum,
    "Sum of wellbeing": wellbeing_sum,
    "Sum of filler": filler_sum,
}
df = df.assign(**new_columns_data) # puts the new columns to the end of the dataset

# BASIC FUNCTIONALITY OF BACK-END: FOR CATEGORIES AND IF / SWITCH STATEMENTS 
# These are just examples for demonstration

for index, row in df.iterrows():
    sum_of_learning = row['Sum of learning']
    sum_of_support = row['Sum of support']
    sum_of_competence = row['Sum of competence']
    sum_of_wellbeing = row['Sum of wellbeing']
    sum_of_filler = row['Sum of filler']

    # Check learning category sum
    if sum_of_learning <= 60 and sum_of_learning > 40:
        #subcategory 1
        print("Deep approach: ")
    
    elif sum_of_learning <= 40 and sum_of_learning > 20: 
        #subcategory 2
        print("Organized studying: ")

    elif sum_of_learning <= 20:
        #subcategory 3
        print("Surface approach: ")


    # Check support category sum
    if sum_of_support <= 165 and sum_of_support > 110:
        #subcategory 1
        print("Felt supported: ")
    
    elif sum_of_support <= 110 and sum_of_support > 55: 
        #subcategory 2
        print("Felt somewhat supported: ")

    elif sum_of_support <= 55:
        #subcategory 3
        print("Felt unsupported: ")


    # Check competence category sum
    if sum_of_competence <= 75 and sum_of_competence > 50:
        #subcategory 1
        print("Felt competent: ")
    
    elif sum_of_competence <= 50 and sum_of_competence > 25: 
        #subcategory 2
        print("Felt somewhat competent: ")

    elif sum_of_competence <= 25:
        #subcategory 3
        print("Felt incompetent: ")

        

