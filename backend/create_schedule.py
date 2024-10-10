import openai
import requests
import json

# Set up the OpenAI API Key
openai.api_key = "your-openai-api-key"

def create_weekly_schedule():
    max_weekly_hours = 224
    employer_information = define_employer(max_weekly_hours)
    
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    employees = get_all_employees()

    # Structure the input to send to GPT-4
    input_data = {
        "max_weekly_hours": max_weekly_hours,
        "days_of_the_week": days_of_the_week,
        "employees": employees.json(),  # Assuming your API returns JSON data
    }

    # Send the structured input to GPT-4
    weekly_schedule = generate_schedule_with_gpt4(input_data)

    # Process and output the schedule
    if weekly_schedule:
        process_weekly_schedule(weekly_schedule)
    else:
        print("Failed to generate a schedule")


def generate_schedule_with_gpt4(input_data):
    prompt = f"""
    You are tasked with generating a weekly work schedule for a company. The company has a maximum of {input_data['max_weekly_hours']} hours to allocate across employees for the week. 
    The employees, along with their availability,efficiency how muuch they like another empoloyee, are as follows:

    {json.dumps(input_data['employees'], indent=2)}

    Your task is to allocate the available hours across the days of the week: {input_data['days_of_the_week']}.
    If an employee works with an employee they like 5 and up they're efficiencies increase by that percentage
    If the likeness is under 5, both of their efficiency decrease by that percentage
    If there is no likeness score assume it is 5 and if it is 5 there is no change to the efficiency
    Consider each employee's availability efficiency, likeness score to create a balanced schedule.
    Return the schedule in JSON format with each day containing a list of employee shifts as well as the efficiency for that specific day. 
    """

    response = openai.Completion.create(
        engine="gpt-4",  # Or "gpt-3.5-turbo" if using GPT-3.5
        prompt=prompt,
        max_tokens=1500,
        temperature=0.7
    )

    try:
        return json.loads(response.choices[0].text.strip())
    except json.JSONDecodeError:
        print("Failed to parse the GPT-4 response")
        return None


def get_all_employees():
    response = requests.get("http://127.0.0.1:5000/employees")
    return response


def process_weekly_schedule(weekly_schedule):
    # This function processes and outputs the generated schedule
    for day, shifts in weekly_schedule.items():
        print(f"--- {day} ---")
        for shift in shifts:
            print(f"Employee {shift['employee']} works from {shift['time_slot']} (Efficiency: {shift['efficiency']})")


# Define Employer information (mock function)
def define_employer(max_weekly_hours):
    return {
        "max_weekly_hours": max_weekly_hours
    }


# Call the function to create the schedule
create_weekly_schedule()
