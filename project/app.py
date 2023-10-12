import pandas as pd
import math
from flask import Flask, render_template, request, redirect, url_for, session
# run this code into powershell: pip install Flask 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'
file_path = "C:/Users/vikiv/OneDrive - Hämeen ammattikorkeakoulu/learnwell_dataset.xlsx"
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

wb_sc_bad_sum = df[['WB304']].sum(axis=1)
wb_sc_good_sum = df[['WB102']].sum(axis=1)
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


# counting the average of all users for the welcome.html chart
rows = len(df)
    # Learning avg
learningavgsum = learning_sum
cells = rows * 12 # vai 16??
learning_avg_all = learningavgsum.sum() / cells
learning_avg_all

# Support avg
supportavgsum = support_sum
cells = rows * 33
support_avg_all = supportavgsum.sum() / cells
support_avg_all

# Competence avg
competenceavgsum = competence_sum
cells = rows * 15
competence_avg_all = competenceavgsum.sum() / cells
competence_avg_all

# Filler avg
filleravgsum = filler_sum
cells = rows * 17
filler_avg_all = filleravgsum.sum() / cells
filler_avg_all

# Wb self efficiancy avg
wb_self_efficiancyavgsum = wb_self_efficiancy_sum
cells = rows * 7
wb_self_efficiancy_avg_all = wb_self_efficiancyavgsum.sum() / cells
wb_self_efficiancy_avg_all

# Wb psychological avg
wb_psychological_avgsum = wb_psychological_sum
cells = rows * 7 #vai 10?
wb_psychological_avg_all = wb_psychological_avgsum.sum() / cells
wb_psychological_avg_all

# Wb burnout avg
wb_burnout_avgsum = wb_burnout_sum
cells = rows * 8
wb_burnout_avg_all = wb_burnout_avgsum.sum() / cells
wb_burnout_avg_all

# Wb sc avg
wb_sc_avgsum = wb_sc_sum
wb_sc_avgsum
cells = rows * 1
wb_sc_avg = wb_sc_avgsum.sum() / cells
wb_sc_avg_all = str(round(wb_sc_avg, 2))
wb_sc_avg_all


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
    global user_data
    user_email = request.form.get('email')  #user email address after form validation in 0.html
    session['user_email'] = user_email          # Store the email in the session
    user_data = df[df['Email'] == user_email]  # Process the email address if needed
        
    if user_data.empty:   # checks if the email address is in the dataset
        print("Invalid email address. It seems like your data is not accessible from our database")
        return redirect('/')  # Redirect the user back to the form
    else: 
        return redirect(url_for('welcome', user_email=user_email))  # Redirect the user to 'welcome'

# The welcome page
@app.route('/welcome')
def welcome():
 # Process the email address if needed
    user_data = df[df['Email'] == user_email]
    rows = len(df)
    #1
    sum_of_learning = user_data['Sum of learning'].values[0]
    learning_percent = 5 * (sum_of_learning / 60)
    #all average
    learningavg_all_sum = ['LP101', 'LP102', 'LP103', 'LP104', 'LP105', 'LP106', 'LP107', 'LP108', 'LP109', 'LP110', 'LP11', 'LP12']
    badavgL_sum = ['LP101', 'LP103', 'LP107', 'LP109']
    learning_avg_sum = row_sums = df[learningavg_all_sum].sum(axis=1) - df[badavgL_sum].sum(axis=1)
    cells = rows *12
    learning_avg = learning_avg_sum / cells
    #2
    sum_of_support = user_data['Sum of support'].values[0]
    #avg
    supportavgsum = ['LE101', 'LE102', 'LE103', 'LE104', 'LE105', 'LE106', 'LE107', 'LE108', 'LE109', 'LE110', 'LE111', 'LE112', 'LE113', 'LE114', 'LE115', 'LE116', 'LE201', 'LE202', 'LE203', 'LE204', 'LE205', 'LE206', 'LE207', 'LE208', 'LE209', 'LE210', 'LE211', 'LE301', 'LE302', 'LE303', 'LE304', 'LE305', 'LE306']
    #supportavgsum
    rows = len(df)
    # rows
    # Sum the desired columns row-wise
    row_sums = df[supportavgsum].sum(axis=1)
    #row_sums
    cells = rows *33
    lp_sum_avg = row_sums.sum() / cells
    #sp_avg = row_sums.sum() / cells
    support_percent = 5 * (sum_of_support / 165)
    #3
    sum_of_competence = user_data['Sum of competence'].values[0]
    competence_percent = 5 * (sum_of_competence / 75)
    #4
    sum_of_filler = user_data['Sum of filler'].values[0]
    filler_percent = 5 * (sum_of_filler / 85) 
    #5
    sum_of_se = user_data['Sum of self-efficacy'].values[0]
    self_ef_percent = 5 * (sum_of_se / 35)
    #6
    sum_of_psych = user_data['Sum of psychological flexibility'].values[0]
    psy_flex_percent = 5 * (sum_of_psych / 35)
    #7
    sum_of_burnout = user_data['Sum of burnout'].values[0]
    burnoutpercent = 5 * (sum_of_burnout / 45)
    #8
    sum_of_sr = user_data['Sum of self-reflection'].values[0]
    selfrefpercent = 5 * (sum_of_sr / 5)

    return render_template('welcome.html', learning_avg_all=learning_avg_all, support_avg_all=support_avg_all, competence_avg_all=competence_avg_all, filler_avg_all=filler_avg_all, wb_self_efficiancy_avg_all=wb_self_efficiancy_avg_all, wb_psychological_avg_all=wb_psychological_avg_all, wb_burnout_avg_all=wb_burnout_avg_all, wb_sc_avg_all=wb_sc_avg_all, learningpercent = learning_percent, \
                           supportpercent = support_percent, competencepercent = competence_percent, \
                            fillerpercent = filler_percent, self_ef_percent = self_ef_percent, psy_flex_percent = psy_flex_percent, \
                                burnoutpercent = burnoutpercent, selfrefpercent = selfrefpercent, lp_sum_avg = lp_sum_avg, \
                                    learning_avg = learning_avg)

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
                # Chart variable for page 1
                # chart_1 = chart_1,
                # the output of the category
                category_message1 = category_message1, sum_of_learning = sum_of_learning
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

    return render_template('2.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound, sum_of_support = sum_of_support, 
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                # Chart variable for page 2
                # chart_2 = chart_2,
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

    return render_template('3.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound, sum_of_competence = sum_of_competence, 
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                # Chart variable for page 3
                # chart_3 = chart_3,
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
                # Chart variable for page 4
                # chart_4 = chart_4,
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

    return render_template('5.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound, sum_of_se = sum_of_se, 
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                # Chart variable for page 5
                # chart_5 = chart_5,
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

    return render_template('6.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound, sum_of_psych = sum_of_psych, 
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                # Chart variable for page 6
                # chart_6 = chart_6,
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

    return render_template('8.html', emailNotFound = emailNotFound, dataNotFound = dataNotFound, sum_of_sr = sum_of_sr, 
                # user name
                user_name=user_name,
                # path to the personalizedResponse which stores feedback paragraphs
                # Chart variable for page 8
                # chart_ = # chart_,
                # the output of the category
                category_message8 = category_message8
                )

# Load the Excel file into a DataFrame
text_file_path = './project/paragraph.xlsx'
paragraph = pd.read_excel(text_file_path)

@app.route('/get_content/<id>')
def get_content(id):
    content_row = paragraph[paragraph['ID'] == id]
    if content_row.empty:
        return jsonify({'content': ''})

    content = content_row['Content'].values[0]
    return jsonify({'content': content})


# app running
if __name__ == '__main__': 
    app.run(debug=True)