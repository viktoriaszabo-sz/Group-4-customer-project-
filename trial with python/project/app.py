import pandas as pd
from flask import Flask, render_template
# run this code into powershell: pip install Flask 

app = Flask(__name__, static_url_path='/static')

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



#VARIABLES FOR FRONTEND
    #   sum_of_learning
    #   sum_of_support
    #   sum_of_competence
    #   sum_of_filler
    #   sum_of_se       = Self-efficiancy
    #   sum_of_psych    = psychological flexibility
    #   sum_of_sr       = self-reflection (like self-compasssion / self-critisim)


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

    return render_template('welcome.html')

@app.route('/page1')
def page_1():
    # Check LEARNING category sum
    global category_message1
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_learning = latest_response['Sum of learning']

    if sum_of_learning <= 60 and sum_of_learning > 40:
        #subcategory 1
        category_message1 = "You have a deep approach to learning, meaning that you aim to understand what you have learned in a deeper level, and you try to find connections, as well as find underlying meanings. You find yourself motivated to learn and often have the appropriate background knowledge to connect the new information with the old. "  # <-- this is for the connection 
    elif sum_of_learning <= 40 and sum_of_learning > 20: 
        #subcategory 2
        category_message1 = "Your studying is organized. You might not necessarily take a deep approach to learning, but you are more organized than someone who takes on a surface approach. You have the tools to shift to deeper understanding if you want to learn to understand and focus on the meaning, but you can also find yourself easily just repeating the learned information without deeper understanding. "
    elif sum_of_learning <= 20:
        #subcategory 3
        category_message1 = "You have a surface approach to learning, meaning your learning aims for repetition. This approach is not reflective and studying might often be done in the last minute. This results in fragmented understanding and things you memorized are often forgotten. Typically, you are not interested in understanding and just want to learn what is required.  "

    #render the HTML template and pass data to it 
    return render_template('1.html', category_message1 = category_message1)

@app.route('/page2')
def page_2():
    
    global category_message2
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_support = latest_response['Sum of support']

    # Check SUPPORT category sum
    if sum_of_support <= 165 and sum_of_support > 110:
        #subcategory 1
        category_message2 = "Learning environment: You feel supported in your studies. Your learning environment supports your learning, and you can work well with other students. You get feedback that is accurate, and you feel like guidance is available whenever you need it.  "
    elif sum_of_support <= 110 and sum_of_support > 55: 
        #subcategory 2
        category_message2 = "Learning environment: You feel somewhat supported. Your learning environment somewhat does its job at supporting you, but it might feel a bit lacking. You get along with other students when it comes to working and studying, if need be, but it does not always feel too fulfilling.  "
    elif sum_of_support <= 55:
        #subcategory 3
        category_message2 = "Learning environment: You feel like you do not get enough support and the learning environment does not support you the way it should. Maybe it is the lack of feedback or guidance, or you do not feel comfortable working with other students. Whichever the case, try to bring this topic up to someone that might help you feel more supported, such as a teacher or student counsellor. "

    return render_template('2.html', category_message2 = category_message2)

@app.route('/page3')
def page_3():
    
    global category_message3
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_competence = latest_response['Sum of competence']


    # Check COMPETENCE category sum
    if sum_of_competence <= 75 and sum_of_competence > 50:
        #subcategory 1
        category_message3 = "Felt competent: "
    elif sum_of_competence <= 50 and sum_of_competence > 25: 
        #subcategory 2
        category_message3 = "Felt somewhat competent: "
    elif sum_of_competence <= 25:
        #subcategory 3
        category_message3 = "Felt incompetent: "

    return render_template('3.html', category_message3 = category_message3)

@app.route('/page4')
def page_4():
    
    global category_message4
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_filler = latest_response['Sum of filler']

    #check FILLER category sum 
    if sum_of_filler <= 85 and sum_of_filler > 57:
        #subcategory 1
        category_message4 = "Future objectives: You have clear objectives for the future. You use the resources that are given to you and always try to max out your opportunities, whether it’s about international interactions or work placement. Maybe even entrepreneurship enthusiasm.  "
    elif sum_of_filler <= 57 and sum_of_filler > 29: 
        #subcategory 2
        category_message4 = "Future objectives: You recognize the options given to you and work with them but might lack the possibility to use them to your own advantage. Try interacting more with internationals or dig up some articles about the work placement advice provided by the university. You could also think about some entrepreneurial tendencies that you might have.  "
    elif sum_of_filler <= 29 or sum_of_filler == 0:
        #subcategory 3
        category_message4 = "Future objectives: Your objectives for the future are not as clear as it should be. You might feel you can’t properly use the resources that are given to you or might not even feel like there’s anything to begin with. Try reaching out to your guidance counsellor or talk to peers in higher years to get some information regarding work placement, international opportunities or sustainability.  "

    return render_template('4.html', category_message4 = category_message4)

@app.route('/page5')
def page_5():
    
    global category_message5
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_se = latest_response['Sum of self-efficacy']

    #CHECK FOR WELLBEING - SUBCATEGORIES 
            
    #check for SELF-EFFICIANCY sum 
    if sum_of_se <= 35 and sum_of_se > 24:
        #subcategory 1
        category_message5 = "WELLBEING: Self-efficacy: You are very self-efficient– you trust in yourself and your capabilities, which makes you an efficient learner as well. You persist working towards your future and won’t let anything stand in your way. "
    elif sum_of_se <= 24 and sum_of_se > 13: 
        #subcategory 2
        category_message5 = "Self-efficacy: You are some-what self-efficient– you recognize your capabilities but won’t trust them to its full extent; you might be a hard-worker, but the lack of self-trust prevents you from reaching your full extent.  Seek more opportunities for engaging in learning activities.  "
    elif sum_of_se <= 13:
        #subcategory 3
        category_message5 = "Self-efficacy: Your self-efficacy needs to get back on track – you don’t necessarily trust your capabilities, which might cause you not putting enough effort in your studies and avoiding tasks or assignments. Recognize your previous achievements, so that you can be more persistent in your studies. Also, try reaching out to other students with similar situations, so you could feel more seen and heard about your problems.  "

    
    return render_template('5.html', category_message5 = category_message5)

@app.route('/page6')
def page_6():
    
    global category_message6
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_psych = latest_response['Sum of psychological flexibility']

    
     #check for PSYCHOLOGICAL FLEXIBILITY sum 
    if sum_of_psych <= 35 and sum_of_psych > 24:
        #subcategory 1
        category_message6 = "very psychologically flexible "
    elif sum_of_psych <= 24 and sum_of_psych > 13: 
        #subcategory 2
        category_message6 = "Somewhat psychologically flexible"
    elif sum_of_psych <= 13:
        #subcategory 3
        category_message6 = "not psychologically flexible"

    return render_template('6.html', category_message6 = category_message6)

@app.route('/page7')
def page_7():
    
    global category_message7
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_burnout = latest_response['Sum of burnout']

    
    #check for BURNOUT
    if sum_of_burnout <= 45 and sum_of_burnout > 30:
        #subcategory 1
        category_message7 = "very burnout"
    elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
        #subcategory 2
        category_message7 = "Somewhat burnout"
    elif sum_of_burnout <= 15:
        #subcategory 3
        category_message7 = "no burnout"


    return render_template('7.html', category_message7 = category_message7)


@app.route('/page8')
def page_8():
    
    global category_message8
    # Access the latest row in the DataFrame (latest response)
    latest_response = df.iloc[-1]
    # Extract the relevant values from the latest response
    sum_of_sr = latest_response['Sum of self-reflection']

    
    #check for SELF-REFLECTION / SELF-COMPASSION
    if sum_of_sr <= 5 and sum_of_sr > 0:
        #subcategory 1
        category_message8 = "Self-reflection: You have a good self- compassion – you are compassionate towards yourself and situations, which makes you achieve more in your studies.  "
    #elif sum_of_sr == 0: 
        #subcategory 2
        category_message8 = "Self-reflection: You have a somewhat good self- compassion – you know your worth and capabilities, but sometimes you might find yourself being hard on yourself and feeling self-critical. Try to recognize the achievements you reached so far and feel prouder about how far you’ve come.  "
    

    return render_template('8.html', category_message8 = category_message8)



if __name__ == '__main__': 
    app.run(debug=True)

