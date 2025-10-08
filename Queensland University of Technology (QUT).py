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
parser.add_argument('--start', type=int, default=100, required=True, help="The starting number.")
parser.add_argument('--end', type=int, default=150, required=True, help="The ending number.")
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://www.qut.edu.au/research/our-experts?discipline=&divfac=&school=&query=&school_all=1&result_700033_result_page=' + str(num))
    print(driver.title)
    time.sleep(5)
                         
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="content"]/div[4]/div/div[1]/div[*]/div/div[2]/div/a')

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
            name = driver.find_element(By.XPATH, r'//*[@id="content"]/div[2]/div[1]/div[2]/h1/span')
            parts = name.text.split(' ', 1)  # 只分割一次
            title = parts[0]  # Professor
            all_data['title'] = title
            full_name = parts[1]  # Ali Abbas
            all_data['full name'] = full_name
        except:
            continue

        try:                                          
            telephone = driver.find_element(By.XPATH, r'//*[@id="biography-section"]/div/div/div/div[2]/p[2]/a')
            # print(telephone.text)
            all_data['telephone'] = [telephone.text]
        except:
            pass

        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="content"]/div[2]/div[1]/div[3]/div/div[2]/div/p')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:
            email = driver.find_element(By.XPATH, r'//*[@id="biography-section"]/div/div/div/div[2]/p[3]/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass
        
        all_info = ''
        intro = driver.find_elements(By.XPATH, r'//*[@id="biography-full"]/p | //*[@id="biography-full"]/ul[1]/li[*] | //*[@id="biography-full"]')
        text_list = [p.text for p in intro]
        all_info += '\n'.join(text_list)
        all_data['brief introduction'] = all_info

        final_data.append(all_data)
        print(all_data)
        time.sleep(3)

with open('Queensland University of Technology (QUT) ' + str(args.start) + ' ' + str(args.end) + '.json', 'w') as json_file:
    json.dump(final_data, json_file)




