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
from selenium.webdriver.support.ui import Select
import re
import argparse

# 创建一个解析器
parser = argparse.ArgumentParser(description="Process some integers.")

# 添加命令行参数 --start 和 --end
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []


# driver.get(r'https://www.notredame.edu.au/about-us/faculties-and-schools/school-of-arts-and-sciences/sydney/school-staff')
# driver.get(r'https://www.notredame.edu.au/research/institutes-and-initiatives/institute-for-ethics-and-society/people')
# driver.get(r'https://www.notredame.edu.au/research/institutes-and-initiatives/institute-for-health-research/people')
# driver.get(r'https://www.notredame.edu.au/research/institutes-and-initiatives/nulungu/people/staff')
driver.get(r'https://www.notredame.edu.au/about-us/faculties-and-schools/school-of-law-and-business/business-fremantle/school-staff')


print(driver.title)
time.sleep(5)
                                              
list_items0 = driver.find_elements(By.XPATH, r'//div[starts-with(@id,"content_container_")]/p[*]/strong/a | //div[@class="accordion__content"]//tr[*]/td[1]//a')


teacher_list = []
for num0, list0 in enumerate(list_items0): 
    href = list0.get_attribute('href')
    # print(href)
    teacher_list.append(href)

for href in teacher_list:
    all_data = {}
    
    try:
        driver.get(href)
        time.sleep(3)
        all_data['website'] = driver.current_url
        print(driver.current_url)

        name = driver.find_element(By.XPATH, r'//*[@id="main"]/div[2]/div[2]/h1')
    except:
        continue

    
    try:
        pattern = re.compile(r'^((?:Honorary Associate )?Professor|(?:Associate )?Professor|Dr|Mr|Ms|Mrs)\s+(.+)$')
        m = pattern.match(name.text)
        all_data['title'] = m.group(1)
        all_data['full name'] = m.group(2)
    except:
        all_data['full name'] = name.text

    try:
        org_unit = driver.find_element(By.XPATH, r'//*[starts-with(@id,"content_container_")]/p[1]/strong')
        # print(org_unit.text)
        all_data['org_unit'] = org_unit.text
    except:
        pass

    try:
        email = driver.find_element(By.XPATH, r'//p[contains(text(), "Email:")]/a')
        # print(email.text)
        all_data['email'] = email.text
    except:
        pass

    try:
        
        telephone = driver.find_element(By.XPATH, r'//p[contains(text(), "Email:")]')
        # print(telephone.text)
        pattern_with_format = r'(?:\(?\d{2,3}\)?\s?)?\d{4}\s?\d{4}'
        # re.findall(pattern_with_format, telephone.text)
        if re.findall(pattern_with_format, telephone.text):
            all_data['telephone'] = re.findall(pattern_with_format, telephone.text)[-1]
    except Exception as e:
        # print(e)
        pass

    
    try:
        all_info = driver.find_element(By.XPATH, r'//*[@id="Biography-1"]/p')
        # print(all_info.text)
        all_data['brief introduction'] = all_info.text
    except:
        pass

    print(all_data)
    final_data.append(all_data)
    time.sleep(3)

# print(final_data)
with open('University of Notre Dame Australia 05.json', 'w') as json_file:
    json.dump(final_data, json_file)
