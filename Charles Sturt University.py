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
parser.add_argument('--port', type=str, default='9222', required=True, help="The port number.")

# 解析命令行参数
args = parser.parse_args()

options = webdriver.ChromeOptions()
chrome_options = Options()
# chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []


driver.get('https://www.csu.edu.au/research/gulbali/find-experts')
print(driver.title)
time.sleep(5)

# # 获取页面完整的 HTML 内容
# html_content = driver.page_source
# print(html_content)
# list_items0 = driver.find_elements(By.XPATH, r'//*[@id="body"]/section[2]/div[3]/h3[*]')

teacher_list = []
# for num0, h3 in enumerate(list_items0): 
#     driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", h3)
#     time.sleep(2)  # 等待滚动完成
#     # 点击 h3 标签
#     h3.click()
#     time.sleep(0.5)  # 等待展开动画（如果有）
#     # print(href)
    
hrefs = driver.find_elements(By.XPATH, r'//div/div[*]/div/div/div[2]/h2/a')
for href in hrefs:
    # print(href.get_attribute('href'))
    teacher_list.append(href.get_attribute('href'))

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
        name = driver.find_element(By.XPATH, r'//*[@id="research_staff_profile"]/section[1]/h2 | //*[@id="content-banner-4201251"]/div[2]/h2')
        # print(name.text)
        parts = name.text.split(' ', 1)  # 只分割一次
        title = parts[0]
        all_data['title'] = title
        full_name = parts[1]
        all_data['full name'] = full_name
    except:
        pass

    try:
        position = driver.find_element(By.XPATH, r'//*[@id="research_staff_profile"]/section[1]/h3 | //*[@id="content-banner-4201251"]/div[2]/h3')
        # print(position.text)
        all_data['position'] = [position.text]
    except:
        pass

    try:
        org_unit = driver.find_element(By.XPATH, r'//*[@id="research_staff_profile"]/section[1]/p')
        # print(org_unit.text)
        all_data['org_unit'] = org_unit.text
    except:
        pass

    try:                                                                                                    
        email = driver.find_element(By.XPATH, r'//*[@id="research_staff_profile"]/section[1]/div[1]/div[2]/ul/li[2]/a | //*[@id="staff-bio-contact"]/div[1]/ul/li[span[text()="Email"]]/a')
        # print(email)
        all_data['email'] = email.text
    except:
        pass

    try:
        all_info = ''                              
        research = driver.find_element(By.XPATH, r'//*[@id="staff-bio-contact"]/div[*]')
        text_list0 = [p.text for p in research.find_elements(By.XPATH, './/p')]
        all_info += '\n'.join(text_list0)
        # print(all_info)
        all_data['brief introduction'] = all_info
    except:
        pass

    print(all_data)
    final_data.append(all_data)
    time.sleep(3)

# print(final_data)
with open('Charles Sturt University.json', 'w') as json_file:
    json.dump(final_data, json_file)
