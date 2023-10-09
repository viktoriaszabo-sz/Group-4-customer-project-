import pandas as pd
import math
from flask import Flask, render_template, request, redirect, url_for, session
# run this code into powershell: pip install Flask 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'
file_path = "./project/learnwell_dataset.xlsx"
engine = "openpyxl"
df = pd.read_excel(file_path, engine=engine, sheet_name='Form1')

# have to convert the numbers into ints bc they are strings originally for some reason 
string_columns = ['ID', 'Start time', 'Completion time', 'Email', 'Name', 'Last modified time',	
                  'Year of birth','Gender', 'Do you have previous studies or degrees?',	
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

# initiate the variables value with empty strings
html_user_email=""
user_email=""
category_message1 = ""
category_message2 = ""
category_message3 = ""
category_message4 = ""
category_message5 = ""
category_message6 = ""
category_message7 = ""
category_message8 = ""

@app.route('/')
def index():

    return render_template('0.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    # Get the user's email address from the form
    global user_email 
    user_email = request.form.get('email')
    # Store the email in the session
    session['user_email'] = user_email
    # Process the email address if needed
    user_data = df[df['Email'] == user_email]
    # Redirect the user to 'welcome'
    return redirect(url_for('welcome', user_email=user_email))

# The welcome page
@app.route('/welcome')
def welcome():

    return render_template('welcome.html')

# Category 1
@app.route('/page1')
def page1():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None
            
# 1. LEARNING
            sum_of_learning = user_data['Sum of learning'].values[0]
            # Check LEARNING category sum and decide the feedback outcome
            if sum_of_learning <= 60 and sum_of_learning > 40:
                category_message1 = "1a1"
            elif sum_of_learning <= 40 and sum_of_learning > 20:
                category_message1 = "1a2"
            elif sum_of_learning <= 20:
                category_message1 = "1a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('1.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 1
                chart_1 = chart_1,
                # the output of the category
                category_message1 = category_message1
                )

# Category 2
@app.route('/page2')
def page2():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 2. SUPPORT
            sum_of_support = user_data['Sum of support'].values[0]
            # Check SUPPORT category sum and decide the feedback outcome
            if sum_of_support <= 165 and sum_of_support > 110:
                category_message2 = "2a1"
            elif sum_of_support <= 110 and sum_of_support > 55:
                category_message2 = "2a2" 
            elif sum_of_support <= 55:
                category_message2 = "2a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('2.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 2
                chart_2 = chart_2,
                # the output of the category
                category_message2 = category_message2,
                )

# Category 3

@app.route('/page3')
def page3():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 3. COMPETENCE
            sum_of_competence = user_data['Sum of competence'].values[0]
            # Check COMPETENCE category sum and decide the feedback outcome
            if sum_of_competence <= 75 and sum_of_competence > 50:
                category_message3 = "3a1"
            elif sum_of_competence <= 50 and sum_of_competence > 25: 
                category_message3 = "3a2"
            elif sum_of_competence <= 25:
                category_message3 = "3a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('3.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 3
                chart_3 = chart_3,
                # the output of the category
                category_message3 = category_message3
                )

# Category 4

@app.route('/page4')
def page4():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 4. FILLER
            sum_of_filler = user_data['Sum of filler'].values[0]
            # Check FILLER category sum and decide the feedback outcome
            if sum_of_filler <= 85 and sum_of_filler > 57:
                category_message4 = "4a1"
            elif sum_of_filler <= 57 and sum_of_filler > 29: 
                category_message4 = "4a2"
            elif sum_of_filler <= 29 or sum_of_filler == 0:
                category_message4 = "4a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('4.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 4
                chart_4 = chart_4,
                # the output of the category
                category_message4 = category_message4
                )

# Category 5

@app.route('/page5')
def page5():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 5. WELLBEING - SUBCATEGORY 1 = SELF-EFFICIANCY
            sum_of_se = user_data['Sum of self-efficacy'].values[0]  
            # Check SELF-EFFICIANCY sum and decide the feedback outcome
            if sum_of_se <= 35 and sum_of_se > 24:
                category_message5 = "5a1"
            elif sum_of_se <= 24 and sum_of_se > 13: 
                category_message5 = "5a2"
            elif sum_of_se <= 13:
                category_message5 = "5a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('5.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 5
                chart_5 = chart_5,
                # the output of the category
                category_message5 = category_message5,
                )

# Category 6

@app.route('/page6')
def page6():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None
            
# 6. WELLBEING - SUBCATEGORY 2 = 
            sum_of_psych = user_data['Sum of psychological flexibility'].values[0]
            # Check for PSYCHOLOGICAL FLEXIBILITY sum and decide the feedback outcome 
            if sum_of_psych <= 35 and sum_of_psych > 24:
                category_message6 = "6a1"
            elif sum_of_psych <= 24 and sum_of_psych > 13: 
                category_message6 = "6a2"
            elif sum_of_psych <= 13:
                category_message6 = "6a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('6.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 6
                chart_6 = chart_6,
                # the output of the category
                category_message6 = category_message6, 
                )

# Category 7
@app.route('/page7')
def page7():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 7. WELLBEING - SUBCATEGORY 3 = BURN OUT
            # Check for BURN OUT sum and decide the feedback outcome
            sum_of_burnout = user_data['Sum of burnout'].values[0]
            if sum_of_burnout <= 45 and sum_of_burnout > 30:
                category_message7 = "7a1"
            elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
                category_message7 = "7a2"
            elif sum_of_burnout <= 15:
                category_message7 = "7a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('7.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # sum of burn out for page 7
                sum_of_burnout = sum_of_burnout,
                # the output of the category
                category_message7 = category_message7
                )

# Category 8
@app.route('/page8')
def page8():
# 0 STARTING GLOBAL SETTINGS
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')
    # prepare the path to overviewResponse
    overviewResponse_url = f'/static/1.overviewResponse/'
    # prepare the path to personalizedResponse
    personalizedResponse_url = f'/static/2.personalizedResponse/'
    # check for existence of user email
    if user_email:
        # no global variable needed
        # email not found message
        emailNotFound = None
        # user data to retrieve the row (1st row found)
        user_data = df[df['Email'] == user_email]
        # retrieve the language preselected by user when giving survey
        lang_preselect = user_data['lang'].values[0]
        # retrieve the user Name for greeting
        user_name = user_data['Name'].values[0]
        # check for existence of user data
        if not user_data.empty:
        # data not found message
            dataNotFound = None

# 8. WELLBEING - SUBCATEGORY 4 = SELF-REFLECTION / SELF-COMPASSION
            # Check SELF-REFLECTION / SELF-COMPASSION sum and decide the feedback outcome
            sum_of_sr = user_data['Sum of self-reflection'].values[0]
            if sum_of_sr <= 5 and sum_of_sr > 0:
                category_message8 = "8a1"
            elif sum_of_sr == 0:
                category_message8 = "8a2"
            elif math.isnan(sum_of_sr):
                category_message8 = "8a3"

# -1 FINISHING GLOBAL SETTINGS
        # closing of "if not user_data.empty"
        else:
            dataNotFound = "User data not found."
    # closing of "if user_email"     
    else: 
        emailNotFound = "User email not found."

    return render_template('8.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound,
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                personalizedResponse_url=personalizedResponse_url,
                overviewResponse_url = overviewResponse_url,
                # Chart variable for page 8
                chart_ = chart_,
                # the output of the category
                category_message8 = category_message8
                )

# app running
if __name__ == '__main__': 
    app.run(debug=True)