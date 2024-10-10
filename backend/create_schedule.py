from employer import define_empoyer
import requests

def create_weekly_schedule():
    max_weekly_hours = 224
    employer_infromation = define_empoyer(224)

    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']




def define_weekly_efficiency(weekly_schedule):
    efficiency = 0
    days_of_the_week = 7



    return efficiency


def get_all_employees():
    employees = requests.get("http://127.0.0.1:5000/")
    return employees

