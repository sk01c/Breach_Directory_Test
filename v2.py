import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)  # or use a specific number like 100
pd.set_option('display.max_columns', None)  # or a specific number of columns
pd.set_option('display.width', 1000)  # adjust as per your screen size
pd.set_option('display.colheader_justify', 'center')  # Center justify column headers
pd.set_option('display.precision', 3)  # Number of decimal places in columns

def get_input(prompt, options=None, min_val=None, max_val=None):
    """ General-purpose input function with optional validation for predefined options or numerical range. """
    while True:
        response = input(prompt).strip().lower()
        if options and response not in options:
            print(f"Invalid input. Please enter one of the following: {', '.join(options)}")
        elif min_val is not None and max_val is not None:
            try:
                response = int(response)
                if min_val <= response <= max_val:
                    return response
                else:
                    print(f"Please enter a value between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid integer.")
        else:
            return response

def append_all(data, keys, values):
    """ Append values to the respective keys in the data dictionary. """
    for key, value in zip(keys, values):
        data[key].append(value)

# Initialize lists in the dictionary with None as placeholders
data = {
    'Names': [],
    'Self Declared': [],
    'Nature of Discovery': [],
    'Dates': [],
    'Entities': [],
    'Department': [],
    'Breach Category': [],
    'MNPI': [],
    'Root Cause Analysis': [],
    'Data/Financial Loss': [],
    'Internal Conflict': [],
    'Intentional Misuse of Confidential Data': [],
    'Customer Detriment': [],
    'Market Impact': [],
    'Reputational Impact': [],
    'Risk Score': [],
    'Risk Rating': []
}

input("Breach Directory. Press enter to continue")

self_declared = get_input("Firstly, could you tell me if this incident was self declared or not? Type yes/no\n", options=["yes", "no"])
append_all(data, ['Self Declared', 'Nature of Discovery'],
           [1 if self_declared == "yes" else 0, "Self declared" if self_declared == "yes" else ""])

if self_declared == "no":
    options = ["1", "2", "3", "4"]
    nature_of_discovery = get_input("Please enter the nature of discovery given the following options:\n"
                                    "1) Data from HR\n2) Data from internal audit\n3) Data from external audit\n4) Other\nPlease select a number\n",
                                    options=options)
    data['Nature of Discovery'].append(nature_of_discovery)  # Append instead of replacing

append_all(data, ['Names', 'Dates', 'Entities', 'Department', 'Breach Category'],
           [get_input("Please enter the name of the person who is under investigation\n"),
            get_input("Please enter the date of the incident in the form dd/mm/yyyy\n"),
            get_input("Please enter the entity in which this incident took place\n"),
            get_input("Please enter the department in which this took place\n"),
            get_input("Please enter the breach category\n")])

data_loss = get_input("Before we continue, we need to clarify if this breach resulted in data loss. Please enter yes or no\n", options=["yes", "no"])
if data_loss == "yes":
    input("Please contact ITSD to ensure this issue has been dealt with before returning. Press enter to continue once contacted\n")

mnpi = get_input("Was this a case of MNPI (insider information involved)? Please enter yes or no\n", options=["yes", "no"])
data['MNPI'].append(1 if mnpi == "yes" else 0)
if mnpi == "yes":
    input("Please contact the Compliance Advisory Team to ensure this issue has been dealt with before returning. Press enter to continue once contacted\n")

root_cause = get_input("Please enter which root cause you see as most apt for this breach: \n1) Human Error \n2) Negligence\n3) Intentional\n4) Process Error\n5) Other\nPlease select a number to continue\n", options=["1", "2", "3", "4", "5"])
data['Root Cause Analysis'].append(root_cause)

input("Now we will assign a score to the breach severity. For the following criteria, please enter a severity rating from 0 to 10\nPress enter to continue")
criteria = ['Data/Financial Loss', 'Internal Conflict', 'Intentional Misuse of Confidential Data', 'Customer Detriment', 'Market Impact', 'Reputational Impact']
for crit in criteria:
    print(f"Please rate the severity of '{crit}':")
    response = get_input(f"Severity of '{crit}' (0-10):\n", min_val=0, max_val=10)
    data[crit].append(int(response))  # Ensure the response is converted to an integer

# Ensure all lists in data have the same length
max_length = max(len(v) for v in data.values())
for key, value in data.items():
    if len(value) < max_length:
        data[key].extend([None] * (max_length - len(value)))

weights = {
    'Data/Financial Loss': 7,
    'Internal Conflict': 3,
    'Intentional Misuse of Confidential Data': 8,
    'Customer Detriment': 8,
    'Market Impact': 8,
    'Reputational Impact': 5
}

total_risk_score = []

for i in range(max_length):
    total_risk_score.append(0)
    for crit in criteria:
        score = data[crit][i]
        if isinstance(score, int):
            weight = weights[crit]
            risk_score = score * weight

    data["Risk Score"].append(risk_score)

data["Risk Rating"] = ["High" if score > 80 else "Medium" if score > 40 else "Low" for score in total_risk_score]

max_length = np.max([len(v) for v in data.values()])

for key, value in data.items():
    if len(value) < max_length:
        data[key].extend([None] * (max_length - len(value)))

df = pd.DataFrame(data)
breach_log = get_input("Type 'okay' to see how this tool could be used to generate a breach log\n", options=["okay", "no"])
if breach_log == 'okay':
    print(df)
