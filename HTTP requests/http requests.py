# Python has a built-in package called re, which can be used to work with Regular Expressions
# Import the re module:
import hashlib
import re
import requests
import json

def get_html_by_url(url):
    print()
    
    responseHtml = ""
    
    #Check if content exists in file
    filename = f"HTTP requests/{hashlib.md5(url.encode("utf-8")).hexdigest()}.html"
    try:
        with open(filename, "rt", encoding="utf-8") as file:
            print(f"Reading html from: {filename}")
            responseHtml = file.read()
    except:
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

def show_and_save_re(textData, regexPattern, group = 0, fileToSave = ""):
    try:
        print()
            
        result = re.findall(f"({regexPattern})", textData)
        listResult = [item[group] for item in result]
        
        if listResult:
            print(f"Result by pattern: {regexPattern}")
            print(f"Result count: {len(listResult)}")
            print(f"Result items:")
            
            for item in listResult:
                print(f"\t{item}")
            
            if fileToSave:
                with open(fileToSave, "wt", encoding="utf-8") as file:
                    json.dump(listResult, file)
                print(f"Written to JSON file: {fileToSave}")
        else:
            print(f"NO RESULT BY PATTERN: {regexPattern}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()

if __name__ == "__main__":
    url = "https://www.lejobadequat.com/emplois"
    html = get_html_by_url(url)
    
    #print(html)
    jobsTitlePattern = r'<h3 class="jobCard_title">([\w \/\-àâçéèêëîïôûùüÿñæœ]+)<\/h3>'
    
    show_and_save_re(html, jobsTitlePattern, 1, "HTTP requests/result jobs.json")