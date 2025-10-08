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
    driver.get(r'https://www.acu.edu.au/searchresearchers?searchStudioQuery=&facets=fq%3Dresearcherfilter_s%3A%22Researcher%22&page=researcher&isGrid=false&orderBy=&start=' + str(num*10) + '&facetFilters=1&model=Default')
    print(driver.title)
    time.sleep(5)
                                      
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="searchstax-search-results"]/div[*]/div/div/div/div[1]/a')

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
        except:
            continue

        try:                                                   
            name = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section/h2 | /html/body/div[1]/div[4]/div/section/h3 | /html/body/div[1]/div[4]/div/section/div/div[1]/h3')
            print(name.text)
        except:
            continue
        try:
            pattern = re.compile(r'^((?:Honorary Associate )?Professor|(?:Associate )?Professor|Dr|Mr|Ms|Mrs|A/Prof)\s+(.+)$')
            m = pattern.match(name.text)
            title = m.group(1)
            full_name = m.group(2)
            all_data['title'] = m.group(1)
            all_data['full name'] = m.group(2)
        except:
            all_data['full name'] = name.text

        try:
            unit_org = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section/h3 | /html/body/div[1]/div[4]/div/section/div/div[1]/p[1]')
            # print(unit_org.text)
            all_data['unit_org'] = unit_org.text
        except:
            pass

        try:                                   
            telephone = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section//p[contains(.,"Phone")]')
            # print(telephone.text)
            all_data['telephone'] = telephone.text
        except:
            pass

        try:                                                 
            email = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section//p[contains(.,"Email:")]')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        try:                                          
            orcid = driver.find_element(By.XPATH, r'/html/body/div[1]/div[4]/div/section//p[contains(.,"ORCID ID:")]')
            # print(orcid.text)  
            all_data['orcid'] = orcid.text
        except:
            pass

        all_info = ''
        try:                               
            info_list = driver.find_elements(By.XPATH, r'/html/body/div[1]/div[4]/div/section/p[*] | /html/body/div[1]/div[4]/div/section/p | /html/body/div[1]/div[4]/div/section/h4')
            i = 0
            while(i < len(info_list)):
                
                while i < len(info_list) and len(info_list[i].find_elements(By.XPATH, r'./strong')) == 1:
                    i += 1
                while i < len(info_list) and info_list[i].tag_name != 'h4':
                    # print(info_list[i].text)
                    all_info += info_list[i].text
                    i += 1
                break
            # print(all_info)
            all_data['brief introduction'] = all_info
        except:
            pass

        print(all_data)
        final_data.append(all_data)
        time.sleep(3)

# print(final_data)
with open('Australian Catholic University (Brisbane campus) ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)

