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

for index, row in df.iterrows():
    sum_of_learning = row['Sum of learning']
    sum_of_support = row['Sum of support']
    sum_of_competence = row['Sum of competence']
    sum_of_filler = row['Sum of filler']
 
    sum_of_se = row['Sum of self-efficacy']
    sum_of_psych = row['Sum of psychological flexibility']
    sum_of_burnout = row['Sum of burnout']
    sum_of_sr = row['Sum of self-reflection']

    # Check LEARNING category sum
    if sum_of_learning <= 60 and sum_of_learning > 40:
        #subcategory 1
        print(f"{index + 1}: Deep approach: ")
    elif sum_of_learning <= 40 and sum_of_learning > 20: 
        #subcategory 2
        print(f"{index + 1}: Organized studying: ")
    elif sum_of_learning <= 20:
        #subcategory 3
        print(f"{index + 1}: Surface approach: ")


    # Check SUPPORT category sum
    if sum_of_support <= 165 and sum_of_support > 110:
        #subcategory 1
        print(f"{index + 1}: Felt supported: ")
    elif sum_of_support <= 110 and sum_of_support > 55: 
        #subcategory 2
        print(f"{index + 1}: Felt somewhat supported: ")
    elif sum_of_support <= 55:
        #subcategory 3
        print(f"{index + 1}: Felt unsupported: ")


    # Check COMPETENCE category sum
    if sum_of_competence <= 75 and sum_of_competence > 50:
        #subcategory 1
        print(f"{index + 1}: Felt competent: ")
    elif sum_of_competence <= 50 and sum_of_competence > 25: 
        #subcategory 2
        print(f"{index + 1}: Felt somewhat competent: ")
    elif sum_of_competence <= 25:
        #subcategory 3
        print(f"{index + 1}: Felt incompetent: ")


    #check FILLER category sum 
    if sum_of_filler <= 85 and sum_of_filler > 42:
        #subcategory 1
        print(f"{index + 1}: Good in career, good objectives: ")
    elif sum_of_filler <= 42 and sum_of_filler > 0: 
        #subcategory 2
        print(f"{index + 1}: Somewhat good objectives: ")
    elif sum_of_filler == 0:
        #subcategory 3
        print(f"{index + 1}: BAd objectives, need more improvement: ")


    #CHECK FOR WELLBEING - SUBCATEGORIES 
        
    #check for SELF-EFFICIANCY sum 
    if sum_of_se <= 35 and sum_of_se > 24:
        #subcategory 1
        print(f"{index + 1}: very self-efficiant ")
    elif sum_of_se <= 24 and sum_of_se > 13: 
        #subcategory 2
        print(f"{index + 1}: Somewhat self-efficiant ")
    elif sum_of_se <= 13:
        #subcategory 3
        print(f"{index + 1}: not self-efficiant ")

    #check for PSYCHOLOGICAL FLEXIBILITY sum 
    if sum_of_psych <= 35 and sum_of_psych > 24:
        #subcategory 1
        print(f"{index + 1}: very psychologically flexible ")
    elif sum_of_psych <= 24 and sum_of_psych > 13: 
        #subcategory 2
        print(f"{index + 1}: Somewhat psychologically flexible")
    elif sum_of_psych <= 13:
        #subcategory 3
        print(f"{index + 1}: not psychologically flexible")
    
    #check for BURNOUT
    if sum_of_burnout <= 45 and sum_of_burnout > 30:
        #subcategory 1
        print(f"{index + 1}: very burnout")
    elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
        #subcategory 2
        print(f"{index + 1}: Somewhat burnout")
    elif sum_of_burnout <= 15:
        #subcategory 3
        print(f"{index + 1}: no burnout")

    #check for SELF-REFLECTION
    if sum_of_sr <= 5 and sum_of_sr > 0:
        #subcategory 1
        print(f"{index + 1}: good self-reflection")
    elif sum_of_sr == 0: 
        #subcategory 2
        print(f"{index + 1}: Somewhat okay self-reflection")
    elif sum_of_sr < 0: 
        #subcategory 3
        print(f"{index + 1}: bad self-reflection")
