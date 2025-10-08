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

#  从第一页开始读取
for num in range(0, 36):

    driver.get(r'https://about.uq.edu.au/experts/search?search=all+experts&page=' + str(num))
    print(driver.title)
    time.sleep(5)


    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/article/div/div[2]/div/div/div/section/div/div/div/div[2]/div[*]/div/a')

    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)


    for href in teacher_list:
        all_data = {}
        
        try:
            driver.get(href)
            
            time.sleep(2)
            all_data['website'] = driver.current_url
            print(driver.current_url)
        except:
            continue
    
        try:
            title = driver.find_element(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/div/div[1]/div/div/div/div[2]/div')
            # print(title.text)
            all_data['title'] = title.text
        except:
            pass
                                                    
        full_name = driver.find_element(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/div/div[1]/div/div/div/div[2]/h1 | //*[@id="block-uq-standard-theme-content"]/div/div[1]/div/div/div/div/h1')
        # print(full_name.text)
        all_data['full name'] = full_name.text

        try:
            email = driver.find_element(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/div/div[1]/div/div/div/div[2]/dl/div[1]/dd/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        try:
            orcid = driver.find_element(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/div/main/section/div/aside[2]/div[1]/div/div/div/ul/li/a')
            # print(orcid.text)
            all_data['orcid'] = orcid.get_attribute('href')
        except:
            pass

        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="block-uq-standard-theme-content"]/div/div[1]/div/div/div/div[2]/dl/div[2]/dd/a')
            # print(telephone.text)
            all_data['telephone'] = telephone.text
        except:
            pass


        try:                                          
            # 先拿到两个 dl
            dls = driver.find_elements(By.CSS_SELECTOR, 'dl.expert-profile__positions')

            position = []
            for dl in dls:
                for el in dl.find_elements(By.CSS_SELECTOR, 'dt, dd'):
                    t = el.text.strip()
                    if t:           # 去空串
                        position.append(t)
            all_data['position'] = position
        except:
            pass

        all_info = ''
        try:
            research_interests = driver.find_elements(By.XPATH, r'//*[@id="overview"]/div[4]/div/div/ul/li[*]')
            for i in research_interests:
                all_info += i.text
                all_info += '\n'
        except:
            pass

        try:
            backgrouds = driver.find_elements(By.XPATH, r'//*[@id="overview"]/div[1]/div/p | //*[@id="overview"]/div[1]/div/p[*]')
            for i in backgrouds:
                all_info += i.text
                all_info += '\n'
        except:
            pass

        if all_info != '':
            all_data['brief introduction'] = all_info
            final_data.append(all_data)
        print(all_data)

        time.sleep(3)

with open('University of Queensland (UQ).json', 'w') as json_file:
    json.dump(final_data, json_file)