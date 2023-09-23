import daWithExcel
df = daWithExcel.df
#VARIABLES FOR FRONTEND
    #   sum_of_learning
    #   sum_of_support
    #   sum_of_competence
    #   sum_of_filler
    #   sum_of_se       = Self-efficiancy
    #   sum_of_psych    = psychological flexibility
    #   sum_of_sr       = self-reflection (like self-compasssion / self-critisim)


# Access the latest row in the DataFrame (latest response)
latest_response = df.iloc[-1]

# Extract the relevant values from the latest response
sum_of_learning = latest_response['Sum of learning']
sum_of_support = latest_response['Sum of support']
sum_of_competence = latest_response['Sum of competence']
sum_of_filler = latest_response['Sum of filler']
sum_of_se = latest_response['Sum of self-efficacy']
sum_of_psych = latest_response['Sum of psychological flexibility']
sum_of_burnout = latest_response['Sum of burnout']
sum_of_sr = latest_response['Sum of self-reflection']


# Check LEARNING category sum
if sum_of_learning <= 60 and sum_of_learning > 40:
    #subcategory 1
    #category_message = "Deep approach"  <-- this is for the connection 
    print("Deep approach: ")
elif sum_of_learning <= 40 and sum_of_learning > 20: 
    #subcategory 2
    print("Organized studying: ")
elif sum_of_learning <= 20:
    #subcategory 3
    print("Surface approach: ")


# Check SUPPORT category sum
if sum_of_support <= 165 and sum_of_support > 110:
    #subcategory 1
    print("Felt supported: ")
elif sum_of_support <= 110 and sum_of_support > 55: 
    #subcategory 2
    print("Felt somewhat supported: ")
elif sum_of_support <= 55:
    #subcategory 3
    print("Felt unsupported: ")


# Check COMPETENCE category sum
if sum_of_competence <= 75 and sum_of_competence > 50:
    #subcategory 1
    print("Felt competent: ")
elif sum_of_competence <= 50 and sum_of_competence > 25: 
    #subcategory 2
    print("Felt somewhat competent: ")
elif sum_of_competence <= 25:
    #subcategory 3
    print("Felt incompetent: ")


#check FILLER category sum 
if sum_of_filler <= 85 and sum_of_filler > 57:
    #subcategory 1
    print("Good in career, good objectives: ")
elif sum_of_filler <= 57 and sum_of_filler > 29: 
    #subcategory 2
    print("Somewhat good objectives: ")
elif sum_of_filler <= 29 or sum_of_filler == 0:
    #subcategory 3
    print("Bad objectives, need more improvement: ")


#CHECK FOR WELLBEING - SUBCATEGORIES 
        
#check for SELF-EFFICIANCY sum 
if sum_of_se <= 35 and sum_of_se > 24:
    #subcategory 1
    print("very self-efficiant ")
elif sum_of_se <= 24 and sum_of_se > 13: 
    #subcategory 2
    print("Somewhat self-efficiant ")
elif sum_of_se <= 13:
    #subcategory 3
    print("not self-efficiant ")

#check for PSYCHOLOGICAL FLEXIBILITY sum 
if sum_of_psych <= 35 and sum_of_psych > 24:
    #subcategory 1
    print("very psychologically flexible ")
elif sum_of_psych <= 24 and sum_of_psych > 13: 
    #subcategory 2
    print("Somewhat psychologically flexible")
elif sum_of_psych <= 13:
    #subcategory 3
    print("not psychologically flexible")
    
#check for BURNOUT
if sum_of_burnout <= 45 and sum_of_burnout > 30:
    #subcategory 1
    print("very burnout")
elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
    #subcategory 2
    print("Somewhat burnout")
elif sum_of_burnout <= 15:
    #subcategory 3
    print("no burnout")

#check for SELF-REFLECTION / SELF-COMPASSION
if sum_of_sr <= 5 and sum_of_sr > 0:
    #subcategory 1
    print("good self-reflection")
elif sum_of_sr == 0: 
    #subcategory 2
    print("Somewhat okay self-reflection")
elif sum_of_sr == None:     # bc of NaN values 
    #subcategory 3
    print("bad self-reflection")
