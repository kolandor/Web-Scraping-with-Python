import json
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#new Selenium adds
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_data_vacancies(url: str, driver: webdriver, serp_count = 1):
    driver.get(url)
    
    vanacies = []
    
    while True:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="c-desktop-nav__link-level-1 | "]')))
        
        vacancies_elements = driver.find_elements(By.XPATH, '//li[@class="ais-Hits-item"]')
        
        for vacancies_element in vacancies_elements:
            vacancy_info = {}
            try:
                vacancy_info["title"] = vacancies_element.find_element(By.XPATH, './/h3[@class="text-2xl bold mb-16"]').text
                vacancy_info["url"] = vacancies_element.find_element(By.XPATH, './/a[@data-track-trigger="job_listing_link"]').get_attribute('href')
                vanacies.append(vacancy_info)
            except Exception as e:
                print(f"ERROR VACANCY LEVEL: {e}")
        
        serp_count -= 1
        
        next_btn = driver.find_elements(By.XPATH, '//a[@aria-label="Next"]')
        
        if not serp_count and next_btn is not None:
            break
        
        next_url = next_btn[0].get_attribute('href')
        
        driver.get(next_url)
    
    return vanacies

def save_list_to_JSON_file(listResult = [], fileToSave = "result.json"):
    try:
        print()
        if fileToSave:
            with open(fileToSave, "w", encoding="utf8") as file:
                #Mod fo saving russiat text: ensure_ascii=False, indent=4
                #NOT WORK WITH INNER HTML DATA
                json.dump(listResult, file, ensure_ascii=False, indent=4)
                print(f"Written to JSON file: {fileToSave}")
    except Exception as e:
        printt(f"ERROR: {e}")
    finally:
        print()

if __name__ == '__main__':
    try:
        options = Options()
        options.add_argument("--headless")  # Enabling headless mode
        options.add_argument("--disable-gpu")  # Disable GPU usage (optional)
        options.add_argument("--disable-cache") # (NEW FOR REFRESH)Configure the browser profile to not cache files
        options.add_argument("--window-size=1920,1080")  # Setting window sizes (optional)
        options.add_argument("--log-level=3")  # Suppress INFO, WARNING, and SEVERE logs
        
        service = Service(r"Selenium\driver\chromedriver.exe") # Browser driver path
        
        print("Driver starting...")
        driver = webdriver.Chrome(service=service, options=options)
        print("Driver READY!")
        
        base_url = "https://jobs.marksandspencer.com/job-search"
        
        vacancies = get_data_vacancies(base_url, driver, 2)
        
        pprint(vacancies)
        
        save_list_to_JSON_file(vacancies, "Selenium/result.json")
        
        print("Driver stoping...")
        driver.quit()
        print("END OF JOB")
        
    except Exception as e:
        print(f"ERROR GLOBAL LEVEL: {e}")