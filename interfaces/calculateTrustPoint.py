from interfaces.getPeaks import get_peaks
def calculate_point(SubjectAddress):
    list, last_request = get_peaks(SubjectAddress)
    min_interval = float('inf')
    for time in list:
        interval = abs(last_request - int(time))
        if interval < min_interval:
            min_interval = interval
    if(min_interval < 600):# after 10 min
        return 1
    elif( min_interval < 1800): # after 30 min
        return 0
    elif( min_interval < 3600):# after 1 hour
        return -5
    elif( min_interval < 7200 ):# after 2 hours
        return -10
    elif( min_interval < 14400): # after 4 hours
        return -15
    else:
        return -20

