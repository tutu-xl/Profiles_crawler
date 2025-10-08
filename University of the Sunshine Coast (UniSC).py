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
driver.get('https://www.usc.edu.au/profiles')

time.sleep(5)

profiles = driver.find_elements(By.XPATH, r'//*[@id="content"]/div/article/ul/li[*]/a')

final_data = []

#  从第一页开始读取
for profile in profiles:
    try:
        website = profile.get_attribute('href')
        driver.get(website)
    except:
        continue
    print(driver.title)
    time.sleep(5)

    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="content"]/div/article/ul/li[*]/a')

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
        
        name = driver.find_element(By.XPATH, r'//*[@id="top"]/header-block/div/h1')
        # print(name.text)
        all_data['full name'] = name.text

        try:
            all_info = ''                                               
            intro = driver.find_element(By.XPATH, r'//*[@id="content"]/div/div[1]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
            # print(all_info)
            all_data['brief introduction'] = all_info
        except Exception as e:
            print(e)

        print(all_data)
        final_data.append(all_data)

        time.sleep(1)

# print(final_data)
with open('University of the Sunshine Coast (UniSC).json', 'w') as json_file:
    json.dump(final_data, json_file)