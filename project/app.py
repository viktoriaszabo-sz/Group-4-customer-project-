import pandas as pd
import math
import re
from flask import Flask, render_template, request, redirect, url_for, session
# run this code into powershell: pip install Flask 

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'
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

@app.route('/index')
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
        return redirect(url_for('index'))  # Redirect the user back to the form
    else: 
        return redirect(url_for('welcome', user_email=user_email))  # Redirect the user to 'welcome'

@app.route('/welcome')
def welcome():

    return render_template('welcome.html')

@app.route('/page1')
def page_1():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message1
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_learning = user_data['Sum of learning'].values[0]
            # Define the category_message1 based on sum_of_learning
            if sum_of_learning <= 60 and sum_of_learning > 40:
                category_message1 = "Deep approach: You take a deep approach to learning, meaning that you aim to understand what you have learned in a deeper level, and you try to find connections, as well as find underlying meanings. You find yourself motivated to learn and often have the appropriate background knowledge to connect the new information with the old. "  # <-- this is for the connection 
            elif sum_of_learning <= 40 and sum_of_learning > 20: 
                category_message1 = "Organized studying: Your studying is organized. You might not necessarily take a deep approach to learning, but you are more organized than someone who takes on a surface approach. You have the tools to shift to deeper understanding if you want to learn to understand and focus on the meaning, but you can also find yourself easily just repeating the learned information without deeper understanding. "
            elif sum_of_learning <= 20:
                category_message1 = "Surface approach: You take a surface approach to learning, meaning your learning aims for repetition. This approach is not reflective and studying might often be done in the last minute. This results in fragmented understanding and things you memorized are often forgotten. Typically, you are not interested in understanding and just want to learn what is required. "
        else:
            category_message1 = "User data not found."
    else: 
        category_message1 = "User email not found."

    return render_template('1.html', category_message1=category_message1)

@app.route('/page2')
def page_2():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message2
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_support = user_data['Sum of support'].values[0]
            # Check SUPPORT category sum
            if sum_of_support <= 165 and sum_of_support > 110:
                category_message2 = "You feel supported in your studies. Your learning environment supports your learning, and you can work well with other students. You get feedback that is accurate, and you feel like guidance is available whenever you need it. "
            elif sum_of_support <= 110 and sum_of_support > 55: 
                category_message2 = "You feel somewhat supported. Your learning environment somewhat does its job at supporting you, but it might feel a bit lacking. You get along with other students when it comes to working and studying, if need be, but it does not always feel too fulfilling. "
            elif sum_of_support <= 55:
                category_message2 = "You feel like you do not get enough support and the learning environment does not support you the way it should. Maybe it is the lack of feedback or guidance, or you do not feel comfortable working with other students. Whichever the case, try to bring this topic up to someone that might help you feel more supported, such as a teacher or student counsellor. "
        else:
            category_message2 = "User data not found."
    else: 
        category_message2 = "User email not found."

    return render_template('2.html', category_message2 = category_message2)

@app.route('/page3')
def page_3():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message3
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_competence = user_data['Sum of competence'].values[0]
            # Check COMPETENCE category sum
            if sum_of_competence <= 75 and sum_of_competence > 50:
                category_message3 = "You feel competent in your studies. You feel like you have learned and improved on skills that are useful and you know how to use the learned knowledge to your advantage. This helps you to know your strengths and weaknesses and makes you more confident in your abilities. "
            elif sum_of_competence <= 50 and sum_of_competence > 25: 
                category_message3 = "You feel somewhat competent when it comes to your studies, but you still have doubts about your skills. You could potentially work and know what you are doing, at least for the most part, but you might feel unsure if you are doing things correctly. Try and ask when it comes to it, maybe you are doing things right and it is about trusting yourself, or maybe you feel like you need more information. Either way, asking is a good way to start gaining that knowledge and confidence. "
            elif sum_of_competence <= 25:
                category_message3 = "You do not feel competent in your studies, and you lack knowledge that would help you feel confident in your field. You feel like you do not have the required knowledge to be able to work effectively and you struggle to work in a group. Try to go over the basics of the subject you feel incompetent in and work your way up at your own pace. When you learn the basics and have acquired and understood it, it is easier for you to trust in your abilities and continue building up that knowledge. Do not be afraid to ask for help either. Asking help, especially from your fellow students, helps you gain those social skills that are needed in working as a group, as well as give you more of that needed knowledge. "
        else:
            category_message3 = "User data not found."
    else: 
        category_message3 = "User email not found."

    return render_template('3.html', category_message3 = category_message3)

@app.route('/page4')
def page_4():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message4
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_filler = user_data['Sum of filler'].values[0]
            #check FILLER category sum 
            if sum_of_filler <= 85 and sum_of_filler > 57:
                category_message4 = "You have clear objectives for the future. You use the resources that are given to you and always try to max out your opportunities, whether it is about international interactions or work placement. Maybe you even feel enthusiastic for entrepreneurship. "
            elif sum_of_filler <= 57 and sum_of_filler > 29: 
                category_message4 = "You recognize the options given to you and work with them but might lack the possibility to use them to your own advantage. Try interacting more with foreigners or dig up some articles about the work placement advice provided by the university. You could also think about some entrepreneurial tendencies that you might have. "
            elif sum_of_filler <= 29 or sum_of_filler == 0:
                category_message4 = "Your objectives for the future are not clear. You might feel like you can not properly use the resources that are given to you or might not even feel like there is anything to begin with. Try reaching out to your guidance counsellor or talk to peers in higher years to get some information regarding work placement, international opportunities or sustainability. "
        else:
            category_message4 = "User data not found."
    else: 
        category_message4 = "User email not found."

    return render_template('4.html', category_message4 = category_message4)

@app.route('/page5')
def page_5():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message5
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_se = user_data['Sum of self-efficacy'].values[0]

            #CHECK FOR WELLBEING - SUBCATEGORIES 
            #check for SELF-EFFICIANCY sum 
            if sum_of_se <= 35 and sum_of_se > 24:
                category_message5 = "Your self-efficacy is good – You trust in yourself and your capabilities, which makes you an efficient learner as well. You persist working towards your future and will not let anything stand in your way. "
            elif sum_of_se <= 24 and sum_of_se > 13: 
                category_message5 = "Your self-efficacy is okay – You recognize your capabilities but will not trust them to their full extent; you might be a hard-worker, but the lack of self-trust prevents you from reaching your full potential. Seek more opportunities for engaging in learning activities. "
            elif sum_of_se <= 13:
                category_message5 = "Your self-efficacy is lacking – You do not necessarily trust your capabilities, which might cause you not putting enough effort in your studies and avoiding tasks or assignments. Recognize your previous achievements, so that you can be more persistent in your studies. Also, try reaching out to other students with a similar situation, so you could feel more seen and heard. Maybe you will get more motivation, as well as see your worth when other students are there to help you. "
        else:
            category_message5 = "User data not found."
    else: 
        category_message5 = "User email not found."     
    
    return render_template('5.html', category_message5 = category_message5)

@app.route('/page6')
def page_6():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message6
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_psych = user_data['Sum of psychological flexibility'].values[0]
            #check for PSYCHOLOGICAL FLEXIBILITY sum 
            if sum_of_psych <= 35 and sum_of_psych > 24:
                category_message6 = "You are psychologically flexible – you will not let your emotions become an obstacle in your studies. You can recognize them and handle them in a manner that does not affect your state of studying. "
            elif sum_of_psych <= 24 and sum_of_psych > 13: 
                category_message6 = "You are somewhat psychologically flexible – you are trying not to let your emotions stand in the way of studying, but sometimes you might find yourself being overwhelmed by your feelings, which prevents you from being efficient. Try to reflect on them and recognize why those feelings are being triggered. "
            elif sum_of_psych <= 13:
                category_message6 = "You lack psychological flexibility – you let your emotions overwhelm you and it prevents you from reaching your full potential in your studies. Try spending time reflecting on them and talk to other peers with similar problems. Comparing your previous state of education to the current one can also help recognizing the shift in your mental health and emotions. "
        else:
            category_message6 = "User data not found."
    else: 
        category_message6 = "User email not found."     

    return render_template('6.html', category_message6 = category_message6)

@app.route('/page7')
def page_7():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message7
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_burnout = user_data['Sum of burnout'].values[0]
            if sum_of_burnout <= 45 and sum_of_burnout > 30:
                category_message7 = "You feel burnt out – stress and exhaustion overwhelm you and you might find yourself feeling indifference towards your education. You might also feel inadequate, which leads you to abandoning your studies. Try to take a break from the assignments you have and reflect on your behaviour towards them. Cutting the tasks in smaller pieces might also help you complete them more easily, as well as make you less overwhelmed. Or if it is about having high expections, cut some slack on your expectations towards yourself. If possible, talk to a professional about your burnout. "
            elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
                category_message7 = "You feel somewhat burnt out – you might do well in your studies, but stress, cynicism and feelings of inadequacy might lead you further down the road. Try to stop for a second and reflect on your behaviour, to see whether there is something you can do to lower the risk of reaching full burnout. If you feel like these feelings are getting worse, seek a professional to help you out. "
            elif sum_of_burnout <= 15:
                category_message7 = "You do not feel burnt out – you are able to handle stress and you feel adequate. You do not let your studies exhaust you and your work is not overwhelming you. "
        else:
            category_message7 = "User data not found."
    else: 
        category_message7 = "User email not found."     

    return render_template('7.html', category_message7 = category_message7, sum_of_burnout = sum_of_burnout)

@app.route('/page8')
def page_8():
    # Get the user's email address from the URL query parameter
    user_email = session.get('user_email')    

    if user_email:
        # Check LEARNING category sum
        global category_message8
        user_data = df[df['Email'] == user_email]
        
        if not user_data.empty:
            sum_of_sr = user_data['Sum of self-reflection'].values[0]
            #check for SELF-REFLECTION / SELF-COMPASSION
            if sum_of_sr <= 5 and sum_of_sr > 0:
                category_message8 = "Your self-compassion is good – you are compassionate towards yourself, which makes you achieve more in your studies. You feel understanding towards yourself when you fail or feel inadequate, rather than being self-critical or ignoring it. "
            elif sum_of_sr == 0: 
                category_message8 = "Your self-compassion is somewhat good – you know your worth and capabilities, but sometimes you might find yourself being hard on yourself and feeling self-critical. Try to recognize the achievements you have reached so far and feel prouder about how far you have come. "
            elif math.isnan(sum_of_sr):
                category_message8 = "You lack self-compassion – you might find yourself being rather critical about yourself and your achievements, which might lead you abandoning your responsibilities and tasks. Think about the last achievement you have reached or how you could help other people with your own knowledge and capabilities. If you work on these, you might find yourself being more motivated to continue your studies as you feel more understanding towards yourself. "
        else:
            category_message8 = "User data not found."
    else: 
        category_message8 = "User email not found."     

    return render_template('8.html', category_message8 = category_message8)

if __name__ == '__main__': 
    app.run(debug=True)