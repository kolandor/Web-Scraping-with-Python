import json


def json_parse_sample():
    #read JSON data from file
    with open("JSON parse/JSON sample.json", "rt") as file:
        jsonData = json.load(file)#load JSON from file
    
    # The object type returned by the json.load function in Python depends on the structure of the JSON data it processes.

    # In most cases json.load returns:

    # Dictionary (dict): If the JSON data is a JSON object.
    # List: If the JSON data is a JSON array.
    # String (str): If the JSON data is a JSON string.
    # Number (int or float): If the JSON data is a JSON number.
    # True or False: If the JSON data is a JSON boolean value.
    # None: If the JSON data is null in JSON.
    
    print(f"JSON result object type: {type(jsonData)}")
    
    #print facts
    for element in jsonData: #iterating over JSON list
        print(element.get("fact"))#Get facts from each element

# Entry point
if __name__ == '__main__':
    json_parse_sample()
    #какие методы присутствуют у результирующего объекта 