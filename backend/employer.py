"""Used to define the employer based on user inputs but if not it will be pre-defined"""

#Lets say there are 2 shifts and 2 employeers per shift each employee works 8 hours 
#Thats 32 per day 
#224 per week
class Employer:
    def __init__(self, max_weekly_hours):
        self.max_weekly_horus = max_weekly_hours
        self.max_daily_hours = max_weekly_hours//7

def define_empoyer(max_weekly_hours = 224):
    employer = Employer(max_weekly_hours)
    return employer
    

