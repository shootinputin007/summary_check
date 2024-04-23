import re
import json

# Loading the data

with open('sim_data.json', 'r') as file:
    sim_data = json.load(file)

with open('explanation_content.txt', 'r') as file:
    explanation_content = file.read()


# Recursively iterates over json object looking for 'amount' key values
def explore_json(obj, amounts):
    try:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == 'amount':
                    amounts.append(value)
                explore_json(value, amounts)
        elif isinstance(obj, list):
            for item in obj:
                explore_json(item, amounts)
        else:
            pass
    
    except Exception as e:
        print("explore_json error: ", e)

# Extracts amount values from json
def extract_amounts(json_obj):
    try:
        amounts = []
        explore_json(json_obj['asset_changes'], amounts)
        amounts = set(amounts)
        return amounts
    
    except Exception as e:
        print("extract_amounts error: ", e)


# Extracts numeric values from summary
def extract_values_summary (explanation_content):
    pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d+(?:\.\d+)?\b'
    summary_amounts = re.findall(pattern, explanation_content)
    summary_amounts = set(summary_amounts)
    return summary_amounts

# Cleaning the strings during comparison
def clean (string):
    string = string.replace(',', '').replace('.', '')
    string = string.lstrip('0')
    return string

# Extract values present in summary but not present in asset_changes
def extract_missing(summary_amounts, json_amounts):
    missing_vals = []
    for summary_value in summary_amounts:
        if summary_value.replace(",","") not in json_amounts:
            missing_vals.append(summary_value)
    return missing_vals

# Check if all values from json data are present in summary values
def check1(json_amounts, summary_amounts):
    for json_value in json_amounts:
        found = False
        for summary_value in summary_amounts:
            if json_value == summary_value.replace(",",""):
                found = True
                break
        if not found:
            return False
    return True

# Check if there are values in summary with misapplied decimals
def check2(json_amounts, summary_amounts):
    missing_values = extract_missing(summary_amounts, json_amounts)
    cleaned_missing_values = [clean(value) for value in missing_values]
    cleaned_json_amounts = [clean(value) for value in json_amounts]
    for missing_value in cleaned_missing_values:
        if missing_value in cleaned_json_amounts:
            return False

    return True


def summary_check(sim_data, explanation_content):
    json_amounts = extract_amounts(sim_data)
    summary_amounts = extract_values_summary(explanation_content)
    
    # Check if all values from json_amounts are present in summary_amounts
    if not check1(json_amounts, summary_amounts):
        return False
    
    # Check if there are any values with wrong decimals
    if not check2(json_amounts, summary_amounts):
        return False
    
    # If both checks pass, return True
    return True


res = summary_check(sim_data, explanation_content)
print(res)
