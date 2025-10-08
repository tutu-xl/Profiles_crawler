from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import random
import winsound


options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.add_argument('')
chrome_options.debugger_address = "127.0.0.1:9223"

driver = webdriver.Chrome(options=chrome_options)

final_data = []

#  从第一页开始读取
start_page = 20
for num in range(start_page, 30):
    
    print(driver.title)
    if num == start_page:
        driver.get('https://researchnow.flinders.edu.au/en/persons/')
        time.sleep(10) 
    else:
        driver.get('https://researchnow.flinders.edu.au/en/persons/?page=' + str(num))
        time.sleep(5)
    
    try:
        isTruePerson = driver.find_element(By.XPATH, r'/html/body/div[1]/div/h1')
        if isTruePerson.text == 'researchnow.flinders.edu.au':
            winsound.Beep(1000, 1000)
            time.sleep(20)
    except :
        pass
    
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main-content"]/div/div[2]/ul//div/div[1]/h3/a')

    teacher_list = []
    for num0, list0 in enumerate(list_items0):
        # print(list0.get_attribute('href'))
        teacher_list.append(list0.get_attribute('href'))
    
    
    for teacher_link in teacher_list:
        all_data = {}
        all_data['website'] = teacher_link
        driver.get(teacher_link)
        time.sleep(1 + random.randint(2, 6))
        name = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div/h1')
        # print(name.text)
        all_data['name'] = name.text

        try:
            person_type = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div/div/ul/li//span')
            print(person_type.get_attribute('class'))
            if(person_type.get_attribute('class') == 'studenttype'):
                continue
        except:
            continue

        try:
            org_text = ''
            organisation = driver.find_elements(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div/div[2]/ul/li//span')
            for org in organisation:
                org_text += org.text
            # print(org_text)
            all_data['organisation'] = org_text
        except :
            pass

        try:
            orcid = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div/div[*]/a[2]')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except :
            pass

        text_list = ''
        try:
            research = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div/div[2]/div[1]/div//div[1]')
            text_list0 = [p.text for p in research.find_elements(By.XPATH, './/p')]
            # print(text_list)
            text_list += '\n'.join(text_list0)
        except:
            pass
        try:
            research = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div/div[2]/div[1]/div[1]/div[2]/ul')
            text_list0 = [p.text for p in research.find_elements(By.XPATH, './/li')]
            # print(text_list)
            text_list += '\n'.join(text_list0)
        except :
            pass
        all_data['all_info'] = text_list

        print(all_data)
        final_data.append(all_data)

        time.sleep(1)

# print(final_data)
with open('array.json', 'w') as json_file:
    json.dump(final_data, json_file)