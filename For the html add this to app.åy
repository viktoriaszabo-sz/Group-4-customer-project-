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
        category_message7 = "You have reached the level of burnout – stress and exhaustion overwhelm you and might find yourself feeling cynical towards your education. You might also feel inadequate, which leads you to abandon your studies. Try to take a break from the assignments you have and reflect on your behaviour towards them. Whether or not you should leave tasks behind that’s not your responsibility, cutting some slacks on your expectations towards yourself. If necessary, talk to a professional about your issues.  "
    elif sum_of_burnout <= 30 and sum_of_burnout > 15: 
        #subcategory 2
        category_message7 = "You are somewhat burned-out – you might do well in your studies, but stress, cynicism and feelings of inadequacy might lead you further down the road. Try to stop for a second and reflect on your behaviour, to see whether there’s anything you can do to lower the risk of reaching full burn-out.  "
    elif sum_of_burnout <= 15:
        #subcategory 3
        category_message7 = "You haven’t reached the level of burnout – you can separate many stages of your life from one another and won’t let your studies exhaust you out or feel cynical towards your studies.  "


    return render_template('7.html', category_message7 = category_message7, sum_of_burnout = sum_of_burnout)
