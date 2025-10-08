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

# 创建一个解析器
parser = argparse.ArgumentParser(description="Process some integers.")

# 添加命令行参数 --start 和 --end
parser.add_argument('--start', type=str, default=100, required=True, help="The starting number.")
parser.add_argument('--end', type=str, default=150, required=True, help="The ending number.")
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
for num in range(ord(args.start), ord(args.end)):
    driver.get('https://www.newcastle.edu.au/profile/staff-list')
    print(driver.title)
    time.sleep(5)
    
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="uon-tab-content-staffaz"]/div[1]/a')
    list_items0[num-ord('a')].click()
    time.sleep(5)

    
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="group-' + chr(num).upper() + '"]/div/ul/li[*]/a') 
    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        all_data = {}
        all_data['website'] = driver.current_url
        print(href)
        try:
            driver.get(href)
            time.sleep(3)
        except:
            continue
        

        try:
            name = driver.find_element(By.XPATH, r'//*[@id="staff-profile"]/div[2]/div/h1')
            # print(name.text)
            parts = name.text.split(' ', 1)  # 只分割一次
            title = parts[0]
            all_data['title'] = title
            full_name = parts[1] 
            all_data['full name'] = full_name
        except:
            continue

        try:
            position = driver.find_element(By.XPATH, r'//*[@id="staff-profile"]/div[2]/div/p[1]')
            # print(position.text)
            all_data['position'] = [position.text]
        except:
            pass

        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="staff-profile"]/div[2]/div/p[2]')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:
            email = driver.find_element(By.XPATH, r'//*[@id="staff-profile"]/div[2]/ul/li[1]/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="staff-profile"]/div[2]/ul/li[2]')
            # print(telephone.text)
            all_data['telephone'] = '+61 ' + telephone.text
        except:
            pass

        try:
            all_info = ''
            intro = driver.find_element(By.XPATH, r'//*[@id="tab-career"]/div[1]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
            # print(all_info)
            all_data['brief introduction'] = all_info
        except Exception as e:
            # print(e)
            pass

        print(all_data)
        final_data.append(all_data)
        time.sleep(1)

# print(final_data)
with open('University of Newcastle ' + str(args.start) + ' ' + str(args.end) + '.json', 'w') as json_file:
    json.dump(final_data, json_file)


