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

driver.get(r'https://www.heinz.cmu.edu/faculty-research/profiles/')
print(driver.title)
time.sleep(3)

# # 获取页面完整的 HTML 内容
# html_content = driver.page_source
# print(html_content)                         
list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main"]/div/section[4]/ol/li[*]/article/div/p[2]/a')
                        
teacher_list = []
for num0, list0 in enumerate(list_items0): 
    href = list0.get_attribute('href')
    # print(href)
    teacher_list.append(href)

for num in range(2, 10):
    

    wait = WebDriverWait(driver, 15)
    pagination_nav = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__inner-container")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pagination_nav)
    time.sleep(1)

    page_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='pagination__link ' and text()='" + str(num) + "']")))
    page_link.click()

    time.sleep(3)

    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="main"]/div/section[4]/ol/li[*]/article/div/p[2]/a')

    teacher_list += [list0.get_attribute('href') for list0 in list_items0 if list0.get_attribute('href')]

for href in teacher_list:
    all_data = {}
    
    try:
        driver.get(href)
        time.sleep(3)
        print(driver.current_url)
        all_data['website'] = driver.current_url
    except:
        continue
    
    try:                                       
        name = driver.find_element(By.XPATH, r'//*[@id="main"]/div/section[2]/div/h1')
        # print(full_name.text)
        all_data['full name'] = name.text
    except:
        continue

    try:  
        position = driver.find_element(By.XPATH, r'//*[@id="main"]/div/section[2]/div/h2')
        # print(position.text)
        all_data['position'] = position.text
    except:
        pass

    try: 
        telephone = driver.find_element(By.XPATH, r'//span[@class="vcard__telephone"]/a')
        # print(telephone.text)
        all_data['telephone'] = telephone.text
    except:
        pass

    try: 
        email = driver.find_element(By.XPATH, r'//span[@class="vcard__email"]/a')
        # print(email.text)
        all_data['email'] = email.text
    except Exception as e:
        # print(e)
        pass

    all_info = ''

    try: 
        research = driver.find_element(By.XPATH, r'//*[@id="main"]/div/section[2]/div[@class="user-markup"]')
        text_list0 = [p.get_attribute('innerText') for p in research.find_elements(By.XPATH, './/p | ./ul/li')]
        all_info += '\n'.join(text_list0)
    except Exception as e:
        # print(e)
        pass

    try:                                            
        research = driver.find_element(By.XPATH, r'//*[@id="rmjs-1"]/div[@class="user-markup"]')
        text_list0 = [p.get_attribute('innerText') for p in research.find_elements(By.XPATH, './/p | ./ul/li')]
        all_info += '\n'.join(text_list0)
    except Exception as e:
        # print(e)
        pass
    if all_info != '':
        all_data['brief introduction'] = all_info

    print(all_data)
    final_data.append(all_data)
    time.sleep(3)

# print(final_data)
with open('Carnegie Mellon University – Australia.json', 'w') as json_file:
    json.dump(final_data, json_file)






