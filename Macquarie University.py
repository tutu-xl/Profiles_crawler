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
        if isTruePerson.text == 'researchnow.flinders.edu.au':
            winsound.Beep(1000, 1000)
            time.sleep(20)
    except :
        pass

#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://hdrss.mq.edu.au/supervisor/index?fields_of_work=&page=' + str(num))
    print(driver.title)
    isTruePerson()
    time.sleep(5)

    list_items0 = driver.find_elements(By.XPATH, r'/html/body/div[3]/div/div[2]/div[2]/div[*]/div/div/div[2]/a[1]')
                                               
    teacher_list = []
    for num0, list0 in enumerate(list_items0): 
        href = list0.get_attribute('href')
        # print(href)
        teacher_list.append(href)

    for href in teacher_list:
        all_data = {}
        all_data['website'] = href
        print(href)
        try:
            driver.get(href)
        except:
            continue
        isTruePerson()
        
        time.sleep(3)

        try:
            full_name = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/h1')
            print(full_name.text)
        except:
            continue

        try:

            title = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[1]/p')
            # print(title.text)
            all_data['title'] = title.text
        except Exception as e:
            # print(e)
            pass

        try: 
            org_unit = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[2]/ul/li[1]')
            print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except Exception as e:
            # print(e)
            pass

        try: 
            orcid = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[1]/div[3]/a[2]')
            # print(orcid.text)
            all_data['orcid'] = orcid.text
        except Exception as e:
            # print(e)
            pass

        try: 
            telephone = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[2]/ul/li[1]/span[2]')
            # print(telephone.text)
            all_data['telephone'] = telephone.text
        except Exception as e:
            # print(e)
            pass

        try: 
            email = driver.find_element(By.XPATH, r'//*[@id="page-content"]/div[1]/section/div[1]/div/div/section[1]/div[2]/div[2]/ul/li[2]/span[2]/a')
            # print(email.text)
            all_data['email'] = email.text
        except Exception as e:
            # print(e)
            pass

        all_info = ''
        try:  
            intro = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div/div[2]/div[1]/div/div[1]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
        except Exception as e:
            # print(e)
            pass

        try: 
            intro = driver.find_element(By.XPATH, r'//*[@id="main-content"]/section[1]/div/div[2]/div[1]/div/div[2]/p[1]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
        except Exception as e:
            # print(e)
            pass

        if all_info != '':
            all_data['brief introduction'] = all_info
        print(all_data)

        final_data.append(all_data)
        time.sleep(3)
    
# print(final_data)
with open('Macquarie University ' + str(args.start) + ' ' + str(args.end) + '.json', 'w') as json_file:
    json.dump(final_data, json_file)