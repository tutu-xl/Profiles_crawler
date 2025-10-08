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
import re
from selenium.webdriver.support.ui import Select

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
driver.get(r'https://www.cqu.edu.au/research/current-research/find-an-expert')
time.sleep(5)

current, total = 0, 512
while(current < 504):
    showing = driver.find_element(By.XPATH, r'//*[@id="skip-to-content"]/div/div/div/div/p')
    current, total_ = map(int, re.findall(r'\d+', showing.text))

    # ========== 1. 定位按钮 ==========
    wait = WebDriverWait(driver, 10)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Show More"]')))
    # ========== 2. 滚动到按钮 ==========
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", btn)
    time.sleep(1)      # 简单等待动画/懒加载完成，可按需调整
    btn.click()

    time.sleep(3)
                                                
list_items0 = driver.find_elements(By.XPATH, r'//*[@id="skip-to-content"]/div/div/div/a[*]')

teacher_list = []
for num0, list0 in enumerate(list_items0): 
    href = list0.get_attribute('href')
    # print(href)
    teacher_list.append(href)

for href in teacher_list:
    all_data = {}
    
    try:
        # driver.get(href)
        driver.get(r'https://staff-profiles.cqu.edu.au/home/view/2440?ignoreLogin=1')
        time.sleep(2)
        all_data['website'] = driver.current_url
        print(driver.current_url)
    except:
        continue

    try:                                       
        name = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div/div/div[2]/h4/b')
        # print(full_name.text)
        pattern = re.compile(r'^((?:Honorary Associate )?Professor|(?:Associate )?Professor|Dr.|Mr|Ms|Mrs|Doctor|A/Prof|AsPr)\s+(.+)$')
        m = pattern.match(name.text)
        
        all_data['full name'] = m.group(2)
        all_data['title'] = m.group(1)
    except:
        all_data['full name'] = name.text

    try:                                           
        org_unit = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div/div/div[2]')
        text_list0 = [p.get_attribute('innerText') for p in research.find_elements(By.XPATH, './/br')]
        all_info += '\n'.join(text_list0)
        all_data['org_unit'] = all_info
        
    except:
        pass

    try:                                        
        email = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div/div/div[2]/div[1]/div[2]/a')
        # print(email.text)
        all_data['email'] = email.text
    except Exception as e:
        # print(e)
        pass

    try:                                        
        telephone = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div/div/div[2]/div[1]/div[6]')
        # print(telephone.text)
        all_data['telephone'] = telephone.text
    except Exception as e:
        # print(e)
        pass

    try:                                        
        orcid = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div/div/div[2]/div[1]/div[4]/a')
        # print(orcid.text)
        all_data['orcid'] = orcid.text
    except Exception as e:
        # print(e)
        pass

    all_info = '' 
    try:                                           
        research = driver.find_element(By.XPATH, r'//*[@id="about"]/div')
        text_list0 = [p.get_attribute('innerText') for p in research.find_elements(By.XPATH, './/p | ./ul/li')]
        all_info += '\n'.join(text_list0)
        
    except Exception as e:
        # print(e)
        pass
    
    if all_info != '':
        # print(all_info)
        all_data['brief introduction'] = all_info
    
    print(all_data)
    final_data.append(all_data)
    time.sleep(30000)

# print(final_data)
with open('Central Queensland University (CQUniversity) ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)







