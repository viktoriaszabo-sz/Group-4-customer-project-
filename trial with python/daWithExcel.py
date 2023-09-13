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
bad_columns = df[['LP101', 'LP103', 'LP107', 'LP109', 'WB101', 'WB102', 'WB103', 'WB104', 'WB105', 'WB106', 'WB107', 'WB108', 'WB109', 'WB401', 'WB402', 'WB403']]
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

#inserting the 2 new columns
good_sum = good_columns.sum(axis= 1)
bad_sum = bad_columns.sum(axis=1)

new_columns_data = {
    "Sum of good": good_sum, 
    "Sum of bad": bad_sum
}
df = df.assign(**new_columns_data) # puts the new columns to the end of the dataset 

# BASIC FUNCTIONALITY OF BACK-END: FOR CATEGORIES AND IF / SWITCH STATEMENTS 
# these are just examples for demonstration

for index, row in df.iterrows():
    sum_of_good = row['Sum of good']
    sum_of_bad = row['Sum of bad']
    
    # Check if "Sum of good" is less than 300
    if sum_of_good < 270 and sum_of_good > 250 and sum_of_bad < 50:
        #category 1
        print(f"Row {index + 1}: Good is between 260 and 270 and Bad is less then 50")
    
    if sum_of_good > 270 and sum_of_bad > 50: 
        #category 2
        print(f"Row {index + 1}: Good is more then 270 and bad is more than 50 ")
    # now our dataset contains the two neccessary sum columns 