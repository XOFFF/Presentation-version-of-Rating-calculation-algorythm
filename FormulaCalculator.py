def calculateByFormula(hoursAtWork, user):
    timeOnWork = user['Time']['On work']
    timeOnRest = user['Time']['On rest']
    employees_points = user['Rating']
    print('Add Rating', employees_points)
    normal_perc_for_work = 60.0 # %
    normal_perc_for_rest = 40.0 # %

    # Check if sum of timeOnWork and timeOnRest is more then hoursAtWork, if more- adapt
    sumOfTime = (timeOnWork + timeOnRest) / 3600
    print('sumOfTime', sumOfTime)
    if sumOfTime > hoursAtWork:
        hoursInPercMore = sumOfTime * 100 / hoursAtWork
        hoursAtWork = hoursAtWork * hoursInPercMore / 100
        normal_perc_for_work = normal_perc_for_work * hoursInPercMore / 100
        normal_perc_for_rest = normal_perc_for_rest * hoursInPercMore / 100
        print('hoursAtWork', hoursAtWork)
        print('hoursInPercMore', hoursInPercMore)
        print('normal_perc_for_job', normal_perc_for_work)
        print('normal_perc_for_rest', normal_perc_for_rest)

    # Set spent time in seconds, convert to hours
    employees_h_f_work_today = timeOnWork / 3600
    employees_h_f_rest_today = timeOnRest / 3600
    # Calculating percentage of work and rest time
    work_perc = employees_h_f_work_today * 100 / hoursAtWork
    rest_perc = employees_h_f_rest_today * 100 / hoursAtWork

    print('work_perc', work_perc)
    print('rest_perc', rest_perc)
    # Check if employee spent time on work more or equal to default work time
    if work_perc >= normal_perc_for_work:
        employees_points += 2
    else:
        employees_points += 1
    print(employees_points)
    # Check if employee spent time on rest less or equal to default work time
    if rest_perc <= normal_perc_for_rest:
        employees_points += 2
    else:
        employees_points += 1
    print(employees_points)

    print(employees_points)
    return employees_points