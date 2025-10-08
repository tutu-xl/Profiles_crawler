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
import re
import winsound

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

def isTruePerson():
    try:
        isTruePerson = driver.find_element(By.XPATH, r'/html/body/div[1]/div/h1')
        if isTruePerson.text == 'research.torrens.edu.au':
            winsound.Beep(1000, 1000)
            time.sleep(30)
    except :
        pass


#  从第一页开始读取
for num in range(0, 3):
    driver.get('https://research.torrens.edu.au/en/persons/?page=' + str(num))
    isTruePerson()
    print(driver.title)
    time.sleep(3)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)                         
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main-content"]/div/div[2]/ul/li[*]/div/div[1]/h3/a')
                         
    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        all_data = {}
        
        try:
            driver.get(href)
            isTruePerson()
            time.sleep(3)
            print(driver.current_url)
            all_data['website'] = driver.current_url
        except:
            continue
        
        try:                                       
            name = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/h1')
            # print(full_name.text)
            all_data['full name'] = name.text
        except:
            continue
        

        try:                                           
            title = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[1]/p')
            text_list0 = title.get_attribute('innerText')
            print(title.get_attribute('innerText'))
            all_data['title'] = text_list0.split(', ')
            
        except:
            pass

        try:                                          
            org_unit = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div/ul/li/a/span')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:                                        
            orcid = driver.find_element(By.XPATH, r'(//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]//div/a[@aria-label="Orcid"])[2]')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except Exception as e:
            # print(e)
            pass

        try:                                          
            email = driver.find_element(By.XPATH, r'//li[@class="emails"]/span[2]/a')
            # print(email.text)
            all_data['email'] = email.get_attribute('innerText')
        except:
            pass

        all_info = '' 
        try:                                           
            research = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div//div/h3[contains(text(),"Research Interests")]/following-sibling::div')
            text_list0 = [p.get_attribute('innerText') for p in research.find_elements(By.XPATH, './/p | ./ul/li')]
            all_info += '\n'.join(text_list0)
        except Exception as e:
            # print(e)
            pass

        try:                                           
            research = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div//div/h3[contains(text(),"Research Profile")]/following-sibling::div')
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
        time.sleep(3)

# print(final_data)
with open('Torrens University Australia.json', 'w') as json_file:
    json.dump(final_data, json_file)










