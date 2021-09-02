# Insight Script
## Convert csv into json

import csv
import json
import pandas as pd
from decimal import Decimal
import locale
from re import sub

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
def make_json(csvFilePath, jsonFilePath):

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows


        # Open a json writer, and use the json.dumps()
        # function to dump data

        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            jsonf.write(json.dumps(data, indent=4))
        
        return json.dumps(data, indent=4)

def convert_csv_to_dict(csvFilePath):
    df = pd.read_csv(csvFilePath, usecols=['Date', 'Expense Details', 'Amount', 'Recurring', 'Account', 'Notes'])
    dict_from_csv = df.to_dict(orient='records')
    return dict_from_csv

def convert_to_money(amount):
    return Decimal(sub(r'[^\d.]', '', amount[1:]))

def is_in_expense_details(word, expenseDetails):
    return word in expenseDetails

def calculate_recurring_bills(data):
    recurring_amount = 0
    for row in data:
        if row['Recurring'] == True:
            recurring_amount += convert_to_money(row['Amount'])  #Decimal(locale.atoi(dollar[1:]))

    return recurring_amount

def calculate_amazon_purchase(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring'] and is_in_expense_details("Amazon", row['Expense Details']):
            recurring_amount += convert_to_money(row['Amount'])
    return recurring_amount

def calculate_takeout(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring']:
            expense_details = row['Expense Details']
            if is_in_expense_details("Uber Eats", expense_details) or is_in_expense_details("Doordash", expense_details) or is_in_expense_details("UBER EATS", expense_details) or is_in_expense_details("Eating Out", expense_details):
                recurring_amount += convert_to_money(row['Amount'])

    return recurring_amount

def calculate_social(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring'] and is_in_expense_details("Social", row['Expense Details']):
            recurring_amount += convert_to_money(row['Amount'])
    return recurring_amount

def calculate_mental_health(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring']:
            expense_details = row['Expense Details']
            if is_in_expense_details("Nurse NP", expense_details) or is_in_expense_details("Dr. Jennings",
                                                                                            expense_details) or is_in_expense_details(
                    "CVS", expense_details) or is_in_expense_details("Pharmacy", expense_details):
                recurring_amount += convert_to_money(row['Amount'])

    return recurring_amount

def calculate_accident_cost(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring']:
            expense_details = row['Expense Details']
            if is_in_expense_details("Chiropractor", expense_details):
                recurring_amount += convert_to_money(row['Amount'])

    return recurring_amount

def lyft_uber_cost(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring']:
            expense_details = row['Expense Details']
            if is_in_expense_details("Lyft", expense_details) or is_in_expense_details("LYFT", expense_details):
                recurring_amount += convert_to_money(row['Amount'])

    return recurring_amount

def calculate_cofee_snacks_cost(data):
    recurring_amount = 0
    for row in data:
        if not row['Recurring']:
            expense_details = row['Expense Details']
            if is_in_expense_details("Coffee", expense_details) or is_in_expense_details("Snacks", expense_details):
                recurring_amount += convert_to_money(row['Amount'])

    return recurring_amount

def how_much_per_day(data):
    # calculate how much money I spend each day of the month across all acounts
    # return a dictionary with the [{date: amount}, ...] or {date: amount, date:amount, ...}
    return 0

def number_of_takeout_orders(data):
    # calculate the number of days that you order take out or even just the number of take transactions you have
    return 0

def calculate_how_far_from_budget(actual, expected):
    ## calculate the difference between how much you spent per month to how much you said you would spend
    return 0

# Driver Code

# Decide the two file paths according to your computer system
csvFilePath = r'/Users/christinahoward/Downloads/august_2021_expense_report.csv'
jsonFilePath = r'/Users/christinahoward/Downloads/august_2021_expense_report.json'

# Budget
RECURRING_BUDGET = "$1889.97"
AMAZON_BUDGET = "$500.00"
TAKEOUT_BUDGET = "$224.00"
MAX_TAKEOUT_MEALS_PER_MONTH = 8
SOCIAL_BUDGET = "$300.00"
MENTAL_HEALTH_BUDGET = "$160.00"
ACCIDENT_BUDGET = "$0"
LYFT = "$75.00"
COFFEE_SNACKS = "$100.00"

raw_json_data = make_json(csvFilePath, jsonFilePath)
data = convert_csv_to_dict(csvFilePath)
recurringAmount = calculate_recurring_bills(data)
amazonAmount = calculate_amazon_purchase(data)
takeoutAmount = calculate_takeout(data)
socialAmount = calculate_social(data)
mentalHealthAmount = calculate_mental_health(data)
accidentAmount = calculate_accident_cost(data)
lyftAmount = lyft_uber_cost(data)
coffeeSnacksAmount = calculate_cofee_snacks_cost(data)

print("Recurring: ", recurringAmount)
print("Amazon: ", amazonAmount)
print("Takeout: ", takeoutAmount)
print("Social: ", socialAmount)
print("Mental Health: ", mentalHealthAmount)
print("Accident: ", accidentAmount)
print("Lyft: ", lyftAmount)
print("Coffee/Snacks: ", coffeeSnacksAmount)