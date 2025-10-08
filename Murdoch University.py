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
# parser.add_argument('--start', type=int, default=100, required=True, help="The starting number.")
# parser.add_argument('--end', type=int, default=150, required=True, help="The ending number.")
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

driver.get(r'https://www.murdoch.edu.au/schools/information-technology/about/our-people?_gl=1*t58t2t*_gcl_au*NjYxNjA0MjAwLjE3NTk1MDUzNjM.*_ga*MTA0NzcyMTAwNS4xNzU5NTA1Mzk5*_ga_JJL7264DX3*czE3NTk1MDUzOTkkbzEkZzEkdDE3NTk1MDU0MDEkajU4JGwwJGgxNDYzMjc3NjMy')
print(driver.title)
time.sleep(3)

# # 获取页面完整的 HTML 内容
# html_content = driver.page_source         
# print(html_content)                      
list_items0 = driver.find_elements(By.XPATH, r'//*[@id="Body_T888C040F001_Col02"]/div[2]/ul[1]/li[*]/a')
                        
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
        print(driver.current_url)
        all_data['website'] = driver.current_url
    except:
        continue

    try:                                            
        name = driver.find_element(By.XPATH, r'/html/body/esp-root/mulo-header-main-footer-layout/main/div/esp-profile-standalone/esp-profile/mulo-centered-block-layout/div/mulo-side-main-layout/div[1]/div/exl-person-box/div[2]/h1/span')
        all_data['full name'] = name.text
    except:
        continue
    
    # try:                                            
    #     position = driver.find_element(By.XPATH, r'//*[@id="public-staff-profile"]/section/section[1]/dl/dt[contains(text(), "Position")]/following-sibling::dd[1]')
    #     all_data['position'] = [position.text]
    # except:
    #     pass

    try:                                            
        org_unit = driver.find_element(By.XPATH, r'/html/body/esp-root/mulo-header-main-footer-layout/main/div/esp-profile-standalone/esp-profile/mulo-centered-block-layout/div/mulo-side-main-layout/div[1]/div/exl-person-box/div[2]/h2')
        all_data['org_unit'] = org_unit.get_attribute('innerText')
    except:
        pass
    
    try:                                        
        orcid = driver.find_element(By.XPATH, r'/html/body/esp-root/mulo-header-main-footer-layout/main/div/esp-profile-standalone/esp-profile/mulo-centered-block-layout/div/mulo-side-main-layout/div[2]/div/mulo-nav-main-layout/div[3]/div/div/esp-profile-overview/section/div[2]/exl-content-box[1]/div[2]/div/exl-expandable-text/div/span/div/mulo-orcid-link/a[2]/span')
        # print(orcid.text)
        all_data['orcid'] = orcid.text
    except:
        pass

    try:                                        
        email = driver.find_element(By.XPATH, r'/html/body/esp-root/mulo-header-main-footer-layout/main/div/esp-profile-standalone/esp-profile/mulo-centered-block-layout/div/mulo-side-main-layout/div[2]/div/mulo-nav-main-layout/div[3]/div/div/esp-profile-overview/section/div[2]/exl-content-box/div[2]/div/div/a')
        # print(email.text)
        all_data['email'] = email.text
    except:
        pass

    
    all_info = '' 
    try:                                           
        research = driver.find_element(By.XPATH, r'/html/body/esp-root/mulo-header-main-footer-layout/main/div/esp-profile-standalone/esp-profile/mulo-centered-block-layout/div/mulo-side-main-layout/div[2]/div/mulo-nav-main-layout/div[3]/div/div/esp-profile-overview/section/div[1]/exl-content-box[1]/div[2]/div/exl-expandable-text/div/span/exl-html-display/div')
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
