# Beautiful Soup
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import hashlib
import json
import os
from pprint import pprint
import requests
from bs4 import BeautifulSoup

# url: traget url
# saveFolder: 
# hardload: download HTML even if file exists
# userAgent: 
def get_html_by_url(url, saveFolder = "Beautiful Soup/htmlbin", hardload = False, userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"):
    try:
        print()
    
        responseHtml = ""
        
        filename = f"{saveFolder}/{hashlib.md5(url.encode("utf-8")).hexdigest()}.html"
        
        #Check if content exists in file AD not hardload
        if os.path.exists(filename) and not hardload:
            with open(filename, "rt", encoding="utf-8") as file:
                print(f"Reading html from: {filename}")
                responseHtml = file.read()
        else:
            print(f"Getting html from: {url}")
            response = requests.get(
                url=url, #url
                headers={#use headers to add my browser user agent
                "User-Agent" : userAgent
                })
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
    except Exception as e:
        print(f"ERROR: {e}")

def get_bbc_sport_news_by_soup(newsMaxCountReturn):
    try:
        htmlContent = get_html_by_url(r"https://www.bbc.com/sport", hardload=True)
        
        soup = BeautifulSoup(htmlContent, features="lxml")
        
        #Get sports news promos by tag div contains data-testid="promo" AND type
        promos = soup.find_all("div", {"data-testid": "promo", "type": True})
        
        promosData = []
        
        counter = newsMaxCountReturn
        
        for promo in promos:
            tempDictPromosData = {}
            try:
                promoATags = promo.find_all("a")
                
                if promoATags is not None and len(promoATags):
                    
                    aTag = promoATags[0]
                    
                    #Check reference
                    if aTag.parent.has_attr("spacing"):
                        # The tag does not contain a full link, but navigation within the site, so we use concatenation
                        tempDictPromosData["Link"] = f"https://www.bbc.com{aTag["href"]}"
                        
                        #Skip life and video (is no contains topics)
                        if "live" in tempDictPromosData["Link"] or "videos" in tempDictPromosData["Link"]:
                            continue
                    else:
                        continue
                    
                    #Then jump into news
                    currentNewsHtml = get_html_by_url(tempDictPromosData["Link"], hardload=True)
                    
                    currentNewsSoup = BeautifulSoup(currentNewsHtml, features="lxml")
                    
                    #Find list of topics 
                    ulOfTopics = currentNewsSoup.find("ul", {"spacing": "2"})
                    if ulOfTopics is None:
                        tempDictPromosData["Topics"] = None
                    else:
                        tempDictPromosData["Topics"] = []
                    
                        #Check parrent is a TopicList
                        classTopicList = ulOfTopics.parent.previousSibling.get("class")
                        if classTopicList:
                            if "TopicList" in classTopicList[0]:
                                for liTopic in ulOfTopics.children:
                                    tempDictPromosData["Topics"].append(liTopic.find("a").text)
                
                promosData.append(tempDictPromosData)
                counter -= 1
            except Exception as e:
                print(f"ERROR: {e}")
            
            if not counter:
                break
        
        pprint(promosData)
        print(len(promosData))
        
        return promosData
    except Exception as e:
        print(f"ERROR: {e}")

def save_list_to_JSON_file(listResult = [], fileToSave = "result.json"):
    try:
        print()
        if fileToSave:
            with open(fileToSave, "wt", encoding="utf-8") as file:
                    json.dump(listResult, file, indent=4)
                    print(f"Written to JSON file: {fileToSave}")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        print()

if __name__ == "__main__":
    result = get_bbc_sport_news_by_soup(5)
    save_list_to_JSON_file(result, "Beautiful Soup/result SPORTS NEWS.json")