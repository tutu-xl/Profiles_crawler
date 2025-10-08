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
chrome_options.page_load_strategy = 'eager'
chrome_options.debugger_address = "127.0.0.1:" + args.port

driver = webdriver.Chrome(options=chrome_options)

final_data = []

#  从第一页开始读取
for num in range(args.start, args.end):
    driver.get('https://www.une.edu.au/search?collection=une~sp-global-search&facetScope=f.Tabs%7Cune~ds-staff%3DPeople&fmo=true&form=wrapper&gscope1=sc!&num_ranks=100&profile=_default&query=&start_rank=' + str((num-1)*100+1) + '&userkeys=7#course-search-results')
    print(driver.title)
    time.sleep(30)

    # # 获取页面完整的 HTML 内容
    # html_content = driver.page_source
    # print(html_content)
    list_items0 = driver.find_elements(By.XPATH, r'//*[@id="course-search-results"]/div/div[2]/div[2]/div[1]/div[*]/div[1]/div[1]/a')
                         
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

        name = driver.find_element(By.XPATH, r'//*[@id="main-content"]/div/div[1]/div[1]/h1')
        # print(name.text)
        parts = name.text.split(' ', 1)  # 只分割一次
        title = parts[0]
        all_data['title'] = title
        full_name = parts[1] 
        all_data['full name'] = full_name

        try:
            org_unit = driver.find_element(By.XPATH, r'//*[@id="main-content"]/div/div[1]/div[1]/p')
            # print(org_unit.text)
            all_data['org_unit'] = org_unit.text
        except:
            pass

        try:
            telephone = driver.find_element(By.XPATH, r'//*[@id="main-content"]/div/div[1]/div[3]/p[contains(., "Phone: ")]')
            # print(telephone.text)
            all_data['telephone'] = telephone.text.split(' ', 1)[1]
        except:
            pass
        
        try:
            email = driver.find_element(By.XPATH, r'//*[@id="main-content"]/div/div[1]/div[3]/p[contains(., "Email: ")]')
            # print(email.text)
            all_data['email'] = email.text.split(' ', 1)[1]
        except:
            pass

        all_info = ''
        try:
            intro = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div/div[1]/div[5]/h2 | //*[@id="main-content"]/div/div[1]/div[5]/p | //*[@id="main-content"]/div/div[1]/div[5]/ul/li')
            for i in intro[1:]:
                # print(i.text)
                if i.tag_name == 'h2':
                    break
                all_info += i.text
                all_info += '\n'
            # print(all_info)
            all_data['brief introduction'] = all_info
        except:
            pass

        
        if all_info != '':
            final_data.append(all_data)
            print(all_data)
        time.sleep(2)

# print(final_data)
with open('University of New England (UNE)' + str(args.start) + ' ' + str(args.end) + ' .json', 'w') as json_file:
    json.dump(final_data, json_file)






