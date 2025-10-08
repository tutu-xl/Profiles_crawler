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
import winsound
import argparse

# 创建一个解析器
parser = argparse.ArgumentParser(description="Process some integers.")

# 添加命令行参数 --start 和 --end
parser.add_argument('--start', type=int, default=50, required=True, help="The starting number.")
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
    
    print(driver.title)
    driver.get('https://search.unisa.edu.au/s/search.html?f.Tabs%7Ctab=People&collection=study-search&f.Student+Type|pmpProgramsStudentType=Australian&start_rank=' + str((num)*10))
    time.sleep(1)
    
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="all"]/div[2]/div[1]//div[1]/div[1]/h3/a')

    teacher_list = []
    for num0, list0 in enumerate(list_items0):
        # print(list0.get_attribute('href'))
        teacher_list.append(list0.get_attribute('href'))
    
    
    for teacher_link in teacher_list:
        all_data = {}
        try:
            driver.get(teacher_link)
            # driver.get('https://people.unisa.edu.au/Steph.Webb')
        except:
            continue
        # print(teacher_link)
        time.sleep(random.randint(1, 3))
        all_data['website'] = driver.current_url

        try:
            name = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div[1]/h1')
            all_data['name'] = name.text
        except:
            continue

        try:
            position = driver.find_element(By.XPATH, r'//div[@class="layout-section-body"]//li')
            # print(position.text)
            all_data['position'] = position.text
        except:
            pass

        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div[2]/ul[2]/li[2]')
            # print(telephone.text)
            all_data['telephone'] = telephone.text
        except:
            pass

        try:
            email = driver.find_element(By.XPATH, r'//*[@id="profile"]/div/div[2]/ul[3]/li/a')
            # print(email.text)
            all_data['email'] = email.text
        except:
            pass

        try:
            driver.get(teacher_link + r'#About-me')
            # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, r'//*[@id="Biography"]/div[2]/div[1]/h3/a')))
            
            time.sleep(3)
            all_info = ''
            intro = driver.find_element(By.XPATH, r'//*[@id="About-me"]/div[3]')
            text_list = [p.text for p in intro.find_elements('xpath', './/p')]
            all_info += '\n'.join(text_list)
            if all_info == '':
                continue
            all_data['all_info'] = all_info
        except Exception as e:
            # print(e)
            pass
        
        print(all_data)
        final_data.append(all_data)

        time.sleep(1)

# print(final_data)
with open('South Australia ' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)


