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
for num in range(0, 6):
    driver.get(r'https://www.acu.edu.au/searchresearchers?searchStudioQuery=Dr%20Mashud%20Rana&facets=&page=researcher&isGrid=false&orderBy=&start=' + str(num*10) + '&model=Default&facetFilters=1')
    print(driver.title)
    time.sleep(5)
                                              
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="searchstax-search-results"]/div[*]/div/div/div/div[1]/a')

    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list[:1]:
        all_data = {}
        print(driver.current_url)

        try:
            driver.get(href)
            # driver.get(r'https://www.acu.edu.au/research-and-enterprise/our-research-institutes/sprint-research-centre/our-people/dr-jack-hickey')
            time.sleep(2)
            all_data['website'] = driver.current_url
        except:
            continue
                  
        name = driver.find_element(By.XPATH, r'/html/body//div[4]/div/section/h2 | /html/body/div[1]/div[4]/div/section/h3 | /html/body/div[1]/div[4]/div/section/div/h2')
        parts = name.text.split(' ', 1)  # 只分割一次
        title = parts[0]  # Professor
        all_data['title'] = title
        full_name = parts[1]  # Ali Abbas
        all_data['full name'] = full_name

        try:
            org_unit = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section/h3 | /html/body/div[1]/div[4]/div/section/p')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:                                           
            telephone = driver.find_element(By.XPATH, r'//p[contains(., "Phone:")]')
            # print(telephone.text)
            all_data['telephone'] = telephone.text.split(': ', 1)[1]
        except Exception as e:
            # print(e)
            pass

        try:
            label = driver.find_element(By.XPATH, r'//strong[contains(text(), "Email:")]')
            email = label.find_element(By.XPATH, './following-sibling::a')
            # print(email.text)
            all_data['email'] = email.text
        except Exception as e:
            # print(e)
            pass

        try:
            label = driver.find_element(By.XPATH, r'//strong[contains(text(), "ORCID ID:")]')
            orcid = label.find_element(By.XPATH, './following-sibling::a')
            # print(org_unit.text)
            all_data['orcid'] = orcid.text
        except Exception as e:
            # print(e)
            pass

        try:
            all_info = ''
            keywords = ("Email", "Phone", "ORCID ID", "Location")   # 关键词列表
            research = driver.find_elements(By.XPATH, r"//h4 | //p | //h2")
            i = len(research)-1
            while(i >= 0):
                
                if any(k in research[i].text for k in keywords):    # 只要有一个命中
                    break
                i -= 1
            i += 1
            while(i < len(research) and research[i].tag_name != "h4" and research[i].tag_name != "h2"):
                all_info += research[i].text
                all_info += '\n'
                i += 1
            all_data['brief introduction'] = all_info
        except:
            pass

        
        print(all_data)
        final_data.append(all_data)
        time.sleep(2)

# print(final_data)
with open('Australian Catholic University (Melbourne campus).json', 'w') as json_file:
    json.dump(final_data, json_file)

