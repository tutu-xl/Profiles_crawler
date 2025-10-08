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


# driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/leadership')
# driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/business')
# driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/engineering-and-mathematics')
# driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/information-technology')
driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/science')
print(driver.title)
time.sleep(5)
                                              
list_items0 = driver.find_elements(By.XPATH, r'//*[@id="table03426"]/tbody/tr[*]/td[1]/a')

teacher_list = []
for num0, list0 in enumerate(list_items0): 
    href = list0.get_attribute('href')
    # print(href)
    teacher_list.append(href)

for href in teacher_list:
    all_data = {}
    print(href)

    try:
        driver.get(href)
        # driver.get(r'https://federation.edu.au/institutes-and-schools/iiss/staff-profiles/staff-profiles/suryani-lim')
        time.sleep(2)
        all_data['website'] = driver.current_url
    except:
        continue

    match = re.match(r"(.+)\s*\((.+)\)", driver.find_element(By.XPATH, r'//*[@id="top"]/main/div/div/section/h1').text)
    if match:
        name = match.group(1).strip()
        title = match.group(2).strip()
        # print(name)
        # print(title)
        all_data['full name'] = name
        all_data['title'] = title
    try:                                            
        position = driver.find_element(By.XPATH, r"//th[text()='Position:']/following-sibling::td")
        # print(position.text)
        all_data['position'] = position.text
    except:
        pass

    try:
        telephone = driver.find_element(By.XPATH, r"//th[text()='Phone:']/following-sibling::td")
        # print(telephone.text)
        all_data['telephone'] += '+61' + telephone.text
    except:
        pass

    try:
        email = driver.find_element(By.XPATH, r"//th[text()='Email:']/following-sibling::td")
        # print(email.text)
        all_data['email'] += email.text
    except:
        pass

    try:
        all_info = ''

        research = driver.find_elements(By.XPATH, r"//h2 | //li | //p")
        num = 0
        while(num < len(research)):
            # print(research[num].text)
            if research[num].tag_name == 'h2' and (research[num].text == 'Research interests' or research[num].text == 'Short biography' or research[num].text == 'Biography'):
                num += 1
                while(num < len(research) and research[num].tag_name != 'h2'):
                    all_info += research[num].text
                    all_info += '\n'
                    num += 1
                num -= 1
            
            if research[num].tag_name == 'h3' and (research[num].text == 'Biography'):
                num += 1
                while(num < len(research) and research[num].tag_name != 'h3'):
                    all_info += research[num].text
                    all_info += '\n'
                    num += 1
                num -= 1
            num +=  1
                
        # print(all_info)
        all_data['brief introduction'] = all_info
    except:
        pass

    print(all_data)

    final_data.append(all_data)

# print(final_data)
with open('Federation University Australia 05.json', 'w') as json_file:
    json.dump(final_data, json_file)



