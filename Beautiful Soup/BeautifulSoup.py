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
def get_html_by_url(url, save_folder = "Beautiful Soup/htmlbin", hardload = False, user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"):
    try:
        print()
    
        response_html = ""
        
        filename = f"{save_folder}/{hashlib.md5(url.encode("utf-8")).hexdigest()}.html"
        
        #Check if content exists in file AD not hardload
        if os.path.exists(filename) and not hardload:
            with open(filename, "rt", encoding="utf-8") as file:
                print(f"Reading html from: {filename}")
                response_html = file.read()
        else:
            print(f"Getting html from: {url}")
            response = requests.get(
                url=url, #url
                headers={#use headers to add my browser user agent
                "User-Agent" : user_agent
                })
            print('Status code:', response.status_code)
            
            if response.status_code < 200 or response.status_code > 299:
                raise Exception(f"Status coge {response.status_code} by getting from: {url}")
            
            response_html = response.text
            with open(filename, "wt", encoding="utf-8") as file:
                file.write(response_html)
                
        with open(filename, "rt", encoding="utf-8") as file:
                response_html = file.read()
        
        print()
        return response_html
    except Exception as e:
        print(f"ERROR: {e}")

def get_bbc_sport_news_by_soup(news_max_count_return):
    try:
        html_content = get_html_by_url(r"https://www.bbc.com/sport", hardload=True)
        
        soup = BeautifulSoup(html_content, features="lxml")
        
        #Get sports news promos by tag div contains data-testid="promo" AND type
        promos = soup.find_all("div", {"data-testid": "promo", "type": True})
        
        promos_data = []
        
        counter = news_max_count_return
        
        for promo in promos:
            temp_dict_promos_data = {}
            try:
                promo_a_link = promo.find_all("a")
                
                if promo_a_link is not None and len(promo_a_link):
                    
                    a_link_tag = promo_a_link[0]
                    
                    #Check reference
                    if a_link_tag.parent.has_attr("spacing"):
                        # The tag does not contain a full link, but navigation within the site, so we use concatenation
                        temp_dict_promos_data["Link"] = f"https://www.bbc.com{a_link_tag["href"]}"
                        
                        #Skip life and video (is no contains topics)
                        if "live" in temp_dict_promos_data["Link"] or "videos" in temp_dict_promos_data["Link"]:
                            continue
                    else:
                        continue
                    
                    #Then jump into news
                    current_news_html = get_html_by_url(temp_dict_promos_data["Link"], hardload=True)
                    
                    current_news_soup = BeautifulSoup(current_news_html, features="lxml")
                    
                    #Find list of topics 
                    ul_of_topics = current_news_soup.find("ul", {"spacing": "2"})
                    if ul_of_topics is None:
                        temp_dict_promos_data["Topics"] = None
                    else:
                        temp_dict_promos_data["Topics"] = []
                    
                        #Check parrent is a TopicList
                        class_topic_list = ul_of_topics.parent.previousSibling.get("class")
                        if class_topic_list:
                            if "TopicList" in class_topic_list[0]:
                                for liTopic in ul_of_topics.children:
                                    temp_dict_promos_data["Topics"].append(liTopic.find("a").text)
                
                promos_data.append(temp_dict_promos_data)
                counter -= 1
            except Exception as e:
                print(f"ERROR: {e}")
            
            if not counter:
                break
        
        pprint(promos_data)
        print(len(promos_data))
        
        return promos_data
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