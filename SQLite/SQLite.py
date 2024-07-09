# sqlite3 — DB-API 2.0 interface for SQLite databases
# https://docs.python.org/3/library/sqlite3.html

import hashlib
import re
import requests
import json
import os
import sqlite3
from pprint import pprint

# url: traget url
# hardload: download HTML even if file exists
def get_html_by_url(url, hardload = False):
    print()
    
    responseHtml = ""
    
    filename = f"SQLite/{hashlib.md5(url.encode("utf-8")).hexdigest()}.html"
    
    #Check if content exists in file AD not hardload
    if os.path.exists(filename) and not hardload:
        with open(filename, "rt", encoding="utf-8") as file:
            print(f"Reading html from: {filename}")
            responseHtml = file.read()
    else:
        print(f"Getting html from: {url}")
        response = requests.get(url)
        print('Status code:', response.status_code)
        
        if response.status_code < 200 or response.status_code > 299:
            raise Exception(f"Status coge {response.status_code} by getting from: {url}")
        
        responseHtml = response.text
        with open(filename, "wt", encoding="utf-8") as file:
            file.write(responseHtml)
            
    with open(filename, "rt", encoding="utf-8") as file:
            responseHtml = file.read()
    
    print()
    return responseHtml

#Key is the group name in the dictionary containing the group number
# Dictionary pattern where the result of the zero group will be stored under the "Main" key
# !!!!A zero group is created automatically for the entire pattern
# {"main":0}
def get_list_by_re(textData, regexPattern, groups = {"main":0}):
    try:
        print()
        
        # Finding all matches according to the ReGex pattern
        # !!!!A zero group is created automatically for the entire pattern
        result = re.findall(f"({regexPattern})", textData)
        
        #resulting list of dictionaries
        listOfDictsResult = []
        
        for item in result:#Walk through results
            
            # The dictionary into which the result extracted from the groups will be saved
            subDictGroupResult = {}
            
            #Fetching dictionary keys (group)
            for group in groups: #Walking through groups to select them from the result
                
                # taking group value from dictionary(groups[group] 
                # Writing the group result (item[groups[group]]) 
                # to a temporary dictionary (subDictGroupResult[group])
                subDictGroupResult[group] = item[groups[group]]
            
            # Adding a temporary dictionary to the list
            listOfDictsResult.append(subDictGroupResult)
        
        #result information
        if listOfDictsResult:
            print(f"Result by pattern: {regexPattern}")
            print(f"Result count: {len(listOfDictsResult)}")
            print(f"Result items:")
            #show result
            pprint(listOfDictsResult)
            
        else:
            print(f"NO RESULT BY PATTERN: {regexPattern}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()
    
    return listOfDictsResult

def save_list_to_JSON_file(listResult = [], fileToSave = "result.json"):
    try:
        print()
        if fileToSave:
            with open(fileToSave, "wt", encoding="utf-8") as file:
                    json.dump(listResult, file)
                    print(f"Written to JSON file: {fileToSave}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()

#create db for saving jobs
def create_rawScript_SQLite_db(dbFileName = "sqlite.db"):
    try:
        if os.path.exists(dbFileName):
            print(f"Delete {dbFileName}")
            os.remove(dbFileName)
        
        print(f"Create SQLite DB: {dbFileName}")
        with sqlite3.connect(dbFileName) as connection:
            cursor = connection.cursor()

            print(f"Create table jobs")
            sql = """
                create table if not exists jobs (
                    id integer primary key,
                    job_title text,
                    job_url text
                )
            """
            cursor.execute(sql)
            
    except Exception as e:
        print(f"ERROR: {e}")
    
#save result jobs list to 
def save_list_to_SQLite_file(listResult = [], columns = [], dbFileName = "sqlite.db"):
    try:
        create_rawScript_SQLite_db(dbFileName)
        
        with sqlite3.connect(dbFileName) as connection:
            cursor = connection.cursor()

            print("Write result list to SQLite DB")
            for element in listResult:
                cursor.execute("""
                    insert into jobs (job_title, job_url)
                    values (?, ?)
                """, (element[columns[0]], element[columns[1]]))
                
            connection.commit()
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    url = "https://www.lejobadequat.com/emplois"
    html = get_html_by_url(url)
    
    urlPattern = r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*))'
    jobNamePattern = r'(<h3 class="jobCard_title"[^>]*>([\s\S]*?)<\/h3>)'
    #Patternt to selecting articles
    fullPatterrArticlePattern = fr'<article[^>]*>[\s\S]*?{urlPattern}[\s\S]*?{jobNamePattern}[\s\S]*?<\/article>'
    
    resultJobsNameRefs = get_list_by_re(html, fullPatterrArticlePattern, {"JobName" : 5, "JobRef" : 1})
    
    jsonFilePath  = "SQLite/ResultJobsNameRefs.json"
    save_list_to_JSON_file(resultJobsNameRefs, jsonFilePath)
    
    SQLliteFilePath = "SQLite/ResultSQLiteBatabaseJobs.db"
    save_list_to_SQLite_file(resultJobsNameRefs, ["JobName", "JobRef"], SQLliteFilePath)