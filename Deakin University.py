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
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://experts.deakin.edu.au/search?by=text&type=user')
    print(driver.title)
    time.sleep(5)

    # 定位 <select> 元素
    select_element = driver.find_element("css selector", "select[aria-label='Pagination']")
    driver.execute_script("arguments[0].style.display = 'block';", select_element)  # 强制显示

    # 使用 Select 类
    select = Select(select_element)

    # 选择指定 value 的 option，比如 value="5"
    select.select_by_value(str(num))
    time.sleep(3)

    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[3]/div[3]/div[2]/div[*]/div[2]/div/a')

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
            time.sleep(2)
            all_data['website'] = driver.current_url
        except:
            continue

        try:
            title = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/p')
            # print(title.text)
            all_data['title'] = title.text
        except:
            pass
        
        try:
            full_name = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/h1')
            # print(full_name.text)
            all_data['full name'] = full_name.text
        except:
            continue

        try:                                          
            position = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/p[1]')
            # print(position.text)
            all_data['position'] = [position.text]
        except:
            pass

        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/p[2]')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        all_info = '' 
        try:                              
            research = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[2]/div[2]/div/div/div[2]/div | //*[@id="app"]/div/main/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div')
            text_list0 = [p.text for p in research.find_elements(By.XPATH, './/p')]
            all_info += '\n'.join(text_list0)
        except:
            pass

        try:                                          
            research = driver.find_element(By.XPATH, r'//*[@id="app"]/div/main/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div')
            all_info += research.text
        except:
            pass
        
        # print(all_info)
        all_data['brief introduction'] = all_info

        try:                                                                          
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, r'button[data-qa="contactModalButton"]')))
            button.click()
            email = driver.find_element(By.XPATH, r'//*[@id="portalTarget"]/div[2]/div/div[2]/div/div/div/div/ul/li[1]/span/a | //*[@id="portalTarget"]/div[2]/div/div[2]/div/div/div/div/ul/li/span/a')
            # print(email.get_attribute('href'))
            all_data['email'] = email.get_attribute('href')
        except:
            pass

        
        print(all_data)
        if all_data != '':
            final_data.append(all_data)
        time.sleep(2)

# # print(final_data)
with open('Deakin University ' + str(args.start) + ' ' + str(args.end) + '.json', 'w') as json_file:
    json.dump(final_data, json_file)

