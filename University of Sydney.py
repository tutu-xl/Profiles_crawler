from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import argparse


options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.add_argument('')
chrome_options.debugger_address = "127.0.0.1:9222"

driver = webdriver.Chrome(options=chrome_options)

final_data = []

driver.get('https://www.sydney.edu.au/engineering/about/our-people/academic-staff.html')
time.sleep(3)

list_items0 = driver.find_elements(By.XPATH, r'//*[@id="staffListContent"]//div[2]/ul/li[*]/a')

teacher_list = []
for num0, list0 in enumerate(list_items0):
    # print(list0.get_attribute('href'))
    teacher_list.append(list0.get_attribute('href'))


for teacher_link in teacher_list:
    all_data = {}
    all_data['website'] = teacher_link
    print(teacher_link)
    try:
        driver.get(teacher_link)
    except:
        continue
    time.sleep(1 + random.randint(2, 3))
    
    try:
        name = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div[1]/div[2]/div/div/div[3]/div/div/div[1]/h1/div')
        # print(name.text)
    except:
        continue

    parts = name.text.split(' ', 1)  # 只分割一次
    title = parts[0]  # Professor
    all_data['title'] = title
    full_name = parts[1]  # Ali Abbas
    all_data['full name'] = full_name
    
    try:
        position = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div[1]/div[2]/div/div/div[3]/div/div/div[4]/div[1]/div[1]/div[1]')
        # print(position.text)
        all_data['position'] = [position.text]
    except:
        pass

    try:
        org_unit = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div[1]/div[2]/div/div/div[3]/div/div/div[4]/div[1]/div[1]/div[2]')
        # print(org_unit.text)
        all_data['org_unit'] = org_unit.text
    except:
        pass

    try:
        email = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div[1]/div[2]/div/div/div[3]/div/div/div[4]/div[1]/div[2]/div[1]/div/div[3]/div[2]/a')
        # print(email.text)
        all_data['email'] = email.text
    except:
        pass

    try:
        telephone = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div[1]/div[2]/div/div/div[3]/div/div/div[4]/div[1]/div[2]/div[1]/div/div[1]/div[2]/div')
        # print(telephone.text)
        all_data['telephone'] = telephone.text
    except:
        pass

    try:
        # driver.find_element(By.XPATH, r'//*[@id="headingprofileresearchinterest"]/div/a').click()
        element = driver.find_element(By.XPATH, r'//*[@id="headingprofileresearchinterest"]/div/a')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(3)  # 等待滚动完成
        element.click()
        all_info = ''
        intro = driver.find_element(By.XPATH, r'//*[@id="collapseprofileresearchinterest"]/div')
        text_list = [p.text for p in intro.find_elements('xpath', './/p | .//ul//li')]
        all_info += '\n'.join(text_list)
        # print(all_info)
        all_data['brief introduction'] = all_info
    except:
        pass

    
    print(all_data)
    final_data.append(all_data)

    time.sleep(1)

print(final_data)
with open('Sydney.json', 'w') as json_file:
    json.dump(final_data, json_file)