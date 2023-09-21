import pandas as pd

file_path = "C:/Users/vikiv/OneDrive - Hämeen ammattikorkeakoulu/learnwell_dataset.xlsx"
engine = "openpyxl"
df = pd.read_excel(file_path, engine=engine, sheet_name='Form1')

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
df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')



# ------------------    CATEGORIES AND SUMS - WE FILTER THE GOOD AND BAD QUESTIONS IN THIS SECTION --------------------------------------------

learning_all_sum = df[['LP101', 'LP102', 'LP103', 'LP104', 'LP105', 'LP106', 'LP107', 'LP108', 'LP109', 'LP110', 'LP11', 'LP12']].sum(axis=1)
badL_sum = df[['LP101', 'LP103', 'LP107', 'LP109']].sum(axis=1)
learning_sum = learning_all_sum - badL_sum    # bc this has the "bad" questions in them
support_sum= df[['LE101', 'LE102', 'LE103', 'LE104', 'LE105', 'LE106', 'LE107', 'LE108', 'LE109', 'LE110', 'LE111', 'LE112', 'LE113', 'LE114', 'LE115', 'LE116', 'LE201', 'LE202', 'LE203', 'LE204', 'LE205', 'LE206', 'LE207', 'LE208', 'LE209', 'LE210', 'LE211', 'LE301', 'LE302', 'LE303', 'LE304', 'LE305', 'LE306']].sum(axis=1)
competence_sum = df[['CD101', 'CD102', 'CD103', 'CD104', 'CD105', 'CD106', 'CD107', 'CD108', 'CD201', 'CD202', 'CD203', 'CD204', 'CD205', 'CD206', 'CD207']].sum(axis=1)
filler_sum = df[['PR101', 'PR102', 'PR103', 'CP101', 'CP102', 'CP103', 'CP104', 'EN101', 'SD101', 'SD102', 'CO101', 'CO102', 'DS101', 'DS102', 'DS103', 'IN101', 'IN102']].sum(axis=1)


#WELLBEING IS DEVIDED INTO 4 SUBCATEGORIES ==> self-efficiancy, psychological flexibility, burnout, self-reflection (probably will be needed for visualizations)

wb_self_efficiancy_sum = df[['WB201', 'WB202', 'WB206', 'WB301', 'WB302', 'WB303', 'WB305']].sum(axis=1)
#this doesnt have bad columns
wb_burnout_sum = df[['WB101', 'WB104', 'WB107', 'WB105', 'WB106', 'WB108', 'WB103', 'WB402']].sum(axis=1)
#this has ONLY BAD columns (exhaustion (101, 104, 107), cynicism (105, 106, 108), inadequacy (103, 402))

wb_psych_all_sum = df[['WB203', 'WB204', 'WB205', 'WB207', 'WB404', 'WB405', 'WB406', 'WB109', 'WB401', 'WB403']].sum(axis=1)
wb_psych_bad_sum = df[['WB109', 'WB401', 'WB403']].sum(axis=1)
wb_psychological_sum = wb_psych_all_sum - wb_psych_bad_sum
#this had good and bad columns, created a sum for this case too 

wb_sc_bad_sum = df['WB304']
wb_sc_good_sum = df['WB102']
wb_sc_sum = wb_sc_good_sum - wb_sc_bad_sum
wb_sc_sum_filled = wb_sc_sum.fillna(0) #it will gives us the actual negative result 
#this could be a negative score too bc theres only 1 good and 1 bad question


#------------------------------- WE INSERT THE NEW SUM COLUMNS INTO THE DATASET --------------------------------
new_columns_data={
    "Sum of learning": learning_sum,
    "Sum of support": support_sum,
    "Sum of competence": competence_sum,
    "Sum of filler": filler_sum,
    "Sum of self-efficacy": wb_self_efficiancy_sum, 
    "Sum of psychological flexibility": wb_psychological_sum,
    "Sum of burnout": wb_burnout_sum, 
    "Sum of self-reflection": wb_sc_sum 
}
df = df.assign(**new_columns_data) # puts the new columns to the end of the dataset