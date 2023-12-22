import datetime


def priority(hour):
    if hour > 15000:
        return 1
    elif hour > 10001 and hour <= 15000:
        return 2
    elif hour > 7301 and hour <= 10000:
        return 3
    elif hour > 4601 and hour <= 7300:
        return 4
    elif hour > 3301 and hour <= 4600:
        return 5
    elif hour > 2401 and hour <= 3300:
        return 6
    elif hour > 1501 and hour <= 2400:
        return 7
    elif hour > 1201 and hour <= 1500:
        return 8
    elif hour > 801 and hour <= 1200:
        return 9
    elif hour > 501 and hour <= 800:
        return 10
    else:
        return 11
    
def senior(hour):
    if hour > 15000:
        senior_g1 = int(hour/4500)
        return senior_g1
    elif hour > 10001 and hour <= 15000:
        return 3
    elif hour > 4601 and hour <= 10000:
        return 2
    elif hour > 1201 and hour <= 4600:
        return 1
    else:
        return 0
    
def staff3(hour):
    if hour > 15000:
        return 0
    elif hour > 2401 and hour <= 15000:
        return 1
    elif hour > 1201 and hour <= 2400:
        return 0
    else:
        return 1
    
def staff2(hour):
    if hour > 15000:
        return 3
    elif hour > 1201 and hour <= 15000:
        return 1
    elif hour > 801 and hour <= 1200:
        return 0
    elif hour > 501 and hour <= 800:
        return 2
    else:
        return 1
    
def trainee(hour):
    if hour > 15000:
        return 2
    elif hour > 10001 and hour <= 15000:
        return 2
    elif hour > 801 and hour <= 10000:
        return 1
    elif hour > 501 and hour <= 800:
        return 0
    else:
        return 1
    
def generate_fy_calendar(BEGIN_FY, END_FY):
    start_date = BEGIN_FY
    end_date = END_FY

    date_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += datetime.timedelta(days=7)
    return date_list

def planejamento(hour):
    if hour > 15000:
        return "Full time"
    elif hour > 7301 and hour <= 15000:
        return 5
    elif hour > 4601 and hour <= 7300:
        return 4
    elif hour > 1501 and hour <= 4600:
        return 3
    elif hour > 1201 and hour <= 1500:
        return 2
    elif hour > 501 and hour <= 1200:
        return 1
    else:
        return 0
    
def interim(hour):
    if hour > 15000:
        return "Full time"
    elif hour > 10001 and hour <= 15000:
        return 7
    elif hour > 4601 and hour <= 10000:
        return 6
    elif hour > 1501 and hour <= 4600:
        return 4
    elif hour > 801 and hour <= 1500:
        return 3
    elif hour > 501 and hour <= 800:
        return 2
    else:
        return 1
    
def final(hour):
    if hour > 15000:
        return "Full time"
    elif hour > 10001 and hour <= 15000:
        return 10
    elif hour > 7301 and hour <= 10000:
        return 9
    elif hour > 4601 and hour <= 7300:
        return 7
    elif hour > 2401 and hour <= 4600:
        return 5
    elif hour > 1501 and hour <= 2400:
        return 4
    else:
        return 3
    
def trimestral(hour):
    if hour > 15000:
        return 4
    elif hour > 7301 and hour <= 15000:
        return 2
    elif hour > 4601 and hour <= 10000:
        return 3
    elif hour > 1501 and hour <= 7300:
        return 2
    elif hour > 1021 and hour <= 1500:
        return 1
    else:
        return 0