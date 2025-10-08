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
    driver.get('https://research.unsw.edu.au/researcher?page=' + str(num))
    print(driver.title)
    time.sleep(5)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="block-resgate8-content"]/div/div/div[*]/div/div[2]/a[1]')
                                        
    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        all_data = {}
        all_data['website'] = href
        print(href)
        driver.get(href)
        time.sleep(3)
        try:
            name = driver.find_element(By.XPATH, r'//*[@id="block-resgate8-breadcrumbs"]/nav/ul/li[3]')
            # print(name.text)
            parts = name.text.split(' ', 1)  # 只分割一次
            title = parts[0]
            all_data['title'] = title
            full_name = parts[1] 
            all_data['full name'] = full_name
        except:
            continue
        

        try:
            orcid = driver.find_element(By.XPATH, r'//*[@id="block-resgate8-content"]/article/div/div/div/div/div/div[3]/div[2]/div/a')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except:
            pass

        try:
            email = driver.find_element(By.XPATH, r'//*[@id="block-resgate8-content"]/article/div/div/div/div/div/div[2]/div[6]/div[2]/div/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="block-resgate8-content"]/article/div/div/div/div/div/div[2]/div[6]/div[1]/div[1]/a')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:
            element = driver.find_element(By.CSS_SELECTOR, 'a.body-toggle')
            driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)  # 等待滚动完成
            element.click()
            time.sleep(1)  # 等待滚动完成
        except Exception as e:
            # print(e)
            pass

        try: 
            all_info = ''
            intro = driver.find_elements(By.CSS_SELECTOR, "div.field-bio p, div.field-bio li")                       
            for p in intro:
                all_info += p.text
                all_info += '\n'
            # print(all_info)
            all_data['brief introduction'] = all_info
        except Exception as e:
            # print(e)
            pass

        print(all_data)
        final_data.append(all_data)
        time.sleep(2)
   
# print(final_data)
with open('University of New South Wales (UNSW Sydney) ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)


