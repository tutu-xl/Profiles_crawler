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

def isTruePerson():
    try:
        isTruePerson = driver.find_element(By.XPATH, r'/html/body/div[1]/div/h1')
        if isTruePerson.text == 'research-repository.uwa.edu.au':
            winsound.Beep(1000, 1000)
            time.sleep(30)
    except :
        pass


#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get(r'https://research-repository.uwa.edu.au/en/persons/?search=all+profile&pageSize=25&showAdvanced=false&allConcepts=true&inferConcepts=true&searchBy=PartOfNameOrTitle&page=' + str(num))
    isTruePerson()
    print(driver.title)
    time.sleep(3)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source         
    # print(html_content)                      
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main-content"]/div/div[2]/ul/li[*]/div/div/h3/a')
                         
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
            all_data['title'] = title.text
        except:
            continue

        
        # try:
        #     position = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[1]/p')
        #     all_data['position'] = [position.text]
        # except:
        #     pass

        try:                                            
            org_unit = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[2]/ul')
            text_list0 = [p.get_attribute('innerText') for p in org_unit.find_elements(By.XPATH, './/li')]
            all_org += '\n'.join(text_list0)
            # print(org_unit.text)
            all_data['org_unit'] = all_org
        except:
            pass
        
        try:                                        
            orcid = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[3]/a[2]')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except:
            pass

        try:                                        
            telephone = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[2]/ul/li[1]/span[2][not(.//a[@class="email"])]')
            # print(telephone.text)
            all_data['telephone'] = '+61' + telephone.text
        except:
            pass

        try:                                        
            email = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[2]/ul/li[2]/span[2]/a | //*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[2]/ul/li/span[2]/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        
        all_info = '' 
        try:                                           
            research = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div/div[2]/div[1]/div/div')
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
with open('University of Western Australia (UWA) ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)










